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
import binascii
import PN532
import RPi.GPIO as GPIO
import MySQLdb
import subprocess
import requests
import json
from threading import Thread
import os.path
import logging


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
        logger.debug("Reading keypad input on main window...")
        self.keypad_thread.start()

        self.scan_thread = ScanThread()
        self.connect(self.scan_thread, QtCore.SIGNAL('cardDetected'), self.card_detected)
        self.connect(self.scan_thread, QtCore.SIGNAL('updateInfo'), self.update_info)
        logger.debug("Starting scanning NFC card...")
        self.scan_thread.start()

    def keypad_pressed_event(self, key):
        self.password += str(key)

        if self.password == '*11121#':
            logger.info("Exit application via keypad...")
            exit(0)

        if self.password == '*11123#':
            self.keypad_thread.terminate()
            self.scan_thread.terminate()
            self.close()
            logger.info("Restarting application...")
            subprocess.call(['python', '/home/pi/ATMB/main-3l.py'])

        if self.password == '*11124#':
            logger.info("Restarting machine...")
            subprocess.call(['sudo', 'reboot'])

        if self.password == '*11125#':
            logger.info("Shutting down machine...")
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])

    def card_detected(self, nasabah):
        logger.info("NFC Card detected!")
        self.timer.stop()
        self.keypad_thread.terminate()
        self.scan_thread.terminate()
        logger.debug("Opening input pin window...")
        self.window = InputPin(nasabah)
        logger.debug("Input pin window opened")
        logger.debug("Closing main window...")
        self.close()
        logger.debug("Main window closed")

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

        self.info.setText("SELAMAT DATANG. MASUKKAN PIN ANDA")
        self.showFullScreen()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        logger.debug("Reading keypad input on input pin window...")
        self.keypad_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(20000)

    def time_out(self):
        logger.debug("Input pin timeout...")
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
            logger.debug("Nasabah: " + nasabah[1] + ", PIN: " + self.entered_pin)
            cur = db.cursor()
            cur.execute(
                "SELECT * FROM nasabah where id = %s AND pin = AES_ENCRYPT(%s, UNHEX(%s))",
                (self.nasabah[0], self.entered_pin, config["db"]["key"])
            )

            res = cur.fetchone()
            cur.close()

            if res:
                logger.debug("PIN OK!")
                self.timer.stop()
                self.keypad_thread.terminate()
                logger.debug("Opening main menu window...")
                self.menu = MainMenu(self.nasabah)
                self.close()

            else:
                logger.debug("PIN FAILED!")
                self.info.setText("PIN ANDA SALAH. SILAKAN ULANGI MASUKKAN PIN ANDA")
                self.pin.setText('----')
                self.entered_pin = ''
                self.masked_pin = ''

    def keypad_pressed_event(self, key):
        if key == '*':
            self.ulangi()

        if key == '#':
            self.kembali()

        if key in range(10):
            self.input_pin(key)


class MainMenu(QtGui.QWidget, menu_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.info.setText("")
        self.showFullScreen()

        self.keypad_thread = KeypadThread()
        self.connect(self.keypad_thread, QtCore.SIGNAL('keypadPressed'), self.keypad_pressed_event)
        self.keypad_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(20000)

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
        logger.debug("Nasabah ID : " + str(self.nasabah[0]) + " ambil beras")
        if self.nasabah[2] == 0:
            logger.debug("Nasabah ID :" + str(self.nasabah[0]) + " transaksi di tolak. Saldo 0")
            self.info.setText("MAAF, TRANSAKSI DITOLAK. SALDO ANDA 0.")
            return

        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Proses(self.nasabah)
        self.close()

    def cek_saldo(self):
        logger.debug("Nasabah ID : " + str(self.nasabah[0]) + " cek saldo")
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Saldo(self.nasabah)
        self.close()

    def ubah_pin(self):
        logger.debug("Nasabah ID : " + str(self.nasabah[0]) + " ubah PIN")
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = UbahPin(self.nasabah)
        self.close()

    def selesai(self):
        logger.debug("Nasabah ID : " + str(self.nasabah[0]) + " selesai transaksi")
        self.timer.stop()
        self.keypad_thread.terminate()
        self.window = Main()
        self.close()


class Saldo(QtGui.QWidget, saldo_ui.Ui_Form):
    def __init__(self, nasabah, additional_info=''):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = %s", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()

        self.saldo.setText('{} LITER'.format(self.nasabah[2]))
        self.info.setText(additional_info + ' ' + self.info.text())
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
        self.timer.start(20000)

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
                    cur = db.cursor()
                    cur.execute("UPDATE nasabah SET pin = AES_ENCRYPT(%s, UNHEX(%s)) "
                                "WHERE id = %s", (self.entered_pin, config["db"]["key"], self.nasabah[0]))
                    cur.execute(
                        "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ganti pin', 0)",
                        (self.nasabah[0],)
                    )
                    cur.close()
                    db.commit()

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
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        while not self.exiting:
            try:
                uid = pn532.read_passive_target()
            except Exception as e:
                self.emit(QtCore.SIGNAL('updateInfo'), 'GAGAL MENGINISIALISASI NFC')
                time.sleep(3)
                continue

            if uid is "no_card":
                continue

            card_id = str(binascii.hexlify(uid))
            cur = db.cursor()
            cur.execute(
                "SELECT * FROM nasabah WHERE card_id = AES_ENCRYPT(%s, UNHEX(%s))",
                (card_id, config["db"]["key"])
            )
            nasabah = cur.fetchone()
            cur.close()

            if nasabah:
                self.emit(QtCore.SIGNAL('cardDetected'), nasabah)
                break

            else:
                self.emit(QtCore.SIGNAL('updateInfo'), "KARTU TIDAK TERDAFTAR")
                time.sleep(3)
                self.emit(QtCore.SIGNAL('updateInfo'), "TEMPELKAN KARTU ATMB ANDA...")


class ProsesThread(QtCore.QThread):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.nasabah = nasabah
        self.saldo = self.nasabah[2] - config["scale"]

    def run(self):
        self.emit(QtCore.SIGNAL('infoProses'), "SEDANG MEMPROSES. SILAKAN TUNGGU...")

        # buka katup
        GPIO.output(config["gpio_pin"]["motor_direction"], 1)
        time.sleep(0.5)

        # hidupkan motor selama n detik
        GPIO.output(config["gpio_pin"]["motor_on"], 1)
        time.sleep(config["timer_calibartion"]["open"])

        # matikan motor
        GPIO.output(config["gpio_pin"]["motor_on"], 0)

        # tunggu sampai beras turun semua
        time.sleep(config["timer_calibartion"]["wait"])

        # tutup katup
        GPIO.output(config["gpio_pin"]["motor_direction"], 0)
        time.sleep(0.5)

        # hidupkan motor n detik
        GPIO.output(config["gpio_pin"]["motor_on"], 1)
        time.sleep(config["timer_calibartion"]["close"])

        # matikan motor
        GPIO.output(config["gpio_pin"]["motor_on"], 0)
        GPIO.output(config["gpio_pin"]["motor_direction"], 1)

        cur = db.cursor()
        cur.execute("UPDATE nasabah SET saldo = %s WHERE id = %s", (self.saldo, self.nasabah[0]))
        cur.execute(
            "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ambil', %s)",
            (self.nasabah[0], config["scale"])
        )
        cur.close()
        db.commit()

        try:
            data = {"id": config["id"], "saldo": config["scale"]}
            r = requests.post(config["api_url"] + '/atm/update')
        except Exception as e:
            pass


class Proses(QtGui.QWidget, proses_ui.Ui_Form):
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.showFullScreen()

        self.proses_thread = ProsesThread(nasabah)
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

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        time.sleep(0.5)
        while not self.exiting:
            for j in range(len(config["gpio_pin"]["keypad_col"])):
                GPIO.output(config["gpio_pin"]["keypad_col"][j], 0)

                for i in range(len(config["gpio_pin"]["keypad_row"])):
                    if GPIO.input(config["gpio_pin"]["keypad_row"][i]) == 0:
                        key = keypad_matrix[i][j]
                        self.emit(QtCore.SIGNAL('keypadPressed'), key)
                        time.sleep(0.27)

                GPIO.output(config["gpio_pin"]["keypad_col"][j], 1)
                time.sleep(0.03)


def scan_card():
    while True:
        uid = pn532.read_passive_target()

        if uid is "no_card":
            continue

        return str(binascii.hexlify(uid))

def card_is_registered(card_id):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM nasabah WHERE card_id = AES_ENCRYPT(%s, UNHEX(%s))",
        (card_id, config["db"]["key"])
    )
    nasabah = cur.fetchone()
    cur.close()

    return nasabah

def console():
    try:
        while True:
            cmd = raw_input('atmb> ')

            if cmd == "daftar":
                nama = raw_input('Nama: ')

                if not nama:
                    continue

                print "Tempelkan kartu ATMB..."
                card_id = scan_card()

                if card_is_registered(card_id):
                    print "Pendaftaran gagal. Kartu telah terdaftar"
                    continue

                cur = db.cursor()
                cur.execute(
                    "INSERT INTO nasabah (nama, saldo, pin, card_id, alamat) VALUES (%s, 15, AES_ENCRYPT('1234', UNHEX(%s)), AES_ENCRYPT(%s, UNHEX(%s)), '-')",
                    (nama, config["db"]["key"], card_id, config["db"]["key"])
                )
                cur.close()
                db.commit()

                print "Pendaftaran Berhasil";

            elif cmd == "quit":
                print "Bye"
                break

    except KeyboardInterrupt:
        print "Bye"

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for i in range(len(config["gpio_pin"]["keypad_row"])):
        GPIO.setup(config["gpio_pin"]["keypad_row"][i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for i in range(len(config["gpio_pin"]["keypad_col"])):
        GPIO.setup(config["gpio_pin"]["keypad_col"][i], GPIO.OUT)
        GPIO.output(config["gpio_pin"]["keypad_col"][i], 1)

    GPIO.setup(config["gpio_pin"]["motor_direction"], GPIO.OUT)
    GPIO.setup(config["gpio_pin"]["motor_on"], GPIO.OUT)

    # relay koplak
    GPIO.output(config["gpio_pin"]["motor_direction"], 1)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('atmb.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        logger.debug("Reading config file...")
        with open(config_file_path) as config_file:
            config = json.load(config_file)
    except Exception as e:
        logger.error("Gagal membuka file konfigurasi (config.json)")
        exit()

    if config["db"]["driver"] == "mysql":
        try:
            logger.debug("Connecting to mysql database...")
            db = MySQLdb.connect(
                host=config["db"]["host"],
                user=config["db"]["user"],
                passwd=config["db"]["pass"],
                db=config["db"]["name"]
            )
            logger.debug("Database connected")
        except Exception as e:
            logger.error("Koneksi ke database gagal. Cek konfigurasi di file config.json")
            exit()
    else:
        logger.error("Hanya bisa memakai mysql")
        exit()

    # initiate nfc
    logger.debug("Waiting NFC ready...")
    time.sleep(3)
    try:
        logger.debug("Initializing NFC Reader...")
        pn532 = PN532.PN532(config["device"]["nfc"], 115200)
        pn532.begin()
        pn532.SAM_configuration()
        logger.debug("NFC Reader found!")
    except Exception as e:
        logger.error("NFC Reader tidak ditemukan")
        exit()

    keypad_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        ['*', 0, '#']
    ]

    logger.debug("Initializing GPIO...")
    init_gpio()
    logger.debug("GPIO Initialized...")

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        logger.debug("Starting GUI Application...")
        app = QtGui.QApplication(sys.argv)
        ui = Main()
        sys.exit(app.exec_())

    else:
        console()
