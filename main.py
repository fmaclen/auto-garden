try: from typing import List
except: pass

from lib.pot import Pot
from lib.device import Device
from env import TEST_ENV

TICK_RATE_IN_S = 2


class AutoGarden:
    def __init__(self) -> None:
        try:
            print("-> Starting AutoGarden")
            self.device = Device(TICK_RATE_IN_S)
            self.pots = self.setup_pots()
            self.loop()
        except Exception as e:
            self.device.handle_system_error(str(e))

    def loop(self) -> None:
        try:
            while True:
                # Check manual irrigation requests
                pot_id_to_irrigate = self.device.server_listen_pot_irrigation()

                for pot in self.pots:
                    if pot.id == pot_id_to_irrigate: pot.irrigate()
                    pot.update()

                # Only run the loop once in tests
                if TEST_ENV == True: break

                self.device.sleep(TICK_RATE_IN_S)

        except KeyboardInterrupt:
            print("-> Stopping AutoGarden")
            for pot in self.pots:
                pot.device_io.cleanup()

    def setup_pots(self) -> List[Pot]:
        pots = []
        pots_collection = self.device.pb.get_pots()

        if len(pots_collection) == 0:
            raise Exception("No pots to irrigate")

        for pot in pots_collection:
            pots.append(
                Pot(
                    self.device,
                    pot["id"],
                    pot["name"],
                    pot["moisture_low"],
                    pot["moisture_high"],
                    pot["moisture_sensor_dry"],
                    pot["moisture_sensor_wet"],
                    pot["moisture_sensor_pin"],
                    pot["pump_max_attempts"],
                    pot["pump_duration_in_s"],
                    pot["pump_frequency_in_s"],
                    pot["pump_relay_pin"],
                )
            )

        return pots


if __name__ == "__main__":
    auto_garden = AutoGarden()
