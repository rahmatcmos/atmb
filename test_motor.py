from pyA20.gpio import gpio, port
import time
from datetime import datetime


class Jajal:
    def __init__(self):
        gpio.init()

        # SEBAGAI INPUT
        self.LS_KATUP_ATAS_BUKA = port.PD14
        self.LS_KATUP_ATAS_TUTUP = port.PC4
        self.LS_KATUP_BAWAH_BUKA = port.PC7
        self.LS_KATUP_BAWAH_TUTUP = port.PA2
        self.LS_SEDOT_PLASTIK_MAJU = port.PC3
        self.LS_SEDOT_PLASTIK_MUNDUR = port.PA21

        # SEBAGAI OUTPUT
        self.MOTOR_KATUP_ATAS = port.PA1
        self.MOTOR_KATUP_BAWAH = port.PA6
        self.MOTOR_SEDOT_PLASTIK = port.PA0
        self.ARAH_MOTOR = port.PA3
        self.VACUM = port.PC0

        gpio.setcfg(self.LS_KATUP_ATAS_BUKA, gpio.INPUT)
        gpio.setcfg(self.LS_KATUP_ATAS_TUTUP, gpio.INPUT)
        gpio.setcfg(self.LS_KATUP_BAWAH_BUKA, gpio.INPUT)
        gpio.setcfg(self.LS_KATUP_BAWAH_TUTUP, gpio.INPUT)
        gpio.setcfg(self.LS_SEDOT_PLASTIK_MAJU, gpio.INPUT)
        gpio.setcfg(self.LS_SEDOT_PLASTIK_MUNDUR, gpio.INPUT)

        gpio.pullup(self.LS_KATUP_ATAS_BUKA, gpio.PULLUP)
        gpio.pullup(self.LS_KATUP_ATAS_TUTUP, gpio.PULLUP)
        gpio.pullup(self.LS_KATUP_BAWAH_BUKA, gpio.PULLUP)
        gpio.pullup(self.LS_KATUP_BAWAH_TUTUP, gpio.PULLUP)
        gpio.pullup(self.LS_SEDOT_PLASTIK_MAJU, gpio.PULLUP)
        gpio.pullup(self.LS_SEDOT_PLASTIK_MUNDUR, gpio.PULLUP)

        gpio.setcfg(self.MOTOR_KATUP_ATAS, gpio.OUTPUT)
        gpio.setcfg(self.MOTOR_KATUP_BAWAH, gpio.OUTPUT)
        gpio.setcfg(self.MOTOR_SEDOT_PLASTIK, gpio.OUTPUT)
        gpio.setcfg(self.ARAH_MOTOR, gpio.OUTPUT)
        gpio.setcfg(self.VACUM, gpio.OUTPUT)

        # reset output ke low semua untuk motor (just in case)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)
        gpio.output(self.VACUM, gpio.LOW)

    def secs(self, start_time):
        dt = datetime.now() - start_time
        return dt.seconds

    def buka_katup_atas(self):
        if gpio.input(self.LS_KATUP_ATAS_BUKA) == 0:
            return
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(0.1)
        # start_time = datetime.now()
        # while gpio.input(self.LS_KATUP_ATAS_BUKA) == 1:
        #     if self.secs(start_time) >= 4:
        #         print "sudah 4 detik"
        #         break
        time.sleep(6.2)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)

    def tutup_katup_atas(self):
        if gpio.input(self.LS_KATUP_ATAS_TUTUP) == 0:
            return
        gpio.output(self.ARAH_MOTOR, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(0.1)
        # start_time = datetime.now()
        # while gpio.input(self.LS_KATUP_ATAS_TUTUP) == 1:
        #     if self.secs(start_time) >= 4:
        #         print "sudah 4 detik"
        #         break
        time.sleep(6.6)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)

    def buka_katup_bawah(self):
        if gpio.input(self.LS_KATUP_BAWAH_BUKA) == 0:
            return
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(0.1)
        start_time = datetime.now()
        # while gpio.input(self.LS_KATUP_BAWAH_BUKA) == 1:
        time.sleep(6)
        # while True:
        #     if self.secs(start_time) >= 5:
        #         break
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)

    def tutup_katup_bawah(self):
        if gpio.input(self.LS_KATUP_BAWAH_TUTUP) == 0:
            return
        gpio.output(self.ARAH_MOTOR, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(0.1)
        start_time = datetime.now()
        # while gpio.input(self.LS_KATUP_BAWAH_TUTUP) == 1:
        # while True:
        #     if self.secs(start_time) >= 6:
        #         break
        time.sleep(7)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)

    def sedot_plastik_maju(self):
        gpio.output(self.ARAH_MOTOR, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.HIGH)
        time.sleep(11.2)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)

    def sedot_plastik_mundur(self):
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.HIGH)
        time.sleep(10)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)

    def hidupkan_vacum(self):
        gpio.output(self.VACUM, gpio.HIGH)

    def matikan_vacum(self):
        gpio.output(self.VACUM, gpio.LOW)

    def simulasi_ambil(self):
        self.buka_katup_atas()
        time.sleep(1)
        self.tutup_katup_atas()
        time.sleep(0.5)
        self.sedot_plastik_maju()
        self.hidupkan_vacum()
        time.sleep(1)
        self.sedot_plastik_mundur()
        self.buka_katup_bawah()
        time.sleep(4)
        self.tutup_katup_bawah()
        self.matikan_vacum()

if __name__ == "__main__":
    try:
        jajal = Jajal()
        print "1. Buka katup atas (Mundur)"
        print "2. Tutup katup atas (Maju)"
        print "3. Buka katup bawah (Mundur)"
        print "4. Tutup katup bawah (Maju)"
        print "5. Sedot plastik maju"
        print "6. Sedot plastik mundur"
        print "7. Hidupkan blower"
        print "8. Matikan blower"
        print "9. Simulasi ambil beras"

        yang_ditest = raw_input("Pilih yang mau ditest:")
        yang_ditest = int(yang_ditest)

        if yang_ditest == 1:
            jajal.buka_katup_atas()

        if yang_ditest == 2:
            jajal.tutup_katup_atas()

        if yang_ditest == 3:
            jajal.buka_katup_bawah()

        if yang_ditest == 4:
            jajal.tutup_katup_bawah()

        if yang_ditest == 5:
            jajal.sedot_plastik_maju()

        if yang_ditest == 6:
            jajal.sedot_plastik_mundur()

        if yang_ditest == 7:
            jajal.hidupkan_vacum()

        if yang_ditest == 8:
            jajal.matikan_vacum()

        if yang_ditest == 9:
            jajal.simulasi_ambil()

    except KeyboardInterrupt:
        gpio.output(jajal.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(jajal.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(jajal.MOTOR_SEDOT_PLASTIK, gpio.LOW)
        gpio.output(jajal.VACUM, gpio.LOW)