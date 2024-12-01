import RPi.GPIO as GPIO
import time


LIGHT_SENSOR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(LIGHT_SENSOR_PIN) == GPIO.HIGH:
            print("light!")
        else:
            print("no light!")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("clean")
finally:
    GPIO.cleanup()