from Utilities.CrcCalculator import Crc8Calculator
from logging import getLogger
from binascii import hexlify


class MessageParser:

    COMMAND_MESSAGE = 0x00
    REQUEST_MESSAGE = 0x01
    REPLY_MESSAGE = 0x02
    HEART_BEAT_MESSAGE = 0x03
    UPDATE_MESSAGE = 0x04
    STRING_MESSAGE = 0x05
    ERROR_MESSAGE = 0x06

    CRC_POLYNOMIAL = 0x97

    __MESSAGE_SIZES = {
        'string': 12,
        'reply': 10,
        'error': 6,
        'update': 10,
        'heart_beat': 6,
        'command': 10
    }

    def __init__(self):
        self.__crc_checker = Crc8Calculator(self.CRC_POLYNOMIAL)
        self.app_logger = getLogger('application.message_parser')
        super().__init__()

    def parse_incoming_message(self, data):
        assert isinstance(data, bytearray), 'Incoming data is not a bytearray'
        assert data[0] == 0xFF, 'Invalid message header'
        assert self.__crc_checker.compute_crc(data) == 0, 'CRC check failed'

        self.app_logger.debug('Parsing incoming message: %s' % hexlify(data))

        msg = dict()
        msg['type'] = self.__get_message_type_string(data[1])
        if msg['type'] == 'string':
            msg['id'] = data[2]
            msg['data'] = data[3:11]
        else:
            msg['id'] = data[2]
            msg['address'] = data[3]
            msg['sub_address'] = data[4]
            msg['data'] = int.from_bytes(data[5:9], byteorder='little')
        return msg

    def pack_command(self, count, address, sub_address, command):
        assert isinstance(command, int)
        data = bytearray(10)
        data[0] = 0xFF
        data[1] = self.COMMAND_MESSAGE
        data[2] = count
        data[3] = address
        data[4] = sub_address
        data[5:9] = command.to_bytes(4, byteorder='little')
        data[9] = self.__crc_checker.compute_crc(data[0:9])
        return data

    def pack_request(self, count, address, sub_address):
        data = bytearray(10)
        data[0] = 0xFF
        data[1] = self.REQUEST_MESSAGE
        data[2] = count
        data[3] = address
        data[4] = sub_address
        data[5] = self.__crc_checker.compute_crc(data[0:5])
        return data

    def __get_message_type_string(self, type_number):
        return_value = ''
        if type_number == self.COMMAND_MESSAGE:
            return_value = 'command'
        elif type_number == self.REPLY_MESSAGE:
            return_value = 'reply'
        elif type_number == self.UPDATE_MESSAGE:
            return_value = 'update'
        elif type_number == self.STRING_MESSAGE:
            return_value = 'string'
        elif type_number == self.ERROR_MESSAGE:
            return_value = 'error'
        return return_value

    def get_message_size(self, message_header):
        assert isinstance(message_header, bytearray), 'Incoming data is not a bytearray'
        assert message_header[0] == 0xFF, 'Invalid message header'
        self.app_logger.debug('Determining type and size for header: %s' % hexlify(message_header))
        self.app_logger.debug(message_header)
        msg_type = self.__get_message_type_string(message_header[1])
        size = self.__MESSAGE_SIZES[msg_type]
        self.app_logger.debug("Determined message type and size: %s, %d" % (msg_type, size))
        return size
