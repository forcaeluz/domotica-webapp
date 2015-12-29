import unittest
from Utilities.CrcCalculator import Crc8Calculator


class TestCrc8Calculator(unittest.TestCase):
    def test_constructor(self):
        calculator = Crc8Calculator(0x97)

    def test_crc_computation(self):
        EXPECTED_CRC = 0xD3
        calculator = Crc8Calculator(0x97)
        data = bytearray(9)
        data[0] = 0x01
        data[1] = 0x02
        data[2] = 0x03
        data[3] = 0x04
        data[4] = 0x05
        data[5] = 0x06
        data[6] = 0x07
        data[7] = 0x08
        data[8] = 0x09
        self.assertEqual(EXPECTED_CRC, calculator.compute_crc(data))

    def test_crc_check(self):
        EXPECTED_CRC = 0xD3
        calculator = Crc8Calculator(0x97)
        data = bytearray(10)
        data[0] = 0x01
        data[1] = 0x02
        data[2] = 0x03
        data[3] = 0x04
        data[4] = 0x05
        data[5] = 0x06
        data[6] = 0x07
        data[7] = 0x08
        data[8] = 0x09
        data[9] = EXPECTED_CRC
        self.assertEqual(0, calculator.compute_crc(data))

if __name__ == '__main__':
    unittest.main()
