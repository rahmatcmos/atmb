#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import main_ui
import menu_ui
import input_pin_ui
import saldo_ui
import ubah_pin_ui
import proses_ui
import sys
import time
# from datetime import datetime
import binascii
import PN532
from pyA20.gpio import gpio, port
import MySQLdb
import subprocess

# card_id test = f28268e0
# pin test = 123456


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.name = 'atm_beras'
        self.username = 'root'
        self.password = 'bismillah'
        self.key = 'F3229A0B371ED2D9441B830D21A390C3'

    def connect(self):
        return MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.name)


class Main(QtGui.QWidget, main_ui.Ui_main):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.update_clock()
        self.info.setText("TEMPELKAN KARTU ATMB ANDA...")
        self.password = ''

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.scan_thread = ScanThread()
        self.connect(self.scan_thread, QtCore.SIGNAL('cardDetected'), self.card_detected)
        self.connect(self.scan_thread, QtCore.SIGNAL('updateInfo'), self.update_info)
        self.scan_thread.start()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()
        self.showFullScreen()

    def keypad_pressed_event(self, key):
        self.password += str(key)

        if self.password == '*123#':
            self.keypad_thread.terminate()
            self.scan_thread.terminate()
            self.close()
            subprocess.call(['python', '/root/Desktop/ATM_BERAS/main.py'])

        if self.password == '*124#':
            subprocess.call(['reboot'])

        if self.password == '*125#':
            subprocess.call(['halt'])

    def card_detected(self, nasabah):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.scan_thread.terminate()
        self.window = InputPin(nasabah)
        self.close()

    def update_info(self, info):
        self.info.setText(info)

    def update_clock(self):
        self.tanggal.setText(time.strftime("%d %b %Y"))
        self.jam.setText(time.strftime("%H:%M:%S"))


class InputPin(QtGui.QWidget, input_pin_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.entered_pin = ''
        self.masked_pin = ''
        self.nasabah = nasabah
        self.trial = 0

        if self.nasabah[5] == 'L':
            panggilan = 'BAPAK {}'.format(self.nasabah[1])
        else:
            panggilan = 'IBU {}'.format(self.nasabah[1])

        self.info.setText("SELAMAT DATANG, {}. MASUKKAN PIN ANDA".format(panggilan))
        self.showFullScreen()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()

    def ulangi(self):
        self.info.setText("SILAKAN ULANGI MASUKKAN PIN ANDA")
        self.pin.setText('----')
        self.entered_pin = ''
        self.masked_pin = ''

    def kembali(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()

    def input_pin(self, pin):
        self.entered_pin += str(pin)
        self.masked_pin += '*'
        self.pin.setText(self.masked_pin)

        if len(self.entered_pin) == 4:
            db = Database()
            db_con = db.connect()
            cur = db_con.cursor()
            cur.execute(
                "SELECT * FROM nasabah where id = %s AND pin = AES_ENCRYPT(%s, UNHEX(%s))",
                (self.nasabah[0], self.entered_pin, db.key)
            )

            res = cur.fetchone()
            cur.close()
            db_con.close()

            if res:
                self.timer.stop()
                self.keypad_thread.terminate()
                self.menu = MainMenu(self.nasabah)
                self.close()

            else:
                self.info.setText("PIN ANDA SALAH. SILAKAN ULANGI MASUKKAN PIN ANDA")
                self.pin.setText('----')
                self.entered_pin = ''
                self.masked_pin = ''
                self.trial += 1

    def blokir(self):
        self.info.setText("ANDA SALAH MEMASUKKAN PIN 3 KALI. KARTU ANDA DIBLOKIR. SILAKAN HUBUNGI PETUGAS.")
        self.pin.setText('')
        self.entered_pin = ''
        self.masked_pin = ''
        self.ulangi_btn.setEnabled(False)

        db = Database()
        db_con = db.connect()
        cur = db_con.cursor()
        cur.execute("SELECT status FROM nasabah WHERE id = %s", (self.nasabah[0],))
        cur.close()

        if not cur.fetchone():
            cur = db_con.cursor()
            cur.execute("UPDATE nasabah SET status = 0 WHERE id = %s", (self.nasabah[0],))
            db_con.commit()

        db_con.close()

    def keypad_pressed_event(self, key):
        if key == '*':
            if self.trial < 1000:
                self.ulangi()

        if key == '#':
            self.kembali()

        if key in range(10):
            if self.trial < 1000:
                self.input_pin(key)
            else:
                self.blokir()


class MainMenu(QtGui.QWidget, menu_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.info.setText("")

        if self.nasabah[2] == 0:
            self.ambil_beras_btn.setEnabled(False)

        self.showFullScreen()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()

    def keypad_pressed_event(self, key):
        if key == 1:
            self.ambil_beras()

        if key == 2:
            self.cek_saldo()

        if key == 3:
            self.ubah_pin()

        if key == 4:
            self.selesai()

    def ambil_beras(self):
        if self.nasabah[2] == 0:
            self.info.setText("MAAF, TRANSAKSI DITOLAK. SALDO ANDA 0.")
            return

        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Proses(self.nasabah)
        self.close()

    def cek_saldo(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Saldo(self.nasabah)
        self.close()

    def ubah_pin(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = UbahPin(self.nasabah)
        self.close()

    def selesai(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()


class Saldo(QtGui.QWidget, saldo_ui.Ui_Form):
    def __init__(self, nasabah, additional_info=''):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        db = Database()
        db = db.connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = %s", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()
        db.close()

        self.saldo.setText('{} KG'.format(self.nasabah[2]))
        self.info.setText(additional_info + ' ' + self.info.text())

        if self.nasabah[2] == 0:
            self.ambil_beras_btn.setEnabled(False)

        self.showFullScreen()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(5000)

    def time_out(self):
        self.window = Main()
        self.close()


class UbahPin(QtGui.QWidget, ubah_pin_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.entered_pin = ''
        self.confirm_pin = ''
        self.masked_pin = ''
        self.ulang = 0
        self.showFullScreen()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()

    def ganti_pin(self, pin):
        self.masked_pin += '*'
        self.pin.setText(self.masked_pin)

        if self.ulang == 0:
            self.entered_pin += str(pin)

            if len(self.entered_pin) == 4:
                self.pin.setText('----')
                self.masked_pin = ''
                self.info.setText("ULANGI MASUKKAN KEMBALI PIN BARU ANDA")
                self.ulang = 1

        else:
            self.confirm_pin += str(pin)

            if len(self.confirm_pin) == 4:
                if self.confirm_pin == self.entered_pin:
                    db = Database()
                    db_con = db.connect()
                    cur = db_con.cursor()
                    cur.execute("UPDATE nasabah SET pin = AES_ENCRYPT(%s, UNHEX(%s)) "
                                "WHERE id = %s", (self.entered_pin, db.key, self.nasabah[0]))
                    cur.execute(
                        "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ganti pin', 0)",
                        (self.nasabah[0],)
                    )
                    cur.close()
                    db_con.commit()
                    db_con.close()

                    self.info.setText("PIN ANDA BERHASIL DIUBAH")
                    self.pin.setText('')

                else:
                    self.info.setText("PIN TIDAK SAMA. SILAKAN ULANGI KEMBALI")
                    self.pin.setText("----")
                    self.ulang = 0
                    self.entered_pin = ''
                    self.confirm_pin = ''
                    self.masked_pin = ''

    def keypad_pressed_event(self, key):
        if key == '*':
            self.ulangi()

        if key == '#':
            self.kembali()

        if key in range(10):
            self.ganti_pin(key)

    def ulangi(self):
        self.info.setText("SILAKAN MASUKKAN PIN BARU ANDA")
        self.pin.setText("----")
        self.entered_pin = ''
        self.confirm_pin = ''
        self.masked_pin = ''
        self.ulang = 0

    def kembali(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = MainMenu(self.nasabah)
        self.close()


class ScanThread(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.nfc_port = "/dev/ttyUSB0"
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        try:
            self.pn532 = PN532.PN532(self.nfc_port, 115200)
            self.pn532.begin()
            self.pn532.SAM_configuration()

            while not self.exiting:
                uid = self.pn532.read_passive_target()
                if uid is "no_card":
                    continue

                card_id = str(binascii.hexlify(uid))

                db = Database()
                db_con = db.connect()
                cur = db_con.cursor()
                cur.execute("SELECT * FROM nasabah WHERE card_id = AES_ENCRYPT(%s, UNHEX(%s))", (card_id, db.key))
                nasabah = cur.fetchone()
                cur.close()
                db_con.close()

                if nasabah:
                    self.emit(QtCore.SIGNAL('cardDetected'), nasabah)
                    break

                else:
                    self.emit(QtCore.SIGNAL('updateInfo'), "KARTU TIDAK TERDAFTAR")
                    time.sleep(3)
                    self.emit(QtCore.SIGNAL('updateInfo'), "TEMPELKAN KARTU ATMB ANDA...")

        except Exception as e:
            self.emit(QtCore.SIGNAL('updateInfo'), "SENSOR KARTU TIDAK DITEMUKAN!")
            time.sleep(3)
            subprocess.call(['python', '/root/Desktop/ATM_BERAS/main.py'])


class ProsesThread(QtCore.QThread):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.nasabah = nasabah
        self.saldo = self.nasabah[2] - 3

        gpio.init()

        # SEBAGAI INPUT
        self.LS_KATUP_ATAS_BUKA = port.PD14
        self.LS_KATUP_ATAS_TUTUP = port.PC4
        self.LS_KATUP_BAWAH_BUKA = port.PC7
        self.LS_KATUP_BAWAH_TUTUP = port.PA2
        self.LS_SEDOT_PLASTIK_MAJU = port.PC3
        self.LS_SEDOT_PLASTIK_MUNDUR = port.PA21

        # SEBAGAI OUTPUT
        self.MOTOR_KATUP_ATAS = port.PA6
        self.MOTOR_KATUP_BAWAH = port.PA1
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

    def __del__(self):
        # matikan motor dulu
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        self.wait()

    def buka_katup_atas(self):
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(3.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)

    def tutup_katup_atas(self):
        gpio.output(self.ARAH_MOTOR, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(4)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)

    def buka_katup_bawah(self):
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)

    def tutup_katup_bawah(self):
        gpio.output(self.ARAH_MOTOR, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(5.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)

    def sedot_plastik_maju(self):
        gpio.output(self.ARAH_MOTOR, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.HIGH)
        time.sleep(10)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)

    def sedot_plastik_mundur(self):
        gpio.output(self.ARAH_MOTOR, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.HIGH)
        time.sleep(10)
        gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)
        gpio.output(self.ARAH_MOTOR, gpio.LOW)

    def hidupkan_vacum(self):
        gpio.output(self.VACUM, gpio.HIGH)

    def matikan_vacum(self):
        gpio.output(self.VACUM, gpio.LOW)

    def run(self):
        self.emit(QtCore.SIGNAL('infoProses'), "SEDANG MEMPROSES. SILAKAN TUNGGU...")

        try:
            self.buka_katup_atas()
            time.sleep(3)
            self.tutup_katup_atas()
            self.sedot_plastik_maju()
            self.hidupkan_vacum()
            time.sleep(2)
            self.sedot_plastik_mundur()
            self.buka_katup_bawah()
            time.sleep(10)
            self.tutup_katup_bawah()
            self.matikan_vacum()

            # simpan log di database, update saldo
            db = Database()
            db_con = db.connect()
            cur = db_con.cursor()
            cur.execute("UPDATE nasabah SET saldo = %s WHERE id = %s", (self.saldo, self.nasabah[0]))
            cur.execute(
                "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ambil', %s)",
                (self.nasabah[0], 3)
            )
            cur.close()
            db_con.commit()
            db_con.close()

        except SystemExit:
            gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
            gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
            gpio.output(self.MOTOR_SEDOT_PLASTIK, gpio.LOW)
            gpio.output(self.ARAH_MOTOR, gpio.LOW)


class Proses(QtGui.QWidget, proses_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.saldo = self.nasabah[2] - 3
        self.showFullScreen()

        self.proses_thread = ProsesThread(self.nasabah)
        self.connect(self.proses_thread, QtCore.SIGNAL('infoProses'), self.update_info)
        self.connect(self.proses_thread, QtCore.SIGNAL('finished()'), self.selesai)
        self.proses_thread.start()

    def update_info(self, info):
        self.info.setText(info)

    def selesai(self):
        self.window = Saldo(self.nasabah, "SILAKAN AMBIL BERAS ANDA.")
        self.close()


class KeypadThread(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.exiting = False

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

    def __del__(self):
        self.exiting = True
        self.wait()

    # def milisecs(self, start_time):
    #     dt = datetime.now() - start_time
    #     return dt.microseconds/1000

    def run(self):
        time.sleep(0.5)
        while not self.exiting:
            for j in range(len(self.col)):
                gpio.output(self.col[j], 0)

                for i in range(len(self.row)):
                    if gpio.input(self.row[i]) == 0:
                        key = self.matrix[i][j]
                        self.emit(QtCore.SIGNAL('keypadPressed'), key)
                        time.sleep(0.27)

                gpio.output(self.col[j], 1)
                time.sleep(0.03)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Main()
    sys.exit(app.exec_())
