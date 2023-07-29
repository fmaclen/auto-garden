from machine import ADC, Pin

class DeviceIO:
    def __init__(self, moisture_sensor_pin: int, pump_relay_pin: int) -> None:
        self.adc = ADC(moisture_sensor_pin)
        self.pump_relay = Pin(pump_relay_pin, Pin.OUT)

    def read_moisture_sensor(self) -> int:
        return self.adc.read_u16()

    def toggle_pump(self) -> None:
        self.pump_relay.toggle()

    def cleanup(self) -> None:
        self.pump_relay.value(0)
