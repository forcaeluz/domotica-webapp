from Utilities.CrcCalculator import Crc8Calculator


class MessageParser:

    COMMAND_MESSAGE = 0x00
    REPLY_MESSAGE = 0x01
    UPDATE_MESSAGE = 0x02
    STRING_MESSAGE = 0x03

    CRC_POLYNOMIAL = 0x97

    def __init__(self):
        self.__crc_checker = Crc8Calculator(self.CRC_POLYNOMIAL)
        super().__init__()

    def parse_incoming_message(self, data):
        assert isinstance(data, bytearray), 'Incomming data is not a bytearray'
        assert data[0] == 0xFF, 'Invalid message header'
        assert self.__crc_checker.compute_crc(data) == 0, 'CRC check failed'

        msg = dict()
        msg['type'] = self.__get_message_type_string(data[1])
        if msg['type'] == 'string':
            msg['id'] = data[2]
            msg['data'] = data[3:9].decode()
        else:
            msg['id'] = data[2]
            msg['address'] = data[3]
            msg['sub_address'] = data[4]
            msg['data'] = int.from_bytes(data[5:9], byteorder='little')
        return msg

    def pack_command(self, address, sub_address, command):
        assert isinstance(command, int)
        data = bytearray(10)
        data[0] = 0xFF
        data[1] = self.COMMAND_MESSAGE
        data[2] = 0
        data[3] = address
        data[4] = sub_address
        data[5:9] = command.to_bytes(4, byteorder='little')
        data[9] = self.__crc_checker.compute_crc(data[0:9])
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
        return return_value
