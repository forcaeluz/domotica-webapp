import unittest
from Utilities.CrcCalculator import Crc8Calculator


class TestCrc8Calculator(unittest.TestCase):
    def test_constructor(self):
        calculator = Crc8Calculator(0x97)


if __name__ == '__main__':
    unittest.main()
