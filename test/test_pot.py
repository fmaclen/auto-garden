from time import mktime, sleep
from requests import get, post, patch as request_patch
import unittest
from unittest.mock import MagicMock, patch as patch

from testboi import TestBoi
testboi = TestBoi()

from lib.pocketbase import PocketBase
from lib.device import Device
from lib.device_io import DeviceIO
from lib.pot import Pot
from env import DEVICE

NAME = "Strawberry (Test)"
MOISTURE_BUFFER_SIZE = 10
MOISTURE_LOW = 15
MOISTURE_HIGH = 80
MOISTURE_SENSOR_DRY = 60000
MOISTURE_SENSOR_WET = 25000
MOISTURE_SENSOR_PIN = 28
PUMP_MAX_ATTEMPTS = 3
PUMP_DURATION_IN_S = 1
PUMP_FREQUENCY_IN_S = 1
PUMP_RELAY_PIN = 16


class TestPot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testboi.pocketbase_reset()
        testboi.pocketbase_start()

        cls.pb = PocketBase(get, post, request_patch, mktime)
        cls.device_record = cls.pb.create_device(DEVICE)
        cls.pot_record = cls.pb.create_pot(
            cls.device_record["id"],
            NAME,
            MOISTURE_LOW,
            MOISTURE_HIGH,
            MOISTURE_SENSOR_DRY,
            MOISTURE_SENSOR_WET,
            MOISTURE_SENSOR_PIN,
            PUMP_MAX_ATTEMPTS,
            PUMP_DURATION_IN_S,
            PUMP_FREQUENCY_IN_S,
            PUMP_RELAY_PIN
        )

    @classmethod
    def tearDownClass(cls):
        testboi.pocketbase_stop()

    def test_init(self):
        pot = self.new_pot()
        self.assertEqual(pot.device.name, self.device_record["name"])
        self.assertEqual(pot.id, self.pot_record["id"])
        self.assertEqual(pot.name, self.pot_record["name"])
        self.assertEqual(pot.moisture_previous, None)
        self.assertEqual(pot.moisture_current, None)
        self.assertEqual(pot.moisture_buffer, [None]*10)
        self.assertEqual(pot.moisture_low, self.pot_record["moisture_low"])
        self.assertEqual(pot.moisture_high, self.pot_record["moisture_high"])
        self.assertEqual(pot.moisture_sensor_dry, self.pot_record["moisture_sensor_dry"])
        self.assertEqual(pot.moisture_sensor_wet, self.pot_record["moisture_sensor_wet"])
        self.assertEqual(pot.irrigation_event, None)
        self.assertEqual(pot.is_first_irrigation_attempt, True)
        self.assertEqual(pot.pump_max_attempts, self.pot_record["pump_max_attempts"])
        self.assertEqual(pot.pump_duration_in_s, self.pot_record["pump_duration_in_s"])
        self.assertEqual(pot.pump_frequency_in_s, self.pot_record["pump_frequency_in_s"])

    @patch.object(Pot, 'read_moisture')
    @patch.object(Pot, 'try_to_irrigate')
    def test_update(self, mock_try_to_irrigate, mock_read_moisture):
        pot = self.new_pot()
        mock_read_moisture.assert_not_called()
        mock_try_to_irrigate.assert_not_called()

        pot.update()
        mock_read_moisture.assert_called_once()
        mock_try_to_irrigate.assert_called_once()

    @patch.object(DeviceIO, "read_moisture_sensor", return_value=MOISTURE_SENSOR_DRY)
    @patch.object(Pot, "set_moisture")
    def test_read_moisture(self, mock_set_moisture, mock_read_moisture_sensor):
        pot = self.new_pot()

        # Reading the moisture 9 more times to fill the buffer
        for i in range(10):
            pot.read_moisture()
            if (i+1) % 10 == 0:  # checking for change every 10th reading
                self.assertEqual(pot.moisture_current, 0)
                mock_set_moisture.assert_called_once_with(0)
            else:
                self.assertNotEqual(pot.moisture_current, 0)
                mock_set_moisture.assert_not_called()
        
        # Let's now simulate a change in the moisture reading
        mock_read_moisture_sensor.return_value = MOISTURE_SENSOR_WET
        pot.read_moisture()
        self.assertNotEqual(pot.moisture_current, 0)

        # Simulating an exception scenario
        mock_read_moisture_sensor.return_value = None
        with self.assertRaises(Exception):
            pot.read_moisture()

        # Check that moisture readings out of range are ignored
        mock_get_moisture_percentage = MagicMock()
        pot.get_moisture_percentage = mock_get_moisture_percentage

        mock_read_moisture_sensor.return_value = pot.moisture_sensor_wet - 1
        pot.read_moisture()
        mock_get_moisture_percentage.assert_not_called()

        mock_read_moisture_sensor.return_value = pot.moisture_sensor_dry + 1
        pot.read_moisture()
        mock_get_moisture_percentage.assert_not_called()
        

    def test_get_moisture_percentage(self):
        pot = self.new_pot()
        self.assertEqual(pot.get_moisture_percentage(MOISTURE_SENSOR_DRY), 0)
        self.assertEqual(pot.get_moisture_percentage(MOISTURE_SENSOR_WET), 100)
        self.assertEqual(pot.get_moisture_percentage(20000), 100)
        self.assertEqual(pot.get_moisture_percentage(42500), 50)
        self.assertEqual(pot.get_moisture_percentage(70000), 0)

    def test_set_moisture(self):
        pot = self.new_pot()
        moisture_record = self.pb.get_last_moisture(pot.id)
        self.assertEqual(moisture_record, [])

        pot.set_moisture(25)
        moisture_record = self.pb.get_last_moisture(pot.id)
        self.assertEqual(moisture_record[0]["level"], 25)
        self.assertEqual(moisture_record[0]["pot"], pot.id)

        # Check if we are indeed getting the most recent moisture record
        pot.set_moisture(50)
        moisture_record = self.pb.get_last_moisture(pot.id)
        self.assertEqual(moisture_record[0]["level"], 50)
        self.assertEqual(moisture_record[0]["pot"], pot.id)

    @patch.object(Pot, "irrigate", return_value=None)
    def test_try_to_irrigate(self, mock_irrigate):
        pot = self.new_pot()
        
        # Test if moisture_buffer is None
        pot.moisture_buffer = [None] * MOISTURE_BUFFER_SIZE
        pot.try_to_irrigate()
        mock_irrigate.assert_not_called()

        # Test if moisture_previous is None
        pot.moisture_buffer = [10] * MOISTURE_BUFFER_SIZE
        pot.moisture_previous = None
        pot.try_to_irrigate()
        mock_irrigate.assert_not_called()

        # Test if moisture_current is None
        pot.moisture_previous = 50
        pot.moisture_current = None
        pot.try_to_irrigate()
        mock_irrigate.assert_not_called()

        # Test if moisture_current and moisture_previous are equal and is_first_irrigation_attempt is False
        pot.moisture_current = 50
        pot.is_first_irrigation_attempt = False
        pot.try_to_irrigate()
        mock_irrigate.assert_not_called()

        # Test if moisture_current is below moisture_low
        pot.moisture_current = pot.moisture_low - 10
        self.assertEqual(pot.irrigation_event, None)

        # Pump 1
        pot.try_to_irrigate()
        mock_irrigate.assert_called_once()
        self.assertEqual(pot.irrigation_event["status"], "in_progress")
        self.assertEqual(pot.irrigation_event["pumps"], pot.pump_max_attempts - 2)

        # Another pump attempt too fast
        pot.moisture_current = pot.moisture_high - 50
        pot.try_to_irrigate()
        mock_irrigate.assert_called_once()
        self.assertEqual(pot.irrigation_event["status"], "in_progress")
        self.assertEqual(pot.irrigation_event["pumps"], pot.pump_max_attempts - 2)
        
        # Pump 2
        sleep(pot.pump_frequency_in_s + 0.1)
        pot.moisture_current = pot.moisture_high - 25
        pot.try_to_irrigate()
        self.assertEqual(mock_irrigate.call_count, pot.pump_max_attempts -1)
        self.assertEqual(pot.irrigation_event["status"], "in_progress")
        self.assertEqual(pot.irrigation_event["pumps"], pot.pump_max_attempts -1)

        # Last pump attempt
        sleep(pot.pump_frequency_in_s + 0.1)
        pot.moisture_current = pot.moisture_high - 5
        pot.try_to_irrigate()
        self.assertEqual(mock_irrigate.call_count, pot.pump_max_attempts)
        self.assertEqual(pot.irrigation_event["status"], "in_progress")
        self.assertEqual(pot.irrigation_event["pumps"], pot.pump_max_attempts)

        # No more pumps needed
        sleep(pot.pump_frequency_in_s + 0.1)
        pot.moisture_current = pot.moisture_high
        pot.try_to_irrigate()
        last_irrigation_record = pot.device.pb.get_last_irrigation(pot.id)[0]
        self.assertEqual(mock_irrigate.call_count, pot.pump_max_attempts)
        self.assertEqual(pot.irrigation_event, None)
        self.assertEqual(last_irrigation_record["status"], "success")
        self.assertEqual(last_irrigation_record["pumps"], pot.pump_max_attempts)

        # No error and no irrigation needed on first attempt
        pot = self.new_pot()
        mock_irrigate.reset_mock()
        pot.moisture_buffer = [pot.moisture_low] * MOISTURE_BUFFER_SIZE
        pot.moisture_previous = pot.moisture_low
        pot.moisture_current = pot.moisture_low + 1
        pot.irrigation_event = None
        pot.is_first_irrigation_attempt = True

        pot.try_to_irrigate()
        mock_irrigate.assert_not_called()
        self.assertEqual(pot.irrigation_event, None)
        self.assertEqual(pot.is_first_irrigation_attempt, False)

        # Fail at irrigating
        pot = self.new_pot()
        mock_irrigate.reset_mock()
        pot.moisture_buffer = [pot.moisture_low] * MOISTURE_BUFFER_SIZE
        pot.moisture_previous = pot.moisture_low
        pot.moisture_current = pot.moisture_low - 1
        pot.is_first_irrigation_attempt = False
        for _ in range(pot.pump_max_attempts + 1):
            pot.try_to_irrigate()
            sleep(pot.pump_frequency_in_s + 0.1)
        self.assertNotEqual(pot.irrigation_event["id"], last_irrigation_record["id"])
        self.assertEqual(pot.irrigation_event["status"], "error")
        self.assertEqual(pot.irrigation_event["pumps"], pot.pump_max_attempts)

        # If the app restarts and the previous error was never cleared, we still
        # don't want to irrigate
        pot = self.new_pot()
        mock_irrigate.reset_mock()
        pot.moisture_buffer = [pot.moisture_low] * MOISTURE_BUFFER_SIZE
        pot.moisture_previous = pot.moisture_low
        pot.moisture_current = pot.moisture_low
        pot.is_first_irrigation_attempt = True
        self.assertEqual(pot.irrigation_event, None)

        pot.try_to_irrigate()
        mock_irrigate.assert_not_called()
        self.assertEqual(pot.irrigation_event["status"], "error")
        self.assertEqual(pot.irrigation_event["pumps"], pot.pump_max_attempts)
        self.assertEqual(pot.is_first_irrigation_attempt, False)

    def test_irrigate(self):
        mock_sleep = MagicMock()
        mock_toggle_pump = MagicMock()

        pot = self.new_pot()
        pot.device.sleep = mock_sleep
        pot.device_io.toggle_pump = mock_toggle_pump
        mock_sleep.assert_not_called()
        mock_toggle_pump.assert_not_called()

        pot.irrigate()
        mock_sleep.assert_called_once_with(pot.pump_duration_in_s)
        self.assertEqual(mock_toggle_pump.call_count, 2)

    def new_pot(self) -> Pot:
        return Pot(
            Device(2),
            self.pot_record["id"],
            self.pot_record["name"],
            self.pot_record["moisture_low"],
            self.pot_record["moisture_high"],
            self.pot_record["moisture_sensor_dry"],
            self.pot_record["moisture_sensor_wet"],
            self.pot_record["moisture_sensor_pin"],
            self.pot_record["pump_max_attempts"],
            self.pot_record["pump_duration_in_s"],
            self.pot_record["pump_frequency_in_s"],
            self.pot_record["pump_relay_pin"]
        )

if __name__ == '__main__':
    unittest.main()
