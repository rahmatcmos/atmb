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
import MySQLdb
import subprocess
import serial
import pygame
import struct


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
        self.showFullScreen()

        pygame.mixer.init()
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/backsound.ogg")
        pygame.mixer.music.play(-1)

        self.password = ''
        self.ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
        self.update_status_beras_dan_pintu()
        self.timer_beras_dan_pintu = QtCore.QTimer()
        self.timer_beras_dan_pintu.timeout.connect(self.update_status_beras_dan_pintu)
        self.timer_beras_dan_pintu.start(5000)

    def update_status_beras_dan_pintu(self):
        # cek status beras dulu
        self.ser.write(b'\x00')
        jarak = self.ser.read()

        if len(jarak) > 0 and ord(jarak) > 61:
            self.scan_thread.terminate()
            self.info.setText("BERAS HABIS. MOHON ISI ULANG.")

        # cek status pintu
        else:
            self.ser.write(b'\x04')
            pintu = self.ser.read()

            if len(pintu) > 0 and ord(pintu) == 0:
                self.scan_thread.terminate()
                self.info.setText("MOHON TUTUP PINTU PENGISIAN BERAS")

            else:
                self.info.setText("TEMPELKAN KARTU ATMB ANDA...")
                if not self.scan_thread.isRunning():
                    self.scan_thread.start()

    def card_detected(self, nasabah):
        pygame.mixer.music.stop()
        self.timer.stop()
        self.timer_beras_dan_pintu.stop()
        self.ser.close()
        self.scan_thread.terminate()
        self.window = InputPin(nasabah)
        self.close()

    def update_info(self, info):
        self.info.setText(info)

    def update_clock(self):
        self.tanggal.setText(time.strftime("%d %b %Y"))
        self.jam.setText(time.strftime("%H:%M:%S"))

    def keyPressEvent(self, e):
        # for test only
        # if e.key() == QtCore.Qt.Key_Asterisk:
        #     db = Database()
        #     db_con = db.connect()
        #     cur = db_con.cursor()
        #     cur.execute("SELECT * FROM nasabah WHERE id = 1")
        #     nasabah = cur.fetchone()
        #     cur.close()
        #     db_con.close()
        #
        #     self.card_detected(nasabah)

        if e.key() in range(48, 58):
            self.password += chr(e.key())

            if self.password == '11123':
                pygame.mixer.music.stop()
                self.timer.stop()
                self.timer_beras_dan_pintu.stop()
                self.scan_thread.terminate()
                self.close()
                subprocess.call(['python', '/root/Desktop/ATM_BERAS/main.py'])

            if self.password == '11124':
                subprocess.call(['reboot'])

            if self.password == '11125':
                subprocess.call(['shutdown', '-h', 'now'])


class InputPin(QtGui.QWidget, input_pin_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.entered_pin = ''
        self.masked_pin = ''
        self.nasabah = nasabah

        if self.nasabah[5] == 'L':
            panggilan = 'BAPAK {}'.format(self.nasabah[1])
        else:
            panggilan = 'IBU {}'.format(self.nasabah[1])

        self.info.setText("SELAMAT DATANG, {}. MASUKKAN PIN ANDA".format(panggilan))
        self.showFullScreen()

        pygame.mixer.init()
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/input_pin.ogg")
        pygame.mixer.music.play()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
        self.window = Main()
        self.close()

    def ulangi(self):
        self.info.setText("SILAKAN ULANGI MASUKKAN PIN ANDA")
        self.pin.setText('----')
        self.entered_pin = ''
        self.masked_pin = ''
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/input_pin.ogg")
        pygame.mixer.music.play()

    def kembali(self):
        self.timer.stop()
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
                self.menu = MainMenu(self.nasabah)
                self.close()

            else:
                self.info.setText("PIN ANDA SALAH. SILAKAN ULANGI MASUKKAN PIN ANDA")
                self.pin.setText('----')
                self.entered_pin = ''
                self.masked_pin = ''
                pygame.mixer.music.load("/root/Desktop/ATM_BERAS/pin_salah.ogg")
                pygame.mixer.music.play()

    def keyPressEvent(self, e):
        pygame.mixer.music.stop()

        if e.key() == QtCore.Qt.Key_Enter:
            self.kembali()

        if e.key() in range(48, 58):
            self.input_pin(chr(e.key()))

        if e.key() == QtCore.Qt.Key_Backspace:
            self.ulangi()


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

        pygame.mixer.init()
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/main_menu.ogg")
        pygame.mixer.music.play()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
        self.window = Main()
        self.close()

    def keyPressEvent(self, e):
        pygame.mixer.music.stop()

        if e.key() == QtCore.Qt.Key_1:
            self.ambil_beras()

        if e.key() == QtCore.Qt.Key_2:
            self.cek_saldo()

        if e.key() == QtCore.Qt.Key_3:
            self.ubah_pin()

        if e.key() == QtCore.Qt.Key_4:
            self.selesai()

    def ambil_beras(self):
        self.timer.stop()
        self.window = AmbilBeras(self.nasabah)
        self.close()

    def cek_saldo(self):
        self.timer.stop()
        self.window = Saldo(self.nasabah)
        self.close()

    def ubah_pin(self):
        self.timer.stop()
        self.window = UbahPin(self.nasabah)
        self.close()

    def selesai(self):
        self.timer.stop()
        self.window = Main()
        self.close()


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

        self.saldo.setText('{} LITER'.format(self.nasabah[2]))
        self.info.setText(additional_info + ' ' + self.info.text())
        self.showFullScreen()

        pygame.mixer.init()
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/" + str(self.nasabah[2]) + "_liter.ogg")
        pygame.mixer.music.play()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(6000)

    def time_out(self):
        self.window = Main()
        self.close()

    # def keyPressEvent(self, e):
    #     if e.key() == QtCore.Qt.Key_1:
    #         self.ambil_beras()
    #
    #     if e.key() == QtCore.Qt.Key_2:
    #         self.kembali()
    #
    #     if e.key() == QtCore.Qt.Key_3:
    #         self.selesai()

    # def ambil_beras(self):
    #     self.timer.stop()
    #     self.window = AmbilBeras(self.nasabah)
    #     self.close()
    #
    # def kembali(self):
    #     self.timer.stop()
    #     self.window = MainMenu(self.nasabah)
    #     self.close()
    #
    # def selesai(self):
    #     self.timer.stop()
    #     self.window = Main()
    #     self.close()


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

        pygame.mixer.init()
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/ubah_pin_main.ogg")
        pygame.mixer.music.play()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
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
                pygame.mixer.music.load("/root/Desktop/ATM_BERAS/ubah_pin_ulang.ogg")
                pygame.mixer.music.play()
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
                    pygame.mixer.music.load("/root/Desktop/ATM_BERAS/ubah_pin_berhasil.ogg")
                    pygame.mixer.music.play()

                else:
                    self.info.setText("PIN TIDAK SAMA. SILAKAN ULANGI KEMBALI")
                    self.pin.setText("----")
                    self.ulang = 0
                    self.entered_pin = ''
                    self.confirm_pin = ''
                    self.masked_pin = ''
                    pygame.mixer.music.load("/root/Desktop/ATM_BERAS/ubah_pin_salah.ogg")
                    pygame.mixer.music.play()

    def keyPressEvent(self, e):
        pygame.mixer.music.stop()

        if e.key() == QtCore.Qt.Key_Backspace:
            self.ulangi()

        if e.key() == QtCore.Qt.Key_Enter:
            self.kembali()

        if e.key() in range(48, 58):
            self.ganti_pin(chr(e.key()))

    def ulangi(self):
        self.info.setText("SILAKAN MASUKKAN PIN BARU ANDA")
        self.pin.setText("----")
        self.entered_pin = ''
        self.confirm_pin = ''
        self.masked_pin = ''
        self.ulang = 0
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/ubah_pin_ulang.ogg")
        pygame.mixer.music.play()

    def kembali(self):
        self.timer.stop()
        self.window = MainMenu(self.nasabah)
        self.close()


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
        pygame.mixer.init()

        if self.saldo == 0:
            self.info.setText('MAAF, SISA SALDO ANDA SAAT INI ADALAH 0 LITER')
            self.satu_liter.setEnabled(False)
            self.dua_liter.setEnabled(False)
            self.tiga_liter.setEnabled(False)
            pygame.mixer.music.load("/root/Desktop/ATM_BERAS/saldo_habis.ogg")
            pygame.mixer.music.play()

        else:
            pygame.mixer.music.load("/root/Desktop/ATM_BERAS/ambil_beras.ogg")
            pygame.mixer.music.play()

        self.showFullScreen()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(60000)

    def time_out(self):
        self.window = Main()
        self.close()

    def selesai(self):
        self.timer.stop()
        self.window = Main()
        self.close()

    def kembali(self):
        self.timer.stop()
        self.window = MainMenu(self.nasabah)
        self.close()

    def proses(self):
        if self.ambil > self.saldo:
            self.info.setText('SALDO TIDAK CUKUP. SALDO ANDA TINGGAL {} LITER. '
                              'SILAKAN PILIH JUMLAH YANG SESUAI.'.format(self.saldo))
            pygame.mixer.music.load("/root/Desktop/ATM_BERAS/saldo_habis.ogg")
            pygame.mixer.music.play()

        else:
            self.timer.stop()
            self.window = Proses(self.nasabah, self.ambil)
            self.close()

    def keyPressEvent(self, e):
        pygame.mixer.music.stop()

        if e.key() == QtCore.Qt.Key_Backspace:
            self.kembali()

        if e.key() == QtCore.Qt.Key_Enter:
            self.selesai()

        if e.key() in range(48, 53) and self.saldo > 0 and e.key() > 48:
            self.ambil = range(48, 53).index(e.key())
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
            # time.sleep(3)
            # subprocess.call(['python', '/root/Desktop/ATM_BERAS/main.py'])


class ProsesThread(QtCore.QThread):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.nasabah = nasabah
        self.ambil = ambil
        self.saldo = self.nasabah[2] - self.ambil
        self.ser = serial.Serial("/dev/ttyUSB1", timeout=1)

    def __del__(self):
        self.wait()

    def run(self):
        if self.ambil == 1:
            self.ser.write(b'\x01')

        if self.ambil == 2:
            self.ser.write(b'\x02')

        if self.ambil == 3:
            self.ser.write(b'\x03')

        while self.ser.read() != '\xff':
            pass

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
        self.ser.close()


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

    def update_info(self, info):
        self.info.setText(info)

    def selesai(self):
        self.window = Saldo(self.nasabah, "SILAKAN AMBIL BERAS ANDA.")
        pygame.mixer.init()
        pygame.mixer.music.load("/root/Desktop/ATM_BERAS/akhir.ogg")
        pygame.mixer.music.play()
        self.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Main()
    sys.exit(app.exec_())


# serial
# 0 : untuk mengetahui volume beras
# 1 : ambil 1 liter
# 2 : ambil 2 liter
# 3 : ambil 3 liter
# 4 : pintu beras (0 : tertutup, 1 : terbuka)