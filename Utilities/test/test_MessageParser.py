import unittest
from Utilities.MessageParser import MessageParser
from Utilities.CrcCalculator import Crc8Calculator


class TestMessageParser(unittest.TestCase):
    def test_constructor(self):
        parser = MessageParser()

    def test_pack_command(self):
        parser = MessageParser()
        crc_calc = Crc8Calculator(0x97)
        ADDRESS = 0x01
        SUB_ADDRESS = 0x02
        DATA = 10
        expected_msg = bytearray(10)
        expected_msg[0] = 0xFF
        expected_msg[1] = 0x00
        expected_msg[2] = 0x00
        expected_msg[3] = ADDRESS
        expected_msg[4] = SUB_ADDRESS
        expected_msg[5:9] = DATA.to_bytes(4, byteorder='little')
        expected_msg[9] = crc_calc.compute_crc(expected_msg[0:9])
        self.assertEqual(expected_msg, parser.pack_command(ADDRESS, SUB_ADDRESS, DATA))

    def test_parse_string_message(self):
        parser = MessageParser()
        crc_calc = Crc8Calculator(0x97)
        msg = bytearray(10)
        msg[0] = 0xFF
        msg[1] = 0x03
        msg[2] = 0x00
        msg[3:9] = 'Hello '.encode()
        msg[9] = crc_calc.compute_crc(msg[0:9])
        expected_parsed_message = dict()
        expected_parsed_message['type'] = 'string'
        expected_parsed_message['id'] = 0x00
        expected_parsed_message['data'] = 'Hello '
        self.assertEqual(expected_parsed_message, parser.parse_incoming_message(msg))

    def test_parse_invalid_header(self):
        parser = MessageParser()
        crc_calc = Crc8Calculator(0x97)
        msg = bytearray(10)
        msg[0] = 0xFE
        msg[1] = 0x03
        msg[2] = 0x00
        msg[3:9] = 'Hello '.encode()
        msg[9] = crc_calc.compute_crc(msg[0:9])
        with self.assertRaises(AssertionError) as cm:
            parser.parse_incoming_message(msg)
        self.assertEqual('Invalid message header', str(cm.exception))

    def test_parse_invalid_header(self):
        parser = MessageParser()
        crc_calc = Crc8Calculator(0x97)
        msg = bytearray(10)
        msg[0] = 0xFF
        msg[1] = 0x03
        msg[2] = 0x00
        msg[3:9] = 'Hello '.encode()
        msg[9] = crc_calc.compute_crc(msg[0:9])
        msg[1] = 0x01 # Simulate bit-flip.
        with self.assertRaises(AssertionError) as cm:
            parser.parse_incoming_message(msg)
        self.assertEqual('CRC check failed', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
