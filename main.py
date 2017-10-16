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
# from datetime import datetime
import binascii
import PN532
import RPi.GPIO as GPIO
import MySQLdb
import subprocess
import serial
import pygame
import os.path
import requests


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.name = 'atmb'
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
        self.beras_habis = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.showFullScreen()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()

        self.scan_thread = ScanThread()
        self.connect(self.scan_thread, QtCore.SIGNAL('cardDetected'), self.card_detected)
        self.connect(self.scan_thread, QtCore.SIGNAL('updateInfo'), self.update_info)

        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.update_status_beras_dan_pintu()
        self.timer_beras_dan_pintu = QtCore.QTimer()
        self.timer_beras_dan_pintu.timeout.connect(self.update_status_beras_dan_pintu)
        self.timer_beras_dan_pintu.start(5000)

        # audio_file = os.path.join(os.path.dirname(__file__), 'backsound.ogg')
        # pygame.mixer.init()
        #
        # if os.path.exists(audio_file):
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play(-1)

    def update_status_beras_dan_pintu(self):
        # cek status beras dulu
        self.ser.write(b'\x00')
        jarak = self.ser.read()

        if len(jarak) > 0 and ord(jarak) > 50:
            self.beras_habis = True
            self.info.setText("BERAS HABIS. MOHON ISI ULANG.")

            try:
                r = requests.get('http://114.6.180.156/atmb/api/atm/update?id=5&status_beras=0')
            except Exception as e:
                pass

            try:
                self.scan_thread.terminate()
            except Exception as e:
                pass

        else:
            self.beras_habis = False
            self.info.setText("TEMPELKAN KARTU ATMB ANDA...")

            try:
                r = requests.get('http://114.6.180.156/atmb/api/atm/update?id=5&status_beras=1')
            except Exception as e:
                pass

            try:
                self.scan_thread.start()
            except Exception as e:
                pass

        # cek status pintu
        # else:
        #     self.ser.write(b'\x04')
        #     pintu = self.ser.read()
        #
        #     if len(pintu) > 0 and ord(pintu) == 0:
        #         self.scan_thread.terminate()
        #         self.info.setText("MOHON TUTUP PINTU PENGISIAN BERAS")
        #         r = requests.get('http://114.6.180.156/atmb/atm/update?id=3&status_pintu=0')
        #
        #     else:
        #         self.info.setText("TEMPELKAN KARTU ATMB ANDA...")
        #         if not self.scan_thread.isRunning():
        #             self.scan_thread.start()

    def keypad_pressed_event(self, key):
        self.password += str(key)

        if self.password == '*11123#':
            self.keypad_thread.terminate()
            self.scan_thread.terminate()
            self.close()
            subprocess.call(['python', '/home/pi/ATMB/main.py'])

        if self.password == '*11124#':
            subprocess.call(['reboot'])

        if self.password == '*11125#':
            subprocess.call(['shutdown', '-h', 'now'])

    def card_detected(self, nasabah):
        # pygame.mixer.music.stop()
        self.timer.stop()
        self.timer_beras_dan_pintu.stop()
        self.ser.close()
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

        # if self.nasabah[5] == 'L':
        #     panggilan = 'BAPAK {}'.format(self.nasabah[1])
        # else:
        #     panggilan = 'IBU {}'.format(self.nasabah[1])

        self.info.setText("SELAMAT DATANG. MASUKKAN PIN ANDA")
        self.showFullScreen()

        # folder = os.path.dirname(__file__)
        # audio_file = os.path.join(folder, '/input_pin.ogg')
        #
        # if os.path.exists(audio_file):
        #     pygame.mixer.init()
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()

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

        # folder = os.path.dirname(__file__)
        # audio_file = os.path.join(folder, '/input_pin.ogg')
        #
        # if os.path.exists(audio_file):
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()

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

                # folder = os.path.dirname(__file__)
                # audio_file = os.path.join(folder, '/pin_salah.ogg')
                #
                # if os.path.exists(audio_file):
                #     pygame.mixer.music.load(audio_file)
                #     pygame.mixer.music.play()

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
        # pygame.mixer.music.stop()

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

        self.showFullScreen()

        # folder = os.path.dirname(__file__)
        # audio_file = os.path.join(folder, '/main_menu.ogg')
        #
        # if os.path.exists(audio_file):
        #     pygame.mixer.init()
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()

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
        # pygame.mixer.music.stop()

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

        self.saldo.setText('{} LITER'.format(self.nasabah[2]))
        self.info.setText(additional_info + ' ' + self.info.text())
        self.showFullScreen()

        # folder = os.path.dirname(__file__)

        # if 0 < self.nasabah[2] <= 15:
        #     audio_file = os.path.join(folder, str(self.nasabah[2]) + "_liter.ogg")
        #     if os.path.exists(audio_file):
        #         pygame.mixer.init()
        #         pygame.mixer.music.load(audio_file)
        #         pygame.mixer.music.play()
        #
        # else:
        #     audio_file = os.path.join(folder, "/saldo_habis.ogg")
        #     if os.path.exists(audio_file):
        #         pygame.mixer.music.load(audio_file)
        #         pygame.mixer.music.play()

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

        # folder = os.path.dirname(__file__)
        # audio_file = os.path.join(folder, '/ubah_pin_main.ogg')
        #
        # if os.path.exists(audio_file):
        #     pygame.mixer.init()
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()

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

                # folder = os.path.dirname(__file__)
                # audio_file = os.path.join(folder, '/ubah_pin_ulang.ogg')
                #
                # if os.path.exists(audio_file):
                #     pygame.mixer.music.load(audio_file)
                #     pygame.mixer.music.play()
                #
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

                    # folder = os.path.dirname(__file__)
                    # audio_file = os.path.join(folder, '/ubah_pin_berhasil.ogg')
                    #
                    # if os.path.exists(audio_file):
                    #     pygame.mixer.music.load(audio_file)
                    #     pygame.mixer.music.play()

                else:
                    self.info.setText("PIN TIDAK SAMA. SILAKAN ULANGI KEMBALI")
                    self.pin.setText("----")
                    self.ulang = 0
                    self.entered_pin = ''
                    self.confirm_pin = ''
                    self.masked_pin = ''

                    # folder = os.path.dirname(__file__)
                    # audio_file = os.path.join(folder, '/ubah_pin_salah.ogg')
                    #
                    # if os.path.exists(audio_file):
                    #     pygame.mixer.music.load(audio_file)
                    #     pygame.mixer.music.play()

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

        # folder = os.path.dirname(__file__)
        # audio_file = os.path.join(folder, '/ubah_pin_ulang.ogg')
        #
        # if os.path.exists(audio_file):
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()

    def kembali(self):
        self.timer.stop()
        self.keypad_thread.terminate()
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
        # pygame.mixer.init()

        if self.saldo == 0:
            self.info.setText('MAAF, SISA SALDO ANDA SAAT INI ADALAH 0 LITER')

            # folder = os.path.dirname(__file__)
            # file_audio = os.path.join(folder, '/saldo_habis.ogg')
            #
            # if os.path.exists(file_audio):
            #     pygame.mixer.music.load(file_audio)
            #     pygame.mixer.music.play()

        else:
            pass
            # folder = os.path.dirname(__file__)
            # file_audio = os.path.join(folder, '/ambil_beras.ogg')
            #
            # if os.path.exists(file_audio):
            #     pygame.mixer.music.load(file_audio)

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

            # folder = os.path.dirname(__file__)
            # file_audio = os.path.join(folder, '/saldo_habis.ogg')
            #
            # if os.path.exists(file_audio):
            #     pygame.mixer.music.load(file_audio)
            #     pygame.mixer.music.play()

        else:
            self.timer.stop()
            self.keypad_thread.terminate()
            self.window = Proses(self.nasabah, self.ambil)
            self.close()

    def keypad_pressed_event(self, key):
        # pygame.mixer.music.stop()

        if key == '*':
            self.kembali()

        if key == '#':
            self.selesai()

        if key in range(1, 4):
            self.ambil = key
            self.proses()


class ScanThread(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.nfc_port = "/dev/serial0"
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
            # subprocess.call(['python', '/home/pi/ATMB/main.py'])


class ProsesThread(QtCore.QThread):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.nasabah = nasabah
        self.ambil = ambil
        self.saldo = self.nasabah[2] - self.ambil
        self.ser = serial.Serial("/dev/ttyUSB0", timeout=1)

    def run(self):
        self.emit(QtCore.SIGNAL('infoProses'), "SEDANG MEMPROSES. SILAKAN TUNGGU...")

        for i in range(1, self.ambil + 1):
            # buka
            self.ser.write(b'\x05') # mundur
            self.ser.write(b'\x07') # motor hidup
            time.sleep(21) # tunggu buka sempurna
            self.ser.write(b'\x08') # motor mati
            time.sleep(10) # tunggu beras turun

            # tutup
            self.ser.write(b'\x06')  # maju
            self.ser.write(b'\x07')  # motor hidup
            time.sleep(21)  # tunggu buka sempurna
            self.ser.write(b'\x08')  # motor mati
            time.sleep(1)

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

        try:
            r = requests.get('http://114.6.180.156/atmb/api/atm/update?id=5&saldo='+str(self.ambil))
        except Exception as e:
            pass

        self.ser.close()


class Proses(QtGui.QWidget, proses_ui.Ui_Form):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.ambil = ambil
        self.saldo = self.nasabah[2] - self.ambil
        self.showFullScreen()

        self.proses_thread = ProsesThread(self.nasabah, self.ambil)
        self.connect(self.proses_thread, QtCore.SIGNAL('infoProses'), self.update_info)
        self.connect(self.proses_thread, QtCore.SIGNAL('finished()'), self.selesai)
        self.proses_thread.start()

    def update_info(self, info):
        self.info.setText(info)

    def selesai(self):
        self.window = Saldo(self.nasabah, "SILAKAN AMBIL BERAS ANDA.")
        # folder = os.path.dirname(__file__)
        # file_audio = os.path.join(folder, '/akhir.ogg')
        #
        # if os.path.exists(file_audio):
        #     pygame.mixer.init()
        #     pygame.mixer.music.load(file_audio)
        #     pygame.mixer.music.play()

        self.close()


class KeypadThread(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.exiting = False

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

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        time.sleep(0.5)
        while not self.exiting:
            for j in range(len(self.col)):
                GPIO.output(self.col[j], 0)

                for i in range(len(self.row)):
                    if GPIO.input(self.row[i]) == 0:
                        key = self.matrix[i][j]
                        self.emit(QtCore.SIGNAL('keypadPressed'), key)
                        time.sleep(0.27)

                GPIO.output(self.col[j], 1)
                time.sleep(0.03)


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
# 5 : mundur
# 6 : maju
# 7 : on motor
# 8 : off motor

