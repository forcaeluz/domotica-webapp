from Devices.ADevice import ADevice
from Devices.ArduinoDigitalInput import ArduinoDigitalInput
from Hardware.IArduinoCommunicator import IArduinoCommunicator
from Devices.IInput import IInput


class Arduino(ADevice):
    __input_list = {}
    __output_list = {}
    __communicator = None
    __address = ''

    __used_ports = []
    ANALOG_INPUT_MAPPING = {
        'A0': 'PC0',
        'A1': 'PC1',
        'A2': 'PC2',
        'A3': 'PC3',
        'A4': 'PC4',
        'A5': 'PC5',
        'A6': 'PC6',
        'A7': 'PC7'
    }
    DIGITAL_INPUT_MAPPING = {
        'D0': 'PD0',
        'D1': 'PD1',
        'D2': 'PD2',
        'D3': 'PD3',
        'D4': 'PD4',
        'D5': 'PD5',
        'D6': 'PD6',
        'D7': 'PD7',
        'D8': 'PB0',
        'D9': 'PB1',
        'D10': 'PB2',
        'D11': 'PB3',
        'D12': 'PB4',
        'D13': 'PB5',
        'A0': 'PC0',
        'A1': 'PC1',
        'A2': 'PC2',
        'A3': 'PC3',
        'A4': 'PC4',
        'A5': 'PC5',
    }

    DATA_MAPPING = {
    }

    def __init__(self, name, communicator, address, description=''):
        super().__init__(name, description)
        assert isinstance(communicator, IArduinoCommunicator)
        self.__communicator = communicator
        self.__address = address
        self.__status = 'Unknown'

    def get_io_list(self):
        io_list = {'inputs': self.__input_list, 'outputs': self.__output_list}
        return io_list

    def get_status(self):
        return self.__status

    def get_output(self, name):
        assert name in self.__output_list
        return self.__output_list[name]

    def get_input(self, name):
        assert name in self.__input_list
        return self.__input_list[name]

    def add_input(self, type, port, name, options):
        assert port not in self.__used_ports

        if type == 'Analog':
            self.__add_setup_analog_port()
        elif type == 'Digital':
            self.__setup_digital_input(port, name, options)
        elif type == 'Counter':
            self.__setup_counter_input(port, name, options)

    def add_output(self, type, port, name, options):
        # Todo: Implement function
        pass

    def get_error_message(self):
        return 'Not implemented'

    def synchronize(self):
        return 0

    def __add_setup_analog_port(self, port, name, options):
        assert port in self.ANALOG_INPUT_MAPPING
        # Todo: Implement the rest.

    def __setup_digital_input(self, port, name, options):
        new_input = ArduinoDigitalInput(name, port, self.__communicator)
        self.__communicator.send_command(self.__address, 0x00, 0x00)
        self.__input_list[name] = new_input

    def __setup_counter_input(self, port, name, options):
        # Todo: Implement function
        pass