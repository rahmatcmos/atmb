from pyA20.gpio import gpio, port
import time


class Keypad:
    def __init__(self):
        self.matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ['*', 0, '#']
        ]

        self.row = [port.PA8, port.PA9, port.PA10, port.PA20]
        self.col = [port.PG7, port.PG6, port.PG9]

        gpio.init()

        for i in range(len(self.row)):
            gpio.setcfg(self.row[i], gpio.INPUT)
            gpio.pullup(self.row[i], gpio.PULLUP)

        for i in range(len(self.col)):
            gpio.setcfg(self.col[i], gpio.OUTPUT)
            gpio.output(self.col[i], 1)

    def get_pressed_key(self):
        try:

            while True:
                for j in range(len(self.col)):
                    gpio.output(self.col[j], 0)

                    for i in range(len(self.row)):
                        if gpio.input(self.row[i]) == 0:
                            key = self.matrix[i][j]
                            print key
                            time.sleep(0.3)

                    gpio.output(self.col[j], 1)
                    # time.sleep(0.001)
        except KeyboardInterrupt:
            print "Quit"

app = Keypad()
app.get_pressed_key()