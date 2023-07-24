import RPi.GPIO as GPIO
import time

POT_PUMP_MAX_ATTEMPS = 3
POT_PUMP_DURATION_IN_S = 8
POT_PUMP_FREQUENCY_IN_S = 5
POT_PUPM_GPIO_BCM_PIN = [21, 20, 16]

# Setting up the GPIO mode
GPIO.setmode(GPIO.BCM) 

try:
    for pin in POT_PUPM_GPIO_BCM_PIN:
        # Setting up pin as output
        GPIO.setup(pin, GPIO.OUT)

        print("turning on:", pin)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(POT_PUMP_DURATION_IN_S)

        print("turning off:", pin)
        GPIO.output(pin, GPIO.HIGH)

        time.sleep(POT_PUMP_FREQUENCY_IN_S)

except KeyboardInterrupt:
    # If CTRL+C is pressed, turn off the pin and cleanup the setup
    for pin in POT_PUPM_GPIO_BCM_PIN:
        GPIO.output(pin, GPIO.HIGH)

    GPIO.cleanup() 
