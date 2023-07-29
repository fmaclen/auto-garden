import RPi.GPIO as GPIO
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn


class DeviceIO:
    def __init__(self, moisture_sensor_pin: int, pump_relay_pin: int) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        adc = ADS1115(i2c)
        self.channel = AnalogIn(adc, moisture_sensor_pin)

        # Pump relay
        self.gpio = GPIO
        self.pump_relay_pin = pump_relay_pin
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.pump_relay_pin, self.gpio.OUT)
        self.gpio.output(self.pump_relay_pin, self.gpio.HIGH) # Turn off the relay by default

    def read_moisture_sensor(self) -> int:
        return self.channel.value

    def toggle_pump(self) -> None:
        self.gpio.output(self.pump_relay_pin, not self.gpio.input(self.pump_relay_pin))

    def cleanup(self) -> None:
        self.gpio.cleanup()
