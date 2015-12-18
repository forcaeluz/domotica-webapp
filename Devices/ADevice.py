from Devices.IDevice import IDevice


class ADevice(IDevice):

    def __init__(self, name, description=''):
        self._dev_name = name
        self._description = description

    def get_description(self):
        return self._description

    def get_name(self):
        return self._dev_name

    def set_description(self, description):
        self._description = description

    def set_name(self, name):
        self._dev_name = name
