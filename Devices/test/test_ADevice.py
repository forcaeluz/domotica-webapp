import unittest
from Devices.ADevice import ADevice


class TestADevice(unittest.TestCase):
    DEVICE_NAME = 'Device1'
    DEVICE_DESCRIPTION = 'This is a test device'
    EMPTY_DESCRIPTION = ''
    MODIFIED_NAME = 'Device2'
    MODIFIED_DESCRIPTION = 'This is another test device'

    def test_constructor(self):
        my_device = ADevice(self.DEVICE_NAME, self.DEVICE_DESCRIPTION)
        self.assertEqual(my_device.get_name(), self.DEVICE_NAME)
        self.assertEqual(my_device.get_description(), self.DEVICE_DESCRIPTION)

    def test_description_less_constructor(self):
        my_device = ADevice(self.DEVICE_NAME)
        self.assertEqual(my_device.get_name(), self.DEVICE_NAME)
        self.assertEqual(my_device.get_description(), self.EMPTY_DESCRIPTION)

    def test_set_name(self):
        my_device = ADevice(self.DEVICE_NAME, self.DEVICE_DESCRIPTION)
        my_device.set_name(self.MODIFIED_NAME)
        self.assertEqual(my_device.get_name(), self.MODIFIED_NAME)

    def test_set_description(self):
        my_device = ADevice(self.DEVICE_NAME, self.DEVICE_DESCRIPTION)
        my_device.set_description(self.MODIFIED_DESCRIPTION)
        self.assertEqual(my_device.get_description(), self.MODIFIED_DESCRIPTION)


if __name__ == '__main__':
    unittest.main()
