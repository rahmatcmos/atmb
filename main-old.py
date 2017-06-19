#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import main_ui
import menu_ui
import input_pin_ui
import saldo_ui
import ubah_pin_ui
import ambil_beras_ui
import proses_ui
import sys
import time
from datetime import datetime
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
        self.setupUi(self)
        self.info.setText("TEMPELKAN KARTU ATMB ANDA...")

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

    # buat development aja. nanti pake kombinasi key
    def keypad_pressed_event(self, key):
        if key == '*':
            self.keypad_thread.terminate()
            self.scan_thread.terminate()
            self.close()
            subprocess.call(['python', '/root/Desktop/ATM_BERAS/main.py'])

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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.timer.stop()
            self.close()


class InputPin(QtGui.QWidget, input_pin_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.entered_pin = ''
        self.masked_pin = ''
        self.nasabah = nasabah
        self.trial = 0

        self.ulangi_btn.clicked.connect(self.ulangi)
        self.selesai_btn.clicked.connect(self.kembali)

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
        self.pin.setText('------')
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

        if len(self.entered_pin) == 6:
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
                self.pin.setText('------')
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
        if key == 'A':
            if self.trial < 1000:
                self.ulangi()

        if key == 'B':
            self.kembali()

        if key in range(10):
            if self.trial < 1000:
                self.input_pin(key)
            else:
                self.blokir()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape or e.key() == QtCore.Qt.Key_B:
            self.kembali()

        if e.key() in range(48, 58):
            if self.trial < 1000:
                self.input_pin(range(48, 58).index(e.key()))
            else:
                self.blokir()

        if e.key() == QtCore.Qt.Key_A:
            if self.trial < 1000:
                self.ulangi()


class MainMenu(QtGui.QWidget, menu_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.nasabah = nasabah
        self.ambil_beras_btn.clicked.connect(self.ambil_beras)
        self.cek_saldo_btn.clicked.connect(self.cek_saldo)
        self.ubah_pin_btn.clicked.connect(self.ubah_pin)
        self.selesai_btn.clicked.connect(self.selesai)
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
        if str(key) == 'A':
            self.ambil_beras()

        if str(key) == 'B':
            self.cek_saldo()

        if str(key) == 'C':
            self.ubah_pin()

        if str(key) == 'D':
            self.selesai()

    def ambil_beras(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = AmbilBeras(self.nasabah)
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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_A:
            self.ambil_beras()

        if e.key() == QtCore.Qt.Key_B:
            self.cek_saldo()

        if e.key() == QtCore.Qt.Key_C:
            self.ubah_pin()

        if e.key() == QtCore.Qt.Key_D:
            self.selesai()


class Saldo(QtGui.QWidget, saldo_ui.Ui_Form):
    def __init__(self, nasabah, additional_info=''):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        db = Database()
        db = db.connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = %s", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()
        db.close()

        self.ambil_beras_btn.clicked.connect(self.ambil_beras)
        self.selesai_btn.clicked.connect(self.selesai)
        self.kembali_btn.clicked.connect(self.kembali)
        self.saldo.setText('{} LITER'.format(self.nasabah[2]))
        self.info.setText(additional_info + ' ' + self.info.text())
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
        if key == 'A':
            self.ambil_beras()

        if key == 'B':
            self.kembali()

        if key == 'C':
            self.selesai()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_A:
            self.ambil_beras()

        if e.key() == QtCore.Qt.Key_B:
            self.kembali()

        if e.key() == QtCore.Qt.Key_C:
            self.selesai()

    def ambil_beras(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = AmbilBeras(self.nasabah)
        self.close()

    def kembali(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = MainMenu(self.nasabah)
        self.close()

    def selesai(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()


class UbahPin(QtGui.QWidget, ubah_pin_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.nasabah = nasabah
        self.entered_pin = ''
        self.confirm_pin = ''
        self.masked_pin = ''
        self.ulang = 0
        self.kembali_btn.clicked.connect(self.kembali)
        self.selesai_btn.clicked.connect(self.selesai)
        self.ulangi_btn.clicked.connect(self.ulangi)
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

            if len(self.entered_pin) == 6:
                self.pin.setText('------')
                self.masked_pin = ''
                self.info.setText("ULANGI MASUKKAN KEMBALI PIN BARU ANDA")
                self.ulang = 1

        else:
            self.confirm_pin += str(pin)

            if len(self.confirm_pin) == 6:
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
                    self.pin.setText("------")
                    self.ulang = 0
                    self.entered_pin = ''
                    self.confirm_pin = ''
                    self.masked_pin = ''

    def keypad_pressed_event(self, key):
        if key == 'A':
            self.ulangi()

        if key == 'B':
            self.kembali()

        if key == 'C':
            self.selesai()

        if key in range(10):
            self.ganti_pin(key)

    def ulangi(self):
        self.info.setText("SILAKAN MASUKKAN PIN BARU ANDA")
        self.pin.setText("------")
        self.entered_pin = ''
        self.confirm_pin = ''
        self.masked_pin = ''
        self.ulang = 0

    def selesai(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()

    def kembali(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = MainMenu(self.nasabah)
        self.close()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_A:
            self.ulangi()

        if e.key() == QtCore.Qt.Key_B:
            self.kembali()

        if e.key() == QtCore.Qt.Key_C:
            self.selesai()

        if e.key() in range(48, 58):
            self.ganti_pin(range(48, 58).index(e.key()))


class AmbilBeras(QtGui.QWidget, ambil_beras_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        db = Database()
        db = db.connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = %s", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()
        db.close()

        self.saldo = self.nasabah[2]
        self.info.setText('')

        if self.saldo == 0:
            self.info.setText('MAAF, SISA SALDO ANDA SAAT INI ADALAH 0 LITER')
            self.satu_liter.setEnabled(False)
            self.dua_liter.setEnabled(False)
            # self.tiga_liter.setEnabled(False)
            # self.empat_liter.setEnabled(False)
            # self.lima_liter.setEnabled(False)

        self.selesai_btn.clicked.connect(self.selesai)
        self.kembali_btn.clicked.connect(self.kembali)
        self.satu_liter.clicked.connect(self.proses_1)
        self.dua_liter.clicked.connect(self.proses_2)
        # self.tiga_liter.clicked.connect(self.proses_3)
        # self.empat_liter.clicked.connect(self.proses_4)
        # self.lima_liter.clicked.connect(self.proses_5)
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
        if key == 'A':
            self.kembali()

        if key == 'B':
            self.selesai()

        if key in range(1, 6):
            self.ambil = key
            self.proses()

    def selesai(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()

    def kembali(self):
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = MainMenu(self.nasabah)
        self.close()

    def proses(self):
        if self.ambil > self.saldo:
            self.info.setText('SALDO TIDAK CUKUP. SALDO ANDA TINGGAL {} LITER. '
                              'SILAKAN PILIH JUMLAH YANG SESUAI.'.format(self.saldo))

        else:
            self.timer.stop()
            self.keypad_thread.terminate()
            self.window = Proses(self.nasabah, self.ambil)
            self.close()

    def proses_1(self):
        self.ambil = 1
        self.proses()

    def proses_2(self):
        self.ambil = 2
        self.proses()

    def proses_3(self):
        self.ambil = 3
        self.proses()

    def proses_4(self):
        self.ambil = 4
        self.proses()

    def proses_5(self):
        self.ambil = 5
        self.proses()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_A:
            self.kembali()

        if e.key() == QtCore.Qt.Key_B:
            self.selesai()

        if e.key() in range(48, 55) and self.saldo > 0 and e.key() > 48:
            # nasabah milih jumlah yg diambil
            self.ambil = range(48, 55).index(e.key())
            self.proses()


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


class ProsesThread(QtCore.QThread):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.nasabah = nasabah
        self.ambil = ambil
        self.saldo = self.nasabah[2] - self.ambil

        gpio.init()

        # SEBAGAI INPUT
        self.LS_KATUP_ATAS_BUKA = port.PA14
        self.LS_KATUP_BAWAH_BUKA = port.PC4
        self.LS_BAKI_ATAS = port.PA2
        # self.LS_BAKI_BAWAH = port.PC7

        # SEBAGAI OUTPUT
        self.MOTOR_KATUP_ATAS = port.PA6
        self.ARAH_MOTOR_KATUP_ATAS = port.PA1
        self.MOTOR_KATUP_BAWAH = port.PA0
        self.ARAH_MOTOR_KATUP_BAWAH = port.PA3
        self.MOTOR_BAKI = port.PC0
        self.POWER_2_LITER = port.PD14
        self.POWER_3_LITER = port.PA13

        gpio.setcfg(self.LS_KATUP_ATAS_BUKA, gpio.INPUT)
        gpio.setcfg(self.LS_KATUP_BAWAH_BUKA, gpio.INPUT)
        gpio.setcfg(self.LS_BAKI_ATAS, gpio.INPUT)
        # gpio.setcfg(self.LS_BAKI_BAWAH, gpio.INPUT)

        gpio.pullup(self.LS_KATUP_ATAS_BUKA, gpio.PULLUP)
        gpio.pullup(self.LS_KATUP_BAWAH_BUKA, gpio.PULLUP)
        gpio.pullup(self.LS_BAKI_ATAS, gpio.PULLUP)
        # gpio.pullup(self.LS_BAKI_BAWAH, gpio.PULLUP)

        gpio.setcfg(self.MOTOR_KATUP_ATAS, gpio.OUTPUT)
        gpio.setcfg(self.ARAH_MOTOR_KATUP_ATAS, gpio.OUTPUT)
        gpio.setcfg(self.MOTOR_KATUP_BAWAH, gpio.OUTPUT)
        gpio.setcfg(self.ARAH_MOTOR_KATUP_BAWAH, gpio.OUTPUT)
        gpio.setcfg(self.MOTOR_BAKI, gpio.OUTPUT)
        gpio.setcfg(self.POWER_2_LITER, gpio.OUTPUT)
        gpio.setcfg(self.POWER_3_LITER, gpio.OUTPUT)

        # reset output ke low semua untuk motor (just in case)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.MOTOR_BAKI, gpio.LOW)
        gpio.output(self.POWER_2_LITER, gpio.LOW)
        gpio.output(self.POWER_3_LITER, gpio.LOW)

    def __del__(self):
        # reset ke posisi default
        # matikan motor dulu
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.MOTOR_BAKI, gpio.LOW)
        gpio.output(self.POWER_2_LITER, gpio.LOW)
        gpio.output(self.POWER_3_LITER, gpio.LOW)
        self.wait()

    def buka_katup_atas(self):
        if gpio.input(self.LS_KATUP_ATAS_BUKA) == 0:
            return
        gpio.output(self.ARAH_MOTOR_KATUP_ATAS, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(0.05)
        while gpio.input(self.LS_KATUP_ATAS_BUKA) == 1:
            pass
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)

    def tutup_katup_atas(self):
        gpio.output(self.ARAH_MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.HIGH)
        time.sleep(0.49)
        gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
        gpio.output(self.ARAH_MOTOR_KATUP_ATAS, gpio.LOW)

    def buka_katup_bawah(self):
        if gpio.input(self.LS_KATUP_BAWAH_BUKA) == 0:
            return
        gpio.output(self.ARAH_MOTOR_KATUP_BAWAH, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(0.05)
        while gpio.input(self.LS_KATUP_BAWAH_BUKA) == 1:
            pass
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)

    def tutup_katup_bawah(self):
        gpio.output(self.ARAH_MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.HIGH)
        time.sleep(0.6)
        gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
        gpio.output(self.ARAH_MOTOR_KATUP_BAWAH, gpio.LOW)

    # def naikkan_baki(self):
    #     gpio.output(self.MOTOR_BAKI, gpio.HIGH)
    #     time.sleep(0.05)
    #     while gpio.input(self.LS_BAKI_ATAS) == 1:
    #         pass
    #     time.sleep(1.2)
    #     gpio.output(self.MOTOR_BAKI, gpio.LOW)
    #     time.sleep(2.2)
    #     gpio.output(self.MOTOR_BAKI, gpio.HIGH)
    #     time.sleep(0.05)
    #     gpio.output(self.MOTOR_BAKI, gpio.LOW)

    def naikkan_baki(self):
        gpio.output(self.MOTOR_BAKI, gpio.HIGH)
        time.sleep(0.3)
        gpio.output(self.MOTOR_BAKI, gpio.LOW)
        time.sleep(2)
        gpio.output(self.MOTOR_BAKI, gpio.HIGH)
        time.sleep(0.05)
        while gpio.input(self.LS_BAKI_ATAS) == 1:
            pass
        time.sleep(1.2)
        gpio.output(self.MOTOR_BAKI, gpio.LOW)
        time.sleep(2.25)
        gpio.output(self.MOTOR_BAKI, gpio.HIGH)
        time.sleep(0.05)
        gpio.output(self.MOTOR_BAKI, gpio.LOW)

    def run(self):
        self.emit(QtCore.SIGNAL('infoProses'), "SEDANG MEMPROSES. SILAKAN TUNGGU. SIAPKAN WADAH.")

        if self.ambil == 2:
            gpio.output(self.POWER_2_LITER, gpio.HIGH)
            gpio.output(self.POWER_3_LITER, gpio.LOW)

        if self.ambil == 3:
            gpio.output(self.POWER_2_LITER, gpio.LOW)
            gpio.output(self.POWER_3_LITER, gpio.HIGH)

        # ulang sesuai jumlah yang diambil
        try:
            for i in range(self.ambil):
                self.buka_katup_atas()
                time.sleep(0.5)
                self.tutup_katup_atas()
                time.sleep(0.5)
                self.buka_katup_bawah()
                time.sleep(1)
                self.tutup_katup_bawah()
                time.sleep(5)
                self.naikkan_baki()

            # simpan log di database, update saldo
            db = Database()
            db_con = db.connect()
            cur = db_con.cursor()
            cur.execute("UPDATE nasabah SET saldo = %s WHERE id = %s", (self.saldo, self.nasabah[0]))
            cur.execute(
                "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ambil', %s)",
                (self.nasabah[0], self.ambil)
            )
            cur.close()
            db_con.commit()
            db_con.close()

        except SystemExit:
            # reset ke posisi default
            # matikan motor dulu
            gpio.output(self.MOTOR_KATUP_ATAS, gpio.LOW)
            gpio.output(self.MOTOR_KATUP_BAWAH, gpio.LOW)
            gpio.output(self.MOTOR_BAKI, gpio.LOW)


class Proses(QtGui.QWidget, proses_ui.Ui_Form):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.nasabah = nasabah
        self.ambil = ambil
        self.saldo = self.nasabah[2] - ambil
        self.showFullScreen()

        self.proses_thread = ProsesThread(self.nasabah, self.ambil)
        self.connect(self.proses_thread, QtCore.SIGNAL('infoProses'), self.update_info)
        self.connect(self.proses_thread, QtCore.SIGNAL('finished()'), self.selesai)
        self.proses_thread.start()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()

    def keypad_pressed_event(self, key):
        if key == 'A':
            self.proses_thread.terminate()

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
            [1, 2, 3, 'A'],
            [4, 5, 6, 'B'],
            [7, 8, 9, 'C'],
            ['*', 0, '#', 'D']
        ]

        self.row = [port.PG7, port.PG6, port.PA20, port.PA10]
        self.col = [port.PG9, port.PA9, port.PA8, port.PG8]

        gpio.init()

        for i in range(4):
            gpio.setcfg(self.col[i], gpio.OUTPUT)
            gpio.output(self.col[i], 1)

            gpio.setcfg(self.row[i], gpio.INPUT)
            gpio.pullup(self.row[i], gpio.PULLUP)

    def __del__(self):
        self.exiting = True
        self.wait()

    def milisecs(self, start_time):
        dt = datetime.now() - start_time
        return dt.microseconds/1000

    def run(self):
        while not self.exiting:
            last_input = datetime.now()
            for j in range(4):
                gpio.output(self.col[j], 0)

                for i in range(4):
                    if gpio.input(self.row[i]) == 0:
                        key = self.matrix[i][j]
                        self.emit(QtCore.SIGNAL('keypadPressed'), key)
                        while self.milisecs(last_input) < 100:
                            pass

                gpio.output(self.col[j], 1)
                time.sleep(0.05)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Main()
    sys.exit(app.exec_())