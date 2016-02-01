from logging import getLogger

from Communicators.IArduinoCommunicator import IArduinoCommunicator, ArduinoCommunicationError, ArduinoRepliedError
from Devices.IDigitalInput import IDigitalInput


class ArduinoDigitalInput(IDigitalInput):
    """
    The ArduinoDigitalInput is an implementation of the IDigitalInput for the Arduino.
    """
    def __init__(self, communication_device, object_address, name, description):
        """
        Constructor.
        :param communication_device: An IArduinoCommunicator used to communicate with the Arduino.
        :param object_address: Address of this digital input.
        :param name:
        :param description:
        """
        assert isinstance(communication_device, IArduinoCommunicator)
        self.__logger = getLogger('application.digital_io')
        self.__name = name
        self.__description = description
        self.__comm_device = communication_device
        self.__pull_up_enabled = False
        self.__address = object_address

    def is_pull_up_enabled(self):
        return self.__pull_up_enabled

    def disable_pull_up(self):
        """
        This function tries to disable the pull-up resistor from the ArduinoDigitalInput.
        In case of errors, they are logged, but nothing more is done. The user can check the success of the operation
        by checking is_pull_up_enabled().
        """
        try:
            self.__comm_device.write_to_object(self.__address, self.__PULL_UP_SUB_ADDRESS, 0)
        except ArduinoCommunicationError as e:
            self.__logger.warning('Unable to communicate with the Arduino to disable the pull-up from %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        except ArduinoRepliedError as e:
            self.__logger.warning('Arduino replied with an error message when disabling pull-up from %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        except Exception as e:
            self.__logger.warning('Exception raised when disabling pull-up on %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        else:
            self.__pull_up_enabled = False

    def enable_pull_up(self):
        """
        This function tries to enable the pull-up resistor from the ArduinoDigitalInput.
        In case of errors, they are logged, but nothing more is done. The user can check the success of the operation
        by checking is_pull_up_enabled().
        """
        try:
            self.__comm_device.write_to_object(self.__address, self.__PULL_UP_SUB_ADDRESS, 1)
        except ArduinoCommunicationError as e:
            self.__logger.warning('Unable to communicate with the Arduino to enable the pull-up from %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        except ArduinoRepliedError as e:
            self.__logger.warning('Arduino replied with an error message when enabling pull-up from %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        except Exception as e:
            self.__logger.warning('Exception raised when enabling pull-up on %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        else:
            self.__pull_up_enabled = True

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__class__.__name__

    def get_value(self):
        """
        This function tries to read the current state of the Digital Input. In case of failure, the exceptions are
        logged.
        :return:
        """
        try:
            return_value = self.__comm_device.request_object_data(self.__address, self.__DATA_SUB_ADDRESS)
        except ArduinoCommunicationError as e:
            self.__logger.warning('Unable to communicate with the Arduino when reading DI: %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        except ArduinoRepliedError as e:
            self.__logger.warning('Arduino replied with an error message when reading DI: %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        except Exception as e:
            self.__logger.warning('Exception raised when reading DI %s', self.__name)
            self.__logger.warning('Exception: %s', e.__str__())
        else:
            return return_value

    __PULL_UP_SUB_ADDRESS = 0x03
    __DATA_SUB_ADDRESS = 0x00
