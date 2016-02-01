class IArduinoCommunicator:
    """
    The description of the interface to communicate with the Arduino. The interface describes how to control
    and read IO of the Arduino. Another interface should be used to describe how to read debug messages
    produced by the Arduino.

    The communication protocol is very similar to the CanOpen protocol. In the Arduino, "Objects" are the data
    containers. You can write to an object, or read from an object. An object has an address and a sub-address,
    and its functionality is described in the Arduino documentation.

    """

    def write_to_object(self, address, sub_address, data):
        """
        Used to send data to the Arduino. This function is blocking, and waits on the
        reply of the Arduino.

        :param address: Object's address.
        :param sub_address: Object's sub-address.
        :param data: Object's data.
        """
        pass

    def request_object_data(self, address, sub_address):
        """
        Used to send data to the Arduino. This function is blocking, and waits on the
        reply of the Arduino.
        :param address: Object's address.
        :param sub_address: Object's sub-address.
        :return: The data in the specified object.
        """
        pass

    def add_observer(self, address, sub_address, observer):
        """
        Used to subscribe to automatic updates of the Arduino. Enabling automatic updates is done by
        writing to objects, as described in the Arduino documentation. This function is only used to
        assign a callback to the updates of a specific object.
        :param address: Object's address.
        :param sub_address: Object's sub-address.
        :param observer:
        """
        pass


class ArduinoCommunicationError(Exception):
    """

    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ArduinoRepliedError(Exception):
    """

    """
    def __init__(self, address, sub_address, value, error):
        self.address = address
        self.sub_address = sub_address
        self.value = value
        self.error = error
