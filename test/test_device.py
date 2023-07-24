import sys
import time
from datetime import datetime
from pytz import utc
import unittest
from unittest.mock import MagicMock, patch

from testboi import TestBoi
testboi = TestBoi()

from main import TICK_RATE_IN_S
from lib.time_math import TimeMath
from env import POCKETBASE_DEVICE_ID, WIFI_SSID, WIFI_PASSWORD

class TestDevice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testboi.pocketbase_reset()
        testboi.pocketbase_start()

        # Mocked libraries for Pico W
        cls.network_mock = MagicMock()
        sys.modules['network'] = cls.network_mock
        cls.machine_mock = MagicMock()
        sys.modules['machine'] = cls.machine_mock
        # `urequests` has the same API as `requests` so we don't need to mock it
        import requests
        sys.modules['urequests'] = requests

    @classmethod
    def tearDownClass(cls):
        testboi.pocketbase_stop()

    def test_device_as_test(self):
        from lib.device import Device as DeviceTest
        device = DeviceTest(TICK_RATE_IN_S)
        self.assertEqual(device.get_current_time() > 0, True)

    def test_device_in_pi_4(self):
        from devices.pi_4.lib.device import Device as DevicePi4
        device = DevicePi4(TICK_RATE_IN_S)
        self.assertEqual(device.get_current_time() > 0, True)

    @patch.object(time, 'mktime', return_value=int(datetime.now(utc).timestamp()))
    @patch.object(time, 'gmtime', return_value=(2023, 1, 2, 3, 4, 5, 6, 7, 8))
    @patch.object(TimeMath, 'datetime_str_to_tuple', return_value=(2023, 1, 2, 3, 4, 5, 6, 7))
    def test_device_in_pico_w(self, datetime_str_to_tuple_mock, gmtime_mock, mktime_mock):
        from devices.pico_w.lib.device import Device as DevicePicoW

        wlan_mock = MagicMock()
        wlan_mock.status.return_value = 3
        wlan_mock.ifconfig.return_value = ['192.168.1.1', '', '', '']
        self.network_mock.WLAN.return_value = wlan_mock

        rtc_mock = MagicMock()
        rtc_mock.datetime.return_value = (2021, 1, 1, 4, 0, 0, 0, 0) # Default Pico W RTC datetime
        self.machine_mock.RTC.return_value = rtc_mock

        device = DevicePicoW(TICK_RATE_IN_S)
        
        # Test __init__ method
        self.assertEqual(device.tick_rate, TICK_RATE_IN_S)
        
        # Test connect_to_wifi method
        self.network_mock.WLAN.assert_called_once()
        wlan_mock.active.assert_called_once_with(True)
        wlan_mock.connect.assert_called_once()
        self.assertEqual(wlan_mock.connect.call_args[0], (WIFI_SSID, WIFI_PASSWORD))
        self.assertEqual(wlan_mock.status.call_count, 3)
        self.assertEqual(device.id, POCKETBASE_DEVICE_ID)
        
        # Test sync_clock method
        datetime_str_to_tuple_mock.assert_called_once()
        args = rtc_mock.datetime.call_args[0][0]
        # Check we're passing a tuple of 8 integers
        self.assertEqual(isinstance(args, tuple) and len(args) == 8 and all(isinstance(val, int) for val in args), True)
        # Check the tuple is not the default Pico W RTC datetime
        self.assertNotEqual(args, (2021, 1, 1, 4, 0, 0, 0, 0))

        # Test connect_to_wifi method with failure
        wlan_mock.status.return_value = -1
        try:
            device.connect_to_wifi()
        except Exception as e:
            self.assertEqual("-> WiFi: Connection failed", str(e))

        # Test get_current_time method
        current_time = device.get_current_time()
        self.assertEqual(current_time > 0, True)
        self.assertEqual(isinstance(current_time, int), True)
        gmtime_mock.assert_called_once()
        mktime_mock.assert_called_once()

if __name__ == '__main__':
    unittest.main()
