from Devices.IInput import IInput


class ArduinoCounterInput(IInput):

    def __init__(self):
        super().__init__()

    def get_type(self):
        super().get_type()

    def get_value(self):
        super().get_value()

    def set_name(self, name):
        super().set_name(name)

    def get_name(self):
        super().get_name()

# Private members

    __SUB_ADDRESSES = dict(
        DATA=0x00,
        ENABLED=0x01,
        PULL_UP_ENABLED=0x02,
        COUNTER_TYPE=0x03
    )