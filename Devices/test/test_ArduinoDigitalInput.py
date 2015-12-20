import unittest
from unittest.mock import MagicMock
from Devices.ArduinoDigitalInput import ArduinoDigitalInput
from Hardware.IArduinoCommunicator import IArduinoCommunicator


class TestArduinoDigitalInput(unittest.TestCase):
    INPUT_NAME = 'Input 1'
    INPUT_PORT = 'D0'
    INPUT_ADDRESS = 0x10

    mock_comm = IArduinoCommunicator()

    def test_constructor(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)

        self.assertEqual(m_input.get_type(), 'ArduinoDigitalInput')
        self.assertEqual(m_input.get_name(), self.INPUT_NAME)

    def test_set_name(self):
        m_input = ArduinoDigitalInput('Wrong name', self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)

        m_input.set_name(self.INPUT_NAME)
        self.assertEqual(m_input.get_name(), self.INPUT_NAME)

    def test_enable(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        m_input.enable()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x01, 0x01)
        self.assertTrue(m_input.is_enabled())

    def test_disable(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        m_input.enable()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x01, 0x01)
        m_input.disable()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x01, 0x00)
        self.assertFalse(m_input.is_enabled())

    def test_enable_pullup(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        m_input.enable_pullup()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x02, 0x01)

    def test_disable_pullup(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        m_input.disable_pullup()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x02, 0x00)

    def test_disable_pullup_when_enabled(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        m_input.enable()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x01, 0x01)
        self.assertTrue(m_input.is_enabled())
        self.assertRaises(AssertionError, lambda: m_input.disable_pullup())

    def test_enable_pullup_when_enabled(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        m_input.enable()
        comm.send_command.assert_called_with(self.INPUT_ADDRESS, 0x01, 0x01)
        self.assertTrue(m_input.is_enabled())
        self.assertRaises(AssertionError, lambda: m_input.enable_pullup())

    def test_get_value(self):
        m_input = ArduinoDigitalInput(self.INPUT_NAME, self.INPUT_PORT,
                                      self.INPUT_ADDRESS, self.mock_comm)
        comm = self.mock_comm
        comm.send_command = MagicMock(return_value=0)
        comm.request_data = MagicMock(return_value=1)
        m_input.enable()
        assert m_input.is_enabled(), 'Test precondition'
        self.assertEqual(1, m_input.get_value())
        comm.request_data.assert_called_with(self.INPUT_ADDRESS, 0x00)


if __name__ == '__main__':
    unittest.main()
