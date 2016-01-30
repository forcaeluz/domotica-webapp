from Devices.IInput import IInput


class IDigitalInput(IInput):
    def enable_pull_up(self):
        pass

    def disable_pull_up(self):
        pass

    def is_pull_up_enabled(self):
        pass
