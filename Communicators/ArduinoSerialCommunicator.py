from binascii import hexlify
from logging import getLogger
from logging.config import dictConfig
from threading import Thread
from queue import Queue
from serial import Serial, SerialException
from time import sleep

from Communicators.IArduinoCommunicator import IArduinoCommunicator
from Utilities.CrcCalculator import Crc8Calculator
from Utilities.MessageParser import MessageParser
from Utilities.ArduinoLogger import ArduinoLogger
from log_config import LOGGING


class ArduinoSerialCommunicator(IArduinoCommunicator):
    """

    """
    def __init__(self):
        """

        """
        CRC_POLYNOMIAL = 0x97
        self.app_logger = getLogger('application.usart_communication')
        self.app_logger.info('Creating serial communicator')
        self.__parser = MessageParser()
        self.__arduino_logger = ArduinoLogger()
        self.__serial_port = Serial()
        self.__crc_calculator = Crc8Calculator(CRC_POLYNOMIAL)
        self.__receiver_thread = Thread(target=self.__read_incoming_message)
        self.__is_reading = False
        self.__request_queue = Queue()
        self.__command_queue = Queue()
        self.__request_counter = 0
        self.__command_counter = 0
        self.__input_message_queue = Queue()

    def request_object_data(self, address, sub_address):
        content = self.__parser.pack_request(self.__command_counter, address, sub_address)
        self.app_logger.debug('Writing request to arduino: %s', hexlify(content))
        self.__serial_port.write(content)
        msg = self.__get_incoming_message()
        if msg['id'] == self.__command_counter:
            self.app_logger.debug('Request replied successfully')
            print('Arduino replied with: %s' % msg['data'])
        self.__request_counter += 1
        self.__request_counter %= 256

    def open(self, port_name):
        self.__serial_port.port = port_name
        self.__serial_port.baudrate = 57600
        self.__serial_port.open()
        self.__start_reading()

    def close(self):
        self.__stop_reading()
        self.__serial_port.close()

    def write_to_object(self, address, sub_address, data):
        content = self.__parser.pack_command(self.__command_counter, address, sub_address, data)
        self.app_logger.debug('Writing command to arduino')
        self.app_logger.debug(content)
        self.__serial_port.write(content)
        msg = self.__get_incoming_message()
        if msg['id'] == self.__command_counter:
            if msg['data'] == 1:
                self.app_logger.debug('Command applied successfully')

        self.__command_counter += 1
        self.__command_counter %= 256

    def __start_reading(self):
        self.__is_reading = True
        self.__receiver_thread.setDaemon(True)
        self.__receiver_thread.start()

    def __stop_reading(self):
        self.__is_reading = False
        self.__receiver_thread.join()

    def __read_incoming_message(self):
        incoming_message = bytearray()
        msg_size = 0
        try:
            while self.__is_reading:
                data = ord(self.__serial_port.read(1))

                # First byte condition
                if data == 0xFF and len(incoming_message) == 0:
                    incoming_message.append(data)
                # Complete header (0xFF + msgType) Stop to determine size
                elif len(incoming_message) == 1:
                    incoming_message.append(data)
                    msg_size = self.__parser.get_message_size(incoming_message)
                elif 1 < len(incoming_message) < msg_size:
                    incoming_message.append(data)
                    if len(incoming_message) == msg_size:
                        self.__process_message(incoming_message)
                        incoming_message = bytearray()
                        msg_size = 0

        except SerialException as e:
            self.app_logger.fatal('Error reading serial port:')
            self.app_logger.fatal(e.strerror)

    def __process_message(self, message):
        self.app_logger.debug('Processing incoming message.')
        assert(type(message) is bytearray)
        parsed_msg = dict(type='unknown')

        try:
            parsed_msg = self.__parser.parse_incoming_message(message)
        except AssertionError as ae:
            self.app_logger.error('Invalid incoming message with error ' + ae.args[0])
            self.app_logger.error('Data: %s' % hexlify(message))
            self.__serial_port.flush()

        if parsed_msg['type'] == 'string':
            self.__arduino_logger.process_log_message(parsed_msg)
        elif parsed_msg['type'] == 'error':
            self.app_logger.warning('Arduino replied with error message')
            self.app_logger.warning('Data: %s' % hexlify(message))
        else:
            self.app_logger.debug('Message put in queue')
            self.app_logger.debug('Type: %s' % parsed_msg['type'])
            self.__input_message_queue.put(parsed_msg)

    def __get_incoming_message(self):
        msg = self.__input_message_queue.get()
        self.app_logger.debug('Message read from queue')
        self.app_logger.debug('Type: %s' % msg['type'])
        self.__input_message_queue.task_done()
        return msg

if __name__ == '__main__':
    """
    The main function allows to use this communicator class as a stand-alone.
    This can be useful for testing the implementation of the code on the arduino.
    """
    dictConfig(LOGGING)
    communicator = ArduinoSerialCommunicator()
    communicator.open('/dev/ttyUSB0')
    communicator.write_to_object(0x10, 0x02, 0)
    communicator.write_to_object(0x11, 0x02, 0)
    communicator.write_to_object(0x12, 0x02, 0)
    communicator.write_to_object(0x13, 0x02, 1)

    communicator.write_to_object(0x10, 0x00, 0)
    communicator.write_to_object(0x11, 0x00, 0)
    communicator.write_to_object(0x12, 0x00, 1)
    while True:
        sleep(3)
        communicator.write_to_object(0x10, 0x00, 1)
        communicator.write_to_object(0x11, 0x00, 0)
        communicator.write_to_object(0x12, 0x00, 0)
        sleep(3)
        communicator.write_to_object(0x10, 0x00, 0)
        communicator.write_to_object(0x11, 0x00, 1)
        communicator.write_to_object(0x12, 0x00, 0)
        sleep(1)
        communicator.write_to_object(0x10, 0x00, 0)
        communicator.write_to_object(0x11, 0x00, 0)
        communicator.write_to_object(0x12, 0x00, 1)

        # communicator.get_incoming_message()
