from datetime import datetime
from time import sleep, mktime
from requests import get, post, patch
from pytz import utc

from lib.pocketbase import PocketBase

from env import DEVICE, POCKETBASE_DEVICE_ID


class Device:
    def __init__(self, tick_rate: int) -> None:
        print("-> Current device:", DEVICE)
        self.name = DEVICE
        self.tick_rate = tick_rate
        self.sleep = sleep

        self.id = POCKETBASE_DEVICE_ID
        self.pb = PocketBase(get, post, patch, mktime)

    def get_current_time(self) -> int:
        return int(datetime.now(utc).timestamp())

    def handle_system_error(self, error: str) -> None:
        print("-> Error:", error)

