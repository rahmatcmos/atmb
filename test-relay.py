import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

try:
    while True:
        GPIO.output(16, 1)
        GPIO.output(18, 1)
        time.sleep(1)
        GPIO.output(16, 0)
        GPIO.output(18, 0)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(16, 0)
    GPIO.output(18, 0)
    GPIO.cleanup()
