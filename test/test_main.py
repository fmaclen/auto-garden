import unittest
from unittest.mock import MagicMock, patch

from testboi import TestBoi
testboi = TestBoi()

from main import AutoGarden, TICK_RATE_IN_S
from lib.device import Device


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testboi.pocketbase_reset()
        testboi.pocketbase_start()

    @classmethod
    def tearDownClass(cls):
        testboi.pocketbase_stop()

    @patch.object(AutoGarden, "setup_pots", return_value=None)
    @patch.object(AutoGarden, "loop", return_value=None)
    @patch.object(Device, "__init__", return_value=None)
    def test_auto_garden_init(self, mock_device_init, mock_loop, mock_setup_pots):
        self.auto_garden = AutoGarden()
        mock_device_init.assert_called_once_with(TICK_RATE_IN_S)
        mock_setup_pots.assert_called_once()
        mock_loop.assert_called_once()

    def test_no_pots(self):
        try:
            self.auto_garden = AutoGarden()
        except Exception as e:
            self.assertEqual("No pots to irrigate", str(e))

    @patch.object(AutoGarden, "setup_pots")
    def test_irrigation_loop(self, mock_setup_pots):
        mock_pot = MagicMock()
        mock_setup_pots.return_value = [mock_pot, mock_pot]
        self.auto_garden = AutoGarden()
        self.assertEqual(mock_pot.update.call_count, 2)


if __name__ == '__main__':
    unittest.main()
