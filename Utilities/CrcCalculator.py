class Crc8Calculator:
    def __init__(self, polynomial):
        self.__polynomial = polynomial
        self.__CRC_TABLE = bytearray(256)
        self.__fill_crc_table()

    def compute_crc(self, message):
        crc = 0
        for i in range(0, len(message)):
            crc = self.__add_crc(crc, message[i])

        return crc

    def __fill_crc_table(self):
        mask = (1 << 7)
        mask2 = (1 << 8) - 1
        for i in range(0, 256):
            crc = i
            for j in range(8):
                if crc & mask:
                    crc = (crc << 1) ^ self.__polynomial
                else:
                    crc <<= 1

            self.__CRC_TABLE[i] = crc & mask2

    def __add_crc(self, crc, byte):
        index = crc ^ byte
        new_crc = self.__CRC_TABLE[index]
        return new_crc

