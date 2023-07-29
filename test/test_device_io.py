import sys
import unittest
from unittest.mock import patch, MagicMock

from testboi import TestBoi
testboi = TestBoi()

class TestDeviceIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testboi.pocketbase_reset()
        testboi.pocketbase_start()

        cls.rpi_mock = MagicMock()
        sys.modules['RPi'] = cls.rpi_mock
        cls.gpio_mock = MagicMock()
        sys.modules['RPi.GPIO'] = cls.gpio_mock
        cls.board_mock = MagicMock()
        sys.modules['board'] = cls.board_mock
        cls.busio_mock = MagicMock()
        sys.modules['busio'] = cls.busio_mock
        cls.adafruit_ads1x15_mock = MagicMock()
        sys.modules['adafruit_ads1x15'] = cls.adafruit_ads1x15_mock
        cls.ads1115_mock = MagicMock()
        sys.modules['adafruit_ads1x15.ads1115'] = cls.ads1115_mock
        cls.analog_in_mock = MagicMock()
        sys.modules['adafruit_ads1x15.analog_in'] = cls.analog_in_mock

        cls.moisture_sensor_pin = 2
        cls.pump_relay_pin = 16

    @classmethod
    def tearDownClass(cls):
        testboi.pocketbase_stop()

    def test_device_io_as_test(self):
        from lib.device_io import DeviceIO as DeviceIOTest
        device_io = DeviceIOTest(self.moisture_sensor_pin, self.pump_relay_pin)
        self.assertEqual(device_io.read_moisture_sensor() == 65535, True)
        self.assertEqual(device_io.toggle_pump() == None, True)
        self.assertEqual(device_io.cleanup() == None, True)

    def test_device_io_in_pi_4(self):
        from devices.pi_4.lib.device_io import DeviceIO as DeviceIOPi4
        self.analog_in_mock.AnalogIn.return_value.value = 65535

        device_io = DeviceIOPi4(self.moisture_sensor_pin, self.pump_relay_pin)

        # Moisture sensor
        self.busio_mock.I2C.assert_called_once_with(self.board_mock.SCL, self.board_mock.SDA)
        self.ads1115_mock.ADS1115.assert_called_once_with(self.busio_mock.I2C())
        self.analog_in_mock.AnalogIn.assert_called_once_with(self.ads1115_mock.ADS1115(), self.moisture_sensor_pin)
        self.assertEqual(device_io.read_moisture_sensor(), 65535)

        # Pump relay
        device_io.gpio.setmode.assert_called_once_with(device_io.gpio.BCM)
        device_io.gpio.setup.assert_called_once_with(device_io.pump_relay_pin, device_io.gpio.OUT)
        device_io.gpio.output.assert_called_once_with(device_io.pump_relay_pin, device_io.gpio.HIGH)
        self.assertEqual(len(device_io.gpio.method_calls), 3)
        self.assertEqual(device_io.gpio.output.call_count, 1)
        self.assertEqual(device_io.pump_relay_pin, self.pump_relay_pin)

        device_io.gpio.input.return_value = False
        self.assertEqual(device_io.toggle_pump() == None, True)
        self.assertEqual(device_io.gpio.output.call_count, 2)
        self.assertEqual(device_io.gpio.output.call_args_list[1][0][1], True)

        device_io.gpio.input.return_value = True
        device_io.toggle_pump()
        self.assertEqual(device_io.gpio.output.call_count, 3)
        self.assertEqual(device_io.gpio.output.call_args_list[2][0][1], False)

        self.assertEqual(device_io.cleanup() == None, True)
        self.assertEqual(device_io.gpio.cleanup.call_count, 1)

    @patch('machine.ADC', autospec=True)
    @patch('machine.Pin', autospec=True)
    @patch('machine.Pin.OUT', autospec=True)
    def test_device_io_in_pico_w(self, pin_out_mock, pin_mock, adc_mock):
        from devices.pico_w.lib.device_io import DeviceIO as DeviceIOPicoW
        adc_instance_mock = MagicMock()
        adc_instance_mock.read_u16.return_value = 65535
        adc_mock.return_value = adc_instance_mock

        device_io = DeviceIOPicoW(self.moisture_sensor_pin, self.pump_relay_pin)

        # Moisture sensor
        adc_mock.assert_called_once_with(self.moisture_sensor_pin)

        # Pump relay
        pin_mock.assert_called_once_with(self.pump_relay_pin, pin_out_mock)
        self.assertEqual(device_io.read_moisture_sensor(), 65535)
        adc_mock.return_value.read_u16.assert_called_once()
        self.assertEqual(device_io.toggle_pump() == None, True)
        pin_mock.return_value.toggle.assert_called_once()
        self.assertEqual(device_io.cleanup() == None, True)
        pin_mock.return_value.value.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()
