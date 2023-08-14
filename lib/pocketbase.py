from env import POCKETBASE_SERVER_URL, POCKETBASE_ADMIN_USERNAME, POCKETBASE_ADMIN_PASSWORD, POCKETBASE_DEVICE_ID


class PocketBase:
    def __init__(self, get, post, patch, mktime) -> None:
        self.id = POCKETBASE_DEVICE_ID
        self.get = get
        self.post = post
        self.patch = patch
        self.mktime = mktime
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_jwt()}"
        }

    def create_device(self, name: str):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/devices/records/"
        data = {
            "name": name,
        }
        response = self.post(url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Couldn't create 'Device'", response.status_code)

        return response.json()

    def create_pot(self, device_id: str, name: str, moisture_low: int, moisture_high: int, moisture_sensor_dry: int, moisture_sensor_wet: int, moisture_sensor_pin: int, pump_max_attempts: int, pump_duration_in_s: int, pump_frequency_in_s: int, pump_relay_pin: int):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/pots/records/"
        data = {
            "device": device_id,
            "name": name,
            "moisture_low": moisture_low,
            "moisture_high": moisture_high,
            "moisture_sensor_dry": moisture_sensor_dry,
            "moisture_sensor_wet": moisture_sensor_wet,
            "moisture_sensor_pin": moisture_sensor_pin,
            "pump_max_attempts": pump_max_attempts,
            "pump_duration_in_s": pump_duration_in_s,
            "pump_frequency_in_s": pump_frequency_in_s,
            "pump_relay_pin": pump_relay_pin,
        }
        response = self.post(url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Couldn't create 'Pot'", response.status_code)

        return response.json()

    def get_pots(self):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/pots/records/?filter=(device.id='{self.id}')"
        response = self.get(url, headers=self.headers)

        if response.status_code != 200:
            raise RuntimeError(
                "-> PocketBase: Couldn't retrieve 'Pots;'", response.status_code)

        return response.json()["items"]

    def create_moisture(self, pot_id: str, level):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/moistures/records/"
        data = {
            "pot": pot_id,
            'level': level
        }
        response = self.post(url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Couldn't create moisture", response.status_code)

        return response.json()


    def get_last_moisture(self, pot_id: str):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/moistures/records/?perPage=1&sort=-created&filter=(pot.id='{pot_id}')"
        response = self.get(url, headers=self.headers)

        if response.status_code != 200:
            raise RuntimeError(
                "-> PocketBase: Couldn't retrieve 'Moisture'", response.status_code)

        return response.json()["items"]

    def get_last_irrigation(self, pot_id: str):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/irrigations/records/?perPage=1&sort=-created&filter=(pot.id='{pot_id}')"
        response = self.get(url, headers=self.headers)

        if response.status_code != 200:
            raise RuntimeError(
                "-> PocketBase: Couldn't retrieve Pots", response.status_code)

        return response.json()["items"]

    def create_irrigation(self, pot_id: str, status, pumps: int):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/irrigations/records/"
        data = {
            "pot": pot_id,
            'status': status,
            'pumps': pumps,
        }
        response = self.post(url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Couldn't create irrigation", response.status_code)

        return response.json()

    def update_irrigation(self, status, pumps: int, id: str):
        url = f"{POCKETBASE_SERVER_URL}/api/collections/irrigations/records/{id}"
        data = {
            'status': status,
            'pumps': pumps,
        }
        response = self.patch(url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Couldn't update irrigation", response.status_code)

        return response.json()

    def get_time(self):
        url = f"{POCKETBASE_SERVER_URL}/api/settings"
        response = self.get(url, headers=self.headers)
        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Couldn't retrieve settings", response.status_code)

        url = f"{POCKETBASE_SERVER_URL}/api/logs/requests/?perPage=1&sort=-created"
        response = self.get(url, headers=self.headers)
        if response.status_code != 200 and len(response.json()["items"]) != 1:
            raise RuntimeError("-> PocketBase: Couldn't retrieve time", response.status_code)

        return response.json()["items"][0]["created"]

    def get_jwt(self) -> str:
        url = f"{POCKETBASE_SERVER_URL}/api/admins/auth-with-password/"
        data = {
            "identity": POCKETBASE_ADMIN_USERNAME,
            'password': POCKETBASE_ADMIN_PASSWORD
        }
        response = self.post(url, headers={ "Content-Type": "application/json" }, json=data)

        if response.status_code != 200:
            raise RuntimeError("-> PocketBase: Invalid credentials", response.status_code)

        return response.json()["token"]

    def is_valid_jwt(self, external_jwt: str) -> bool:
        url = f"{POCKETBASE_SERVER_URL}/api/settings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": external_jwt # e.g. `Bearer aaaa.bbbb.cccc`
        }
        response = self.get(url, headers=headers)

        return response.status_code == 200
