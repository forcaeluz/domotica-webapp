import unittest

from Communicators.IArduinoCommunicator import IArduinoCommunicator
from Devices.Arduino import Arduino


class TestArduino(unittest.TestCase):

    def setUp(self):
        self.DEVICE_NAME = 'Device1'
        self.DEVICE_DESCRIPTION = 'This is a test device'
        self.mock_comm = IArduinoCommunicator()

    def test_constructor_inheritance(self):
        my_device = Arduino(self.mock_comm, self.DEVICE_NAME, self.DEVICE_DESCRIPTION)
        self.assertEqual(self.DEVICE_NAME, my_device.get_name())
        self.assertEqual(self.DEVICE_DESCRIPTION, my_device.get_description())

    @unittest.skip('Not implemented yet')
    def test_add_digital_input(self):
        """
        Adding a digital input, with valid parameters should return a valid IDigitalInput, and send the right commands
         to the Arduino, using the mock_communicator.
        """
        self.assertTrue(False, 'Test not yet implemented')

    @unittest.skip('Not implemented yet')
    def test_add_digital_input_invalid_pin(self):
        """
        When adding a digital input to a pin which cannot be used as digital input, an error should be given.
        """
        self.assertTrue(False, 'Test not yet implemented')

    @unittest.skip('Not implemented yet')
    def test_add_digital_input_used_pin(self):
        """
        When adding a digital input to a pin that is already being used an error should be given.
        """
        self.assertTrue(False, 'Test not yet implemented')

    @unittest.skip('Not implemented yet')
    def test_add_digital_input_twice(self):
        """
        When adding a digital input twice the second time should return the input created at the first
        attempt, without throwing an error. Note that name and description should be the same.
        """
        self.assertTrue(False, 'Test not yet implemented')


if __name__ == '__main__':
    unittest.main()
