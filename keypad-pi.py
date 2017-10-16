import RPi.GPIO as GPIO
import time


class Keypad:
    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ['*', 0, '#']
        ]

        self.row = [31, 33, 35, 37]
        self.col = [36, 38, 40]

        for i in range(len(self.row)):
            GPIO.setup(self.row[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for i in range(len(self.col)):
            GPIO.setup(self.col[i], GPIO.OUT)
            GPIO.output(self.col[i], 1)

    def get_pressed_key(self):
        try:

            while True:
                for j in range(len(self.col)):
                    GPIO.output(self.col[j], 0)

                    for i in range(len(self.row)):
                        if GPIO.input(self.row[i]) == 0:
                            key = self.matrix[i][j]
                            print key
                            time.sleep(0.27)

                    GPIO.output(self.col[j], 1)
                    time.sleep(0.03)

        except KeyboardInterrupt:
            GPIO.cleanup()
            print "Quit"


app = Keypad()
app.get_pressed_key()