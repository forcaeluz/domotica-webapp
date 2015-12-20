from Devices.IInput import IInput
from Hardware.IArduinoCommunicator import IArduinoCommunicator


class ArduinoDigitalInput(IInput):

    def __init__(self, name, port, address, communicator=None):
        """
            ArduinoDigitalInput constructor
        :param name: Human readable name given to input. (i.e.: Door sensor, Light switch, etc)
        :param port: Port name on the arduino. Note this is different than the AtMega port names.
        :param address: Address used to access the data for this input.
        :param communicator: Used to send commands to the Arduino.
        """
        assert isinstance(communicator, IArduinoCommunicator)
        self.__name = name
        self.__port = port
        self.__register_address = address
        self.__communicator = communicator

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_value(self):
        address = self.__register_address
        sub_address = self.__SUB_ADDRESSES['DATA']
        self.__value = self.__communicator.request_data(address, sub_address)
        return self.__value

    def get_type(self):
        return self.__type

    def enable_pullup(self):
        assert not self.__enabled, 'Cannot enable pull-up during operation'
        self.__pull_up_enabled = True
        address = self.__register_address
        sub_address = self.__SUB_ADDRESSES['PULL_UP_ENABLED']
        data = 1
        self.__communicator.send_command(address, sub_address, data)

    def disable_pullup(self):
        assert not self.__enabled, 'Cannot disable pull-up during operation'
        self.__pull_up_enabled = False
        address = self.__register_address
        sub_address = self.__SUB_ADDRESSES['PULL_UP_ENABLED']
        data = 0
        self.__communicator.send_command(address, sub_address, data)

    def enable(self):
        address = self.__register_address
        sub_address = self.__SUB_ADDRESSES['ENABLED']
        data = 1
        self.__communicator.send_command(address, sub_address, data)
        self.__enabled = True

    def disable(self):
        address = self.__register_address
        sub_address = self.__SUB_ADDRESSES['ENABLED']
        data = 0
        self.__communicator.send_command(address, sub_address, data)
        self.__enabled = False

    def is_enabled(self):
        return self.__enabled

# Private members
    __name = ''
    __value = 0
    __type = 'ArduinoDigitalInput'
    __port = ''
    __pull_up_enabled = False
    __communicator = None
    __enabled = False

    __SUB_ADDRESSES = dict(
        DATA=0x00,
        ENABLED=0x01,
        PULL_UP_ENABLED=0x02
    )
