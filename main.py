try: from typing import List
except: pass

from lib.pot import Pot
from lib.device import Device

TICK_RATE_IN_S = 2


class AutoGarden:
    def __init__(self) -> None:
        print("-> Starting AutoGarden")
        self.device = Device(TICK_RATE_IN_S)
        self.pots = self.setup_pots()
        self.loop()

    def loop(self) -> None:
        try:
            while True:
                for pot in self.pots:
                    pot.update()

                # Only run the loop once in tests
                if self.device.name == "Greenhouse (Test)": break

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
