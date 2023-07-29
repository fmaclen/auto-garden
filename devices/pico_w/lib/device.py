import network
from time import sleep, mktime, gmtime
from urequests import get, post, patch
from machine import RTC, Pin

from lib.pocketbase import PocketBase
from lib.time_math import TimeMath

from env import DEVICE, POCKETBASE_DEVICE_ID, WIFI_SSID, WIFI_PASSWORD


class Device:
    def __init__(self, tick_rate: int) -> None:
        print("-> Current device:", DEVICE, POCKETBASE_DEVICE_ID)
        self.name = DEVICE
        self.tick_rate = tick_rate
        self.sleep = sleep
        self.connect_to_wifi()

        self.id = POCKETBASE_DEVICE_ID
        self.pb = PocketBase(get, post, patch, mktime)

        self.time_math = TimeMath()
        self.rtc = RTC()
        self.sync_clock()

    def connect_to_wifi(self) -> None:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # Wait for connect or fail
        wait = 10
        while wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            wait -= 1
            print('-> WiFi: waiting for connection...')
            sleep(self.tick_rate)

        # Handle connection error
        if wlan.status() != 3:
            print(wlan.status())
            raise RuntimeError('-> WiFi: Connection failed')
        else:
            print('-> WiFi: Connected')
            print('-> WiFi: IP', wlan.ifconfig()[0])

    def sync_clock(self) -> None:
        # Get the current time from PocketBase
        datetime_str = self.pb.get_time() # "2023-07-17 15:06:57.160Z"

        # Set the RTC time
        datetime_tuple = self.time_math.datetime_str_to_tuple(datetime_str)
        # Trim the last digit of the tuple since it's not supported by `RTC.datetime()`
        self.rtc.datetime(datetime_tuple[:8])

    def get_current_time(self) -> int:
        # Convert GMT tuple to timestamp
        timestamp = mktime(gmtime())
        return int(timestamp)

    def handle_system_error(self, error: str) -> None:
        print("-> Error:", error)
        # Turn on the onboard LED to indicate an error
        while True:
            Pin("LED", Pin.OUT).toggle()

            # Only run the loop once in tests
            if self.name == "Greenhouse (Test)": break

            sleep(1)
