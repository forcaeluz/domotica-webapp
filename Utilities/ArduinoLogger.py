from logging import Logger, getLogger
from logging.handlers import RotatingFileHandler


class ArduinoLogger:
    def __init__(self):
        self.__arduino_logger = getLogger('arduino')
        handler = self.__arduino_logger.handlers[0]
        assert isinstance(handler, RotatingFileHandler)
        handler.doRollover()
        self.__app_logger = getLogger('application.usart_communication')
        self.__log_buffer = bytearray()
        self.__current_log_message = 0

    def process_log_message(self, message):
        self.__app_logger.debug('Expected message: %d' % self.__current_log_message)
        self.__app_logger.debug('Incoming message: %d' % message['id'])

        if message['id'] == self.__current_log_message:
            self.__log_buffer.extend(message['data'])
            self.__app_logger.debug(self.__log_buffer)
            if self.__log_buffer.endswith(b'\00'):
                self.__arduino_logger.debug(self.__log_buffer.decode().replace('\n', ''))
                self.__log_buffer = bytearray()
                self.__current_log_message += 1
                self.__current_log_message %= 256
        else:
            self.__app_logger.warning('Previous message was not completed')
            self.__app_logger.warning(self.__log_buffer.decode().replace('\n', ''))
            self.__arduino_logger.debug(self.__log_buffer.decode().replace('\n', ''))

            self.__log_buffer = bytearray()
            self.__log_buffer.extend(message['data'])
            self.__current_log_message = message['id']

        self.__app_logger.info('Log message parsed')
