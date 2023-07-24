from datetime import datetime
from time import sleep, mktime
from requests import get, post, patch
from pytz import utc

from lib.pocketbase import PocketBase

from env import DEVICE


class Device:
    def __init__(self, tick_rate: int) -> None:
        print("-> Current device:", DEVICE)
        self.tick_rate = tick_rate
        self.sleep = sleep

        self.name = DEVICE
        self.id = None # This value is set by the test
        self.pb = PocketBase(get, post, patch, mktime)

    def get_current_time(self) -> int:
        return int(datetime.now(utc).timestamp())

