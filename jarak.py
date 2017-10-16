import RPi.GPIO as GPIO
import time


class Jarak:
    def __init__(self):

        self.trig = 16
        self.echo = 12

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # trigger
        GPIO.setup(self.trig, GPIO.OUT)
        # echo
        GPIO.setup(self.echo, GPIO.IN)

    def ukur_jarak(self):
        try:
            while True:
                GPIO.output(self.trig, False)
                time.sleep(2)
                GPIO.output(self.trig, True)
                time.sleep(0.00001)
                GPIO.output(self.trig, False)

                while GPIO.input(self.trig) == 0:
                    pulse_start = time.time()

                while GPIO.input(self.echo) == 1:
                    pulse_end = time.time()

                duration = pulse_end - pulse_start

                distance = duration * 17150
                distance = round(distance, 2)

                if distance > 2 and distance < 400:
                    print "Distance:", distance - 0.5, "cm"
                else:
                    print "Out Of Range"  # display out of range

        except KeyboardInterrupt:
            GPIO.cleanup()
            print "Quit"


app = Jarak()
app.ukur_jarak()
