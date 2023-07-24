import RPi.GPIO as GPIO
import time

POT_PUMP_MAX_ATTEMPS = 1
POT_PUMP_DURATION_IN_S = 8
POT_PUMP_FREQUENCY_IN_S = 5
POT_PUPM_GPIO_BCM_PIN = 20

# Setting up the GPIO mode
GPIO.setmode(GPIO.BCM) 

# Setting up pin as output
GPIO.setup(POT_PUPM_GPIO_BCM_PIN, GPIO.OUT)

try:
    pumps = 0
    while True:
        # Don't wait if this is the first pump
        if pumps > 0: time.sleep(POT_PUMP_FREQUENCY_IN_S)

        print("turning on:", POT_PUPM_GPIO_BCM_PIN)
        pumps += 1
        GPIO.output(POT_PUPM_GPIO_BCM_PIN, GPIO.LOW)
        time.sleep(POT_PUMP_DURATION_IN_S)

        print("turning off:", POT_PUPM_GPIO_BCM_PIN)
        GPIO.output(POT_PUPM_GPIO_BCM_PIN, GPIO.HIGH)

        if POT_PUMP_FREQUENCY_IN_S is None: raise KeyboardInterrupt # Runs once and stops
        if pumps >= POT_PUMP_MAX_ATTEMPS: raise KeyboardInterrupt # Runs once and stops

except KeyboardInterrupt:
    # If CTRL+C is pressed, turn off the pin and cleanup the setup
    GPIO.output(POT_PUPM_GPIO_BCM_PIN, GPIO.HIGH)
    GPIO.cleanup() 
