import time
import serial

class TestMotor:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyUSB0", timeout=1)


    def maju(self):
        self.ser.write(b'\x07')
        self.ser.write(b'\x06')
        # time.sleep(21) untuk yang lambat
        time.sleep(21)
        self.ser.write(b'\x08')

    def mundur(self):
        self.ser.write(b'\x07')
        self.ser.write(b'\x05')
        # time.sleep(21) untuk yang lambat
        time.sleep(21)
        self.ser.write(b'\x08')

    def ambil(self, jumlah):
        for i in range(1, jumlah):
            # buka
            self.ser.write(b'\x05')  # mundur
            self.ser.write(b'\x07')  # motor hidup
            time.sleep(2.5)  # tunggu buka sempurna
            self.ser.write(b'\x08')  # motor mati
            time.sleep(10)  # tunggu beras turun

            # tutup
            self.ser.write(b'\x06')  # maju
            self.ser.write(b'\x07')  # motor hidup
            time.sleep(2.5)  # tunggu buka sempurna
            self.ser.write(b'\x08')  # motor mati
            time.sleep(1)

    def close_serial(self):
        self.ser.close()


if __name__ == "__main__":
    try:
        test = TestMotor()
        print "1. MAJU"
        print "2. MUNDUR"
        print "3. AMBIL 1"
        print "4. AMBIL 2"
        print "5. AMBIL 3"

        yang_ditest = raw_input("Pilih:")
        yang_ditest = int(yang_ditest)

        if yang_ditest == 1:
            test.maju()

        if yang_ditest == 2:
            test.mundur()

        if yang_ditest == 3:
            test.ambil(1)

        if yang_ditest == 4:
            test.ambil(2)

        if yang_ditest == 5:
            test.ambil(3)

    except KeyboardInterrupt:
        test.ser.write(b'\x08')
        test.close_serial()