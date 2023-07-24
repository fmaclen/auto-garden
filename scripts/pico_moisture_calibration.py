from machine import ADC
from utime import sleep

print("Reading moisture...")
while True:
    adc = ADC(28) # GPIO28 = ADC0
    print(adc.read_u16())
    sleep(1) # sleep 1sec
