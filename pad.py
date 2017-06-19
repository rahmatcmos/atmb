#!/usr/bin/python

from pyA20.gpio import gpio
from pyA20.gpio import port
import time


class Keypad():
    def __init__(self):
        self._handlers = []

        self._keypad = [
            [1, 2, 3, "A"],
            [4, 5, 6, "B"],
            [7, 8, 9, "C"],
            ["*", 0, "#", "D"]
        ]

        self._row_pins = [port.PG7, port.PG6, port.PA20, port.PA10]
        self._col_pins = [port.PG9, port.PA9, port.PA8, port.PG8]
        self._key_delay = 300

        self._last_key_press_time = 0

        gpio.init()

        self._setRowsAsInput()
        self._setColumnsAsOutput()

    def registerKeyPressHandler(self, handler):
        self._handlers.append(handler)

    def unregisterKeyPressHandler(self, handler):
        self._handlers.remove(handler)

    def clearKeyPressHandlers(self):
        self._handlers = []

    def _onKeyPress(self, channel):
        currTime = self.getTimeInMillis()
        if currTime < self._last_key_press_time + self._key_delay:
            return

        keyPressed = self.getKey()
        if keyPressed is not None:
            for handler in self._handlers:
                handler(keyPressed)
            self._last_key_press_time = currTime

    def _setRowsAsInput(self):
        # Set all rows as input
        for i in range(len(self._row_pins)):
            gpio.setcfg(self._row_pins[i], gpio.INPUT)
            gpio.pullup(self._row_pins[i], gpio.PULLUP)
            # gpio.add_event_detect(self._row_pins[i], gpio.FALLING, callback=self._onKeyPress, bouncetime=self._key_delay)

    def _setColumnsAsOutput(self):
        # Set all columns as output low
        for j in range(len(self._col_pins)):
            gpio.setcfg(self._col_pins[j], gpio.OUTPUT)
            gpio.output(self._col_pins[j], gpio.LOW)

    def getKey(self):

        keyVal = None

        # Scan rows for pressed key
        rowVal = None
        for i in range(len(self._row_pins)):
            tmpRead = gpio.input(self._row_pins[i])
            if tmpRead == 0:
                rowVal = i
                break

        # Scan columns for pressed key
        colVal = None
        if rowVal is not None:
            for i in range(len(self._col_pins)):
                gpio.output(self._col_pins[i], gpio.HIGH)
                if gpio.input(self._row_pins[rowVal]) == gpio.HIGH:
                    colVal = i
                gpio.output(self._col_pins[i], gpio.LOW)

        # Determine pressed key, if any
        if colVal is not None:
            keyVal = self._keypad[rowVal][colVal]

        return keyVal

    def cleanup(self):
        gpio.cleanup()

    def getTimeInMillis(self):
        return time.time() * 1000