class IDevice:

    def get_name(self):
        """
        Returns the name of the device
        :rtype: str
        """
        pass

    def set_name(self, name):
        """
        Gives the device a new name.
        :param name: New name for the device.
        """
        pass

    def get_description(self):
        """
        Returns the description given to the device.
        :rtype: str
        """
        pass

    def set_description(self, description):
        """
        Changes the description of the device.
        :param description: New description for the device.
        """
        pass

    def get_status(self):
        """
        Function to get the status of the device.
        :return The current status of the device. (Unknown, online, error, etc).
        :rtype: str
        """
        pass

    def get_io_list(self):
        """
        Function to get the list of inputs and outputs available on the device.
        :return A dictionary with inputs and outputs of the device.
        :rtype: dict
        """
        pass

    def get_output(self, name):
        """
        :param name: Name of the Output.
        :rtype: IOutput
        :return An IOutput object
        """
        pass

    def get_input(self, name):
        """
        :param name: Name of the Input.
        :rtype: IInput
        """
        pass
