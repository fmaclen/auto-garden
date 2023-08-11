try: from typing import List, Optional, Dict, Any
except: pass

from lib.device import Device
from lib.device_io import DeviceIO
from lib.time_math import TimeMath


class Pot:
    def __init__(
            self,
            device: Device,
            id: str,
            name: str,
            moisture_low: int,
            moisture_high: int,
            moisture_sensor_dry: int,
            moisture_sensor_wet: int,
            moisture_sensor_pin: int,
            pump_max_attempts: int,
            pump_duration_in_s: int,
            pump_frequency_in_s: int,
            pump_relay_pin: int,
        ) -> None:

        self.device = device
        self.id = id
        self.name = name
        self.device = device
        self.device_io = DeviceIO(moisture_sensor_pin, pump_relay_pin)
        self.time_math = TimeMath()

        self.moisture_previous: Optional[int] = None
        self.moisture_current: Optional[int] = None
        self.moisture_buffer: List[Optional[int]] = [None] * 10 # A list to keep the last 10 readings so we can smooth them
        self.moisture_low = moisture_low # It will only irrigate if the moisture value is avobe this low
        self.moisture_high = moisture_high # It will stop irrigating above this moisture value
        self.moisture_sensor_dry = moisture_sensor_dry # It will only irrigate if the moisture value is avobe this low
        self.moisture_sensor_wet = moisture_sensor_wet # It will stop irrigating above this moisture value

        self.irrigation_event: Optional[Dict[str, Any]] = None
        self.is_first_irrigation_attempt = True
        self.pump_max_attempts = pump_max_attempts # Max number of pumps per irrigation event
        self.pump_duration_in_s = pump_duration_in_s # How long will the pump remain on during irrigation
        self.pump_frequency_in_s = pump_frequency_in_s # How long to wait between pumps during an irrigation event

    def update(self) -> None:
        self.read_moisture()
        self.try_to_irrigate()


    # --------------------------------------------------------------------------
    # Moisture

    def read_moisture(self) -> None:
        self.moisture_previous = self.moisture_current # Temporarily store the previous moisture level
        raw_value = self.device_io.read_moisture_sensor() # Read the raw value from the sensor

        # Ensure that the moisture level has been read
        if not isinstance(raw_value, (int, float)):
            raise Exception("Could not read moisture level correctly")

        # Skip the moisture level reading if it's out of range
        if raw_value < self.moisture_sensor_wet: return
        if raw_value > self.moisture_sensor_dry: return

        # Add the new reading to the list and calculate the moving average
        new_moisture = self.get_moisture_percentage(raw_value)
        self.moisture_buffer.append(new_moisture)
        self.moisture_buffer.pop(0)

        if None not in self.moisture_buffer: # Only calculate average if buffer is full
            self.moisture_current = round(sum(self.moisture_buffer) / len(self.moisture_buffer)) # type: ignore

            # Save the reading
            if self.moisture_current is not None and self.moisture_previous != self.moisture_current:
                self.set_moisture(self.moisture_current)

    # Calculate moisture percentage, from dry (0%) to wet (100%)
    def get_moisture_percentage(self, raw_value: int) -> int:
        # Clip the raw_value to the defined min and max values
        clipped_value = round(max(min(raw_value, self.moisture_sensor_dry), self.moisture_sensor_wet))

        return round(100 - ((clipped_value - self.moisture_sensor_wet) / (self.moisture_sensor_dry - self.moisture_sensor_wet)) * 100)

    def set_moisture(self, moisture_level: int) -> None:
        print("-> Saving moisture reading:", f"{moisture_level}%")
        self.device.pb.create_moisture(self.id, moisture_level)
        self.moisture_current = moisture_level


    # --------------------------------------------------------------------------
    # Irrigation

    def try_to_irrigate(self) -> None:
        if None in self.moisture_buffer: return # Wait for the buffer to be filled with smoothed readings
        if self.moisture_previous is None: return # Ensure that the moisture level has been read
        if self.moisture_current is None: return # Ensure that the moisture level has been read

        if self.irrigation_event == None:
            # Check if the moisture level has changed, unless the app has just been restarted
            if (self.moisture_previous == self.moisture_current) and (self.is_first_irrigation_attempt == False): return

            # Check the last irrigation event didn't errored
            irrigation_collection = self.device.pb.get_last_irrigation(self.id)
            if len(irrigation_collection) > 0 and irrigation_collection[0]["status"] == "error":
                print("-> Last irrigation errored and won't try again:", self.id, self.name)
                self.irrigation_event = irrigation_collection[0]
                self.is_first_irrigation_attempt = False
                return

            # It's time to irrigate
            if (self.moisture_current <= self.moisture_low):
                print("-> Irrigation started:", self.id, self.name)
                self.irrigation_event = self.device.pb.create_irrigation(self.id, "in_progress", 1)
                self.irrigate()

            self.is_first_irrigation_attempt = False
            return

        # If the last irrigation was an error, don't try to irrigate again
        if self.irrigation_event["status"] == "error": return

        if self.irrigation_event["status"] == "in_progress":
            # Ensure that the moisture level is not above the high threshold
            if self.moisture_current >= self.moisture_high:
                print("-> Irrigation stopped (succes):", self.id, self.name)
                self.device.pb.update_irrigation("success", self.irrigation_event["pumps"], self.irrigation_event["id"])
                self.irrigation_event = None
                return

            # Pump water again
            if self.irrigation_event["pumps"] < self.pump_max_attempts:
                # Check the time of the last irrigation (in UTC)
                current_time = self.device.get_current_time()
                last_irrigation_time = self.time_math.datetime_str_to_timestamp(self.irrigation_event["updated"])
                time_since_last_irrigation = current_time - last_irrigation_time

                # Ensure that the last irrigation was not recent
                if time_since_last_irrigation < self.pump_frequency_in_s: return

                self.irrigation_event = self.device.pb.update_irrigation(self.irrigation_event["status"], self.irrigation_event["pumps"] + 1, self.irrigation_event["id"])
                self.irrigate()
                return

            # Exceeded pump attempts
            if self.irrigation_event["pumps"] >= self.pump_max_attempts:
                print("-> Irrigation stopped (error):", self.id, self.name)
                self.irrigation_event = self.device.pb.update_irrigation("error", self.irrigation_event["pumps"], self.irrigation_event["id"])
                return

    def irrigate(self) -> None:
        self.device_io.toggle_pump()
        self.device.sleep(self.pump_duration_in_s)

        self.device_io.toggle_pump()
