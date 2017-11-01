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
import sqlite3
import subprocess
import requests
import json
import os.path
import logging
import logging.handlers
from threading import Thread
from pygame import mixer


class Database:
    def __init__(self):
        self.host = config["db"]["host"]
        self.username = config["db"]["user"]
        self.password = config["db"]["pass"]
        self.name = config["db"]["name"]
        self.con = None
        self.cur = None

    def connect(self):
        if self.con == None:
            self.con = MySQLdb.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                db=self.name
            )
        return self.con

    def query(self, query, param=None):
        self.con = self.connect()
        self.cur = self.con.cursor()
        self.cur.execute(query, param)
        return self.cur

    def fetchone():
        result = self.cur.fetchone()
        self.cur.close()
        self.con.close()
        return result

    def fetchall():
        result = self.cur.fetchall()
        self.cur.close()
        self.con.close()
        return result

    def save(self, query, param=None):
        self.con = self.connect()
        cur = self.con.cursor()
        cur.execute(query, param)
        cur.close()
        self.con.commit()
        self.con.close()

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
        logger.debug("Starting scanning NFC card...")
        self.scan_thread.start()

        play_audio("backsound.ogg")

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
            subprocess.call(['python', '/home/pi/ATMB/atmb.py'])

        if self.password == '*11124#':
            logger.info("Restarting machine...")
            subprocess.call(['sudo', 'reboot'])

        if self.password == '*11125#':
            logger.info("Shutting down machine...")
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])

    def card_detected(self, nasabah):
        logger.info("NFC Card detected! Nasabah ID: " + str(nasabah[0]))
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

        self.info.setText("SELAMAT DATANG. MASUKKAN PIN ANDA")
        self.showFullScreen()

        play_audio("masukkan_pin.ogg")

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

    def ulangi(self):
        self.info.setText("SILAKAN ULANGI MASUKKAN PIN ANDA")
        play_audio("ulangi_pin.ogg")
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
            logger.debug("Nasabah ID: " + str(self.nasabah[0]) + ", PIN: " + self.entered_pin)

            db = Database()
            con = db.connect()
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM nasabah where id = %s AND pin = AES_ENCRYPT(%s, UNHEX(%s))",
                (self.nasabah[0], self.entered_pin, config["db"]["key"])
            )
            res = cur.fetchone()
            cur.close()
            con.close()

            if res:
                logger.debug("PIN OK!")
                self.timer.stop()
                self.keypad_thread.terminate()
                self.menu = MainMenu(self.nasabah)
                self.close()

            else:
                logger.debug("PIN FAILED!")
                self.info.setText("PIN ANDA SALAH. SILAKAN ULANGI MASUKKAN PIN ANDA")
                play_audio("pin_salah.ogg")
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
        logger.debug("Nasabah ID: " + str(self.nasabah[0]) + " ambil beras")
        if self.nasabah[2] == 0:
            logger.debug("Nasabah ID: " + str(self.nasabah[0]) + " transaksi di tolak. Saldo 0")
            self.info.setText("MAAF, TRANSAKSI DITOLAK. SALDO ANDA 0.")
            play_audio("saldo_habis.ogg")
            return

        self.timer.stop()
        self.keypad_thread.terminate()

        if len(config["selection"]) == 1:
            self.window = Proses(self.nasabah, config["selection"])
        else:
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
    def __init__(self, nasabah):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        db = Database()
        con = db.connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = %s", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()
        con.close()

        logger.info("Nasabah ID: " + str(self.nasabah[0]) + ", saldo: " + str(self.nasabah[2]))
        self.saldo.setText('{} LITER'.format(self.nasabah[2]))
        self.showFullScreen()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(5000)

    def time_out(self):
        self.window = Main()
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

        if self.saldo == 0:
            self.info.setText('MAAF, SISA SALDO ANDA SAAT INI ADALAH 0 LITER')
            play_audio("saldo_habis.ogg")

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
        if key == '*':
            self.kembali()

        if key == '#':
            self.selesai()

        if key in config["selection"]:
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
            play_audio("saldo_tidak_cukup.ogg")

        else:
            self.timer.stop()
            self.keypad_thread.terminate()
            self.window = Proses(self.nasabah, self.ambil)
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
                play_audio("ulangi_pin.ogg")
                self.ulang = 1

        else:
            self.confirm_pin += str(pin)

            if len(self.confirm_pin) == 4:
                if self.confirm_pin == self.entered_pin:
                    db = Database()
                    con = db.connect()
                    cur = con.cursor()
                    cur.execute("UPDATE nasabah SET pin = AES_ENCRYPT(%s, UNHEX(%s)) "
                                "WHERE id = %s", (self.entered_pin, config["db"]["key"], self.nasabah[0]))
                    cur.execute(
                        "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ganti pin', 0)",
                        (self.nasabah[0],)
                    )
                    cur.close()
                    con.commit()
                    con.close()

                    logger.info("Nasabah ID: " + str(self.nasabah[0]) + " Ganti PIN OK!")
                    self.info.setText("PIN ANDA BERHASIL DIUBAH")
                    play_audio("pin_berhasil_diubah.ogg")
                    self.pin.setText('')

                else:
                    logger.info("Nasabah ID: " + str(self.nasabah[0]) + " Ganti PIN GAGAL! PIN tidak sama.")
                    self.info.setText("PIN TIDAK SAMA. SILAKAN ULANGI KEMBALI")
                    play_audio("pin_tidak_sama.ogg")
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
        play_audio("masukkan_pin_baru.ogg")
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
                logger.error("Gagal membaca NFC Card")
                self.emit(QtCore.SIGNAL('updateInfo'), 'GAGAL MEMBACA KARTU ATMB')
                time.sleep(3)
                self.emit(QtCore.SIGNAL('updateInfo'), 'TEMPELKAN KARTU ATMB ANDA...')
                continue

            if uid is "no_card":
                continue

            card_id = str(binascii.hexlify(uid))
            db = Database()
            con = db.connect()
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM nasabah WHERE card_id = AES_ENCRYPT(%s, UNHEX(%s))",
                (card_id, config["db"]["key"])
            )
            nasabah = cur.fetchone()
            cur.close()
            con.close()

            if nasabah:
                self.emit(QtCore.SIGNAL('cardDetected'), nasabah)
                break

            else:
                logger.info("Kartu tidak terdaftar")
                self.emit(QtCore.SIGNAL('updateInfo'), "KARTU TIDAK TERDAFTAR")
                time.sleep(3)
                self.emit(QtCore.SIGNAL('updateInfo'), "TEMPELKAN KARTU ATMB ANDA...")


class ProsesThread(QtCore.QThread):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.nasabah = nasabah
        self.ambil = ambil
        self.saldo = self.nasabah[2] - self.ambil

    def run(self):
        logger.debug("Proses ambil beras nasabah ID: " + str(self.nasabah[0]))
        self.emit(QtCore.SIGNAL('infoProses'), "SEDANG MEMPROSES. SILAKAN TUNGGU...")
        play_audio("sedang_proses.ogg")
        play_audio("backsound.ogg")

        # buka katup
        logger.debug("Buka katup")
        GPIO.output(config["gpio_pin"]["motor_direction"], 1)
        time.sleep(0.2)
        # hidupkan motor selama n detik
        GPIO.output(config["gpio_pin"]["motor_on"], 1)
        time.sleep(config["timer_calibartion"]["open"])

        # matikan motor
        logger.debug("Tunggu beras turun")
        GPIO.output(config["gpio_pin"]["motor_on"], 0)
        # tunggu sampai beras turun semua
        time.sleep(config["timer_calibartion"]["wait"])

        # tutup katup
        logger.debug("Tutup katup")
        GPIO.output(config["gpio_pin"]["motor_direction"], 0)
        time.sleep(0.2)
        # hidupkan motor n detik
        GPIO.output(config["gpio_pin"]["motor_on"], 1)
        time.sleep(config["timer_calibartion"]["close"])

        # matikan motor
        GPIO.output(config["gpio_pin"]["motor_on"], 0)
        # untuk relay koplak only
        # GPIO.output(config["gpio_pin"]["motor_direction"], 1)

        db = Database()
        con = db.connect()
        cur = con.cursor()
        cur.execute("UPDATE nasabah SET saldo = %s WHERE id = %s", (self.saldo, self.nasabah[0]))
        cur.execute(
            "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (%s, 'ambil', %s)",
            (self.nasabah[0], self.ambil)
        )
        cur.close()
        con.commit()
        con.close()

        try:
            data = {"id": config["id"], "saldo": config["scale"]}
            r = requests.post(config["api_url"] + '/atm/update')
        except Exception as e:
            pass


class Proses(QtGui.QWidget, proses_ui.Ui_Form):
    def __init__(self, nasabah, ambil):
        super(self.__class__, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.nasabah = nasabah
        self.showFullScreen()

        self.proses_thread = ProsesThread(nasabah, ambil)
        self.connect(self.proses_thread, QtCore.SIGNAL('infoProses'), self.update_info)
        self.connect(self.proses_thread, QtCore.SIGNAL('finished()'), self.selesai)
        self.proses_thread.start()

    def update_info(self, info):
        self.info.setText(info)

    def selesai(self):
        self.window = Saldo(self.nasabah)
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


class Console():
    def __init__(self):
        pass

    def daftar(self):
        nama = raw_input('Nama: ')

        if not nama:
            continue

        logger.info("Pendaftaran atas nama " + nama)
        print "Tempelkan kartu ATMB..."
        card_id = scan_card()

        if card_is_registered(card_id):
            logger.info("Pendaftaran gagal. Kartu telah terdaftar")
            print "Pendaftaran gagal. Kartu telah terdaftar"
            continue

        cur = db.cursor()
        cur.execute(
            "INSERT INTO nasabah (nama, saldo, pin, card_id, alamat) VALUES (%s, 15, AES_ENCRYPT('1234', UNHEX(%s)), AES_ENCRYPT(%s, UNHEX(%s)), '-')",
            (nama, config["db"]["key"], card_id, config["db"]["key"])
        )
        cur.close()
        db.commit()

        logger.info("Pendaftaran atas nama " + nama + " Berhasil!")
        print "Pendaftaran Berhasil"

    def run(self):
        try:
            while True:
                cmd = raw_input('atmb> ')

                if cmd == "daftar":
                    self.daftar()

                elif cmd == "quit":
                    print "Bye"
                    break

        except KeyboardInterrupt:
            print "Bye"


def scan_card():
    while True:
        uid = pn532.read_passive_target()

        if uid is "no_card":
            continue

        return str(binascii.hexlify(uid))


def play_audio(audio_file, loops=0):
    audio = os.path.join(os.path.dirname(__file__), audio_file)
    if os.path.isfile(audio):
        try:
            mixer.music.load(audio)
        except Exception as e:
            logger.debug("Failed to play " + audio_file + " : " + str(e))
            return
        mixer.music.play(loops)


def card_is_registered(card_id):
    db = Database()
    con = db.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM nasabah WHERE card_id = AES_ENCRYPT(%s, UNHEX(%s))",
        (card_id, config["db"]["key"])
    )
    nasabah = cur.fetchone()
    cur.close()
    con.close()

    return nasabah


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

    # untuk relay koplak
    # GPIO.output(config["gpio_pin"]["motor_direction"], 1)


if __name__ == "__main__":
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    log_file_path = os.path.join(os.path.dirname(__file__), 'atmb.log')

    try:
        with open(config_file_path) as config_file:
            config = json.load(config_file)
    except Exception as e:
        print "Gagal membuka file konfigurasi (config.json)" + str(e)
        exit()

    log_level = {
        "NOTSET": 0,
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level[config["log_level"]])
    handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=1024000, backupCount=100)
    handler.setLevel(log_level[config["log_level"]])
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if config["db"]["driver"] == "sqlite":
        logger.debug("Connecting to database...")
        db = sqlite3.connect(os.path.join(os.path.dirname(__file__), config["db"]["name"]), check_same_thread=False)
        logger.debug("Creating database schema...")

        db.execute("CREATE TABLE IF NOT EXISTS `penerima` ( \
            `id` INTEGER PRIMARY KEY AUTOINCREMENT, \
            `uuid` varchar(50) NULL, \
            `nama` varchar(30) NOT NULL, \
            `card_id` varchar(20) NULL, \
            `template` text NULL, \
            `template1` text NULL, \
            `active` boolean default 1, \
            `allow` boolean default 1, \
            `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
            `last_access` timestamp NULL, \
            `waktu_daftar` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)");

        db.execute("CREATE TABLE IF NOT EXISTS `log` ( \
            `id` INTEGER PRIMARY KEY AUTOINCREMENT, \
            `karyawan_id` int(11) NULL, \
            `waktu` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    else:
        message = "Hanya bisa memakai sqlite"
        print(message)
        logger.error(message)
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
        message = "NFC Reader tidak ditemukan"
        logger.error(message)
        print(message)
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
        mixer.init()
        app = QtGui.QApplication(sys.argv)
        ui = Main()
        sys.exit(app.exec_())

    else:
        console()
