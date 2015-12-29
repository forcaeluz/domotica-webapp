
from logging import getLogger
from logging.config import dictConfig
from threading import Thread
from queue import Queue
from serial import Serial, SerialException

from Communicators.IArduinoCommunicator import IArduinoCommunicator
from Utilities.CrcCalculator import Crc8Calculator
from Utilities.MessageParser import MessageParser
from Utilities.ArduinoLogger import ArduinoLogger
from log_config import LOGGING


class ArduinoUsartCommunicator(IArduinoCommunicator):

    COMMAND_MESSAGE = 0x00
    REPLY_MESSAGE = 0x01
    UPDATE_MESSAGE = 0x02
    STRING_MESSAGE = 0x03
    CRC_POLYNOMIAL = 0x97

    def __init__(self):
        self.__setup_logging()
        self.__parser = MessageParser()
        self.__arduino_logger = ArduinoLogger()
        self.serial_port = Serial()
        self.__crc_calculator = Crc8Calculator(self.CRC_POLYNOMIAL)
        self.__receiver_thread = Thread(target=self.__read_incoming_message)
        self.__is_reading = False
        self.__log_buffer = bytearray()
        self.__current_log_message = 0
        self.__input_message_queue = Queue()

    def open(self, port_name):
        self.serial_port.port = port_name
        self.serial_port.baudrate = 57600
        self.serial_port.open()
        self.__start_reading()

    def close(self):
        self.__stop_reading()
        self.serial_port.close()

    def get_incoming_message(self):
        msg = self.__input_message_queue.get()
        self.app_logger.info('Message read from queue')
        self.app_logger.debug('Type: %s' % msg['type'])
        self.__input_message_queue.task_done()
        return msg

    def __start_reading(self):
        self.__is_reading = True
        self.__receiver_thread.setDaemon(True)
        self.__receiver_thread.start()

    def __stop_reading(self):
        self.__is_reading = False
        self.__receiver_thread.join()

    def __read_incoming_message(self):
        incoming_message = bytearray()
        try:
            while self.__is_reading:
                data = ord(self.serial_port.read(1))
                # First byte condition
                if data == 0xFF and len(incoming_message) == 0:
                    incoming_message.append(data)
                # Intermediary bytes
                elif 0 < len(incoming_message) < 10:
                    incoming_message.append(data)
                    if len(incoming_message) == 10:
                        self.__process_message(incoming_message)
                        incoming_message = bytearray()

        except SerialException as e:
            print('Error reading serial port:')
            print(e.strerror)

    def __process_message(self, message):
        assert(type(message) is bytearray)
        parsed_msg = dict(type='unknown')
        try:
            parsed_msg = self.__parser.parse_incoming_message(message)
        except AssertionError as ae:
            self.app_logger.error('Invalid incoming message with error ' + ae.args[0])
            self.serial_port.flush()

        if parsed_msg['type'] == 'string':
            self.__arduino_logger.process_log_message(parsed_msg)
        else:
            self.app_logger.info('Message put in queue')
            self.app_logger.debug('Type: %s' % parsed_msg['type'])
            self.__input_message_queue.put(parsed_msg)

    def __setup_logging(self):
        self.app_logger = getLogger('application.usart_communication')

"""
The main function allows to use this communicator class as a stand-alone.
This can be useful for testing the implementation of the code on the arduino.
"""
if __name__ == '__main__':
    dictConfig(LOGGING)
    communicator = ArduinoUsartCommunicator()
    communicator.open('/dev/ttyUSB0')
    while True:
        communicator.get_incoming_message()
