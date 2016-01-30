from Devices.ADevice import ADevice
from Communicators.IArduinoCommunicator import IArduinoCommunicator


class Arduino(ADevice):
    """
    The Arduino is one of the supported devices in the web application. In the domotica project there is always one
    Arduino connected to the Raspberry-pi. It can be used to connect to I2C sensors, read analog or digital inputs,
    dim lights or control digital outputs, depending on the connected hardware.
    """

    def __init__(self, communicator, name, description=''):
        """
        In the constructor, we require access to a communication device. We also need to specify a name and description
        for the Device.

        :param communicator: A communication device. Used but not owned by the Arduino, as it could be shared among
        other devices.
        :param name: A name for the device being created. Used to identify devices.
        :param description: A description for the device.
        """
        super().__init__(name, description)
        assert (isinstance(communicator, IArduinoCommunicator))
        self.__communicator = communicator

    def get_io_list(self):
        return super().get_io_list()

    def get_output(self, name):
        super().get_output(name)

    def get_input(self, name):
        super().get_input(name)

    def get_status(self):
        return super().get_status()

    def add_digital_output(self, name, description, pin):
        """
        Create a digital output, and also send the configuration command to the Arduino.
        :param name: A string with the name for the digital output.
        :param description: A string with the description for the digital output.
        :param pin: A string specifying the pin of the Arduino that should be used.
        :return: The created digital output, if creation was successful. It should be an implementation of the
        IDigitalOutput interface.
        """
        # TODO: Implement function
        pass

    def add_digital_input(self, name, description, pin):
        """
        Create a digital input, and also send the configuration command to the Arduino.
        :param name: A string with the name for the digital input.
        :param description: A string with the description for the digital input.
        :param pin: A string specifying the pin of the Arduino that should be used.
        :return: The created digital output. It should be an implementation of the IDigitalInput interface.
        """
        # TODO: Implement function
        pass

    def __request_status(self):
        # TODO: Implement the function
        pass

    def __setup_digital_output(self):
        # TODO: Implement the function
        pass

    def __setup_digital_input(self):
        # TODO: Implement the function
        pass