class DeviceIO:
    def __init__(self, moisture_sensor_pin: int, pump_relay_pin: int) -> None:
        pass

    def read_moisture_sensor(self) -> int:
        return 65535

    def toggle_pump(self) -> None:
        pass

    def cleanup(self) -> None:
        pass
