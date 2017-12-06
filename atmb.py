#!/usr/bin/env python

from __future__ import print_function
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
import os
import logging
import logging.handlers
from pygame import mixer


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

        try:
            self.keypad_thread.terminate()
        except Exception as e:
            logger.error("Failed to terminate keypad thread." + str(e))

        try:
            self.scan_thread.terminate()
        except Exception as e:
            logger.error("Failed to terminate scan thread." + str(e))

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

            cur = db.cursor()
            cur.execute(
                "SELECT * FROM nasabah where id = ? AND pin = ?",
                (self.nasabah[0], self.entered_pin, )
            )
            res = cur.fetchone()
            cur.close()

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
        try:
            self.keypad_thread.terminate()
        except Exception as e:
            logger.error("Failed to terminate keypad thread. " + str(e))

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
            self.window = Proses(self.nasabah, config["selection"][0])
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

        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = ?", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()

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

        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE id = ?", (nasabah[0],))
        self.nasabah = cur.fetchone()
        cur.close()

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
                    cur = db.cursor()
                    cur.execute(
                        "UPDATE nasabah SET pin = ? WHERE id = ?",
                        (self.entered_pin, self.nasabah[0])
                    )
                    cur.execute(
                        "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (?, 'ganti pin', 0)",
                        (self.nasabah[0],)
                    )
                    cur.close()
                    db.commit()

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

            cur = db.cursor()
            cur.execute("SELECT * FROM nasabah WHERE card_id = ?", (card_id,))
            nasabah = cur.fetchone()
            cur.close()

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
        self.jumlah_proses = self.ambil / config["scale"]

    def run(self):
        logger.debug("Proses ambil beras nasabah ID: " + str(self.nasabah[0]))
        self.emit(QtCore.SIGNAL('infoProses'), "SEDANG MEMPROSES. SILAKAN TUNGGU...")
        play_audio("sedang_proses.ogg")

        # asumsi jumlah ambil habis dibagi scale
        # asumsi: scale 1, pilihan ambil 1,2,3. scale 3, ga ada pilihan ambil
        for i in range(self.ambil / config["scale"]):
            # buka katup
            logger.debug("Buka katup")
            GPIO.output(config["gpio_pin"]["motor_direction"], 1)
            time.sleep(0.2)
            # hidupkan motor selama n detik
            GPIO.output(config["gpio_pin"]["motor_on"], 1)
            time.sleep(config["timer_calibration"]["open"])

            # matikan motor
            logger.debug("Tunggu beras turun")
            GPIO.output(config["gpio_pin"]["motor_on"], 0)
            # tunggu sampai beras turun semua
            time.sleep(config["timer_calibration"]["wait"])

            # tutup katup
            logger.debug("Tutup katup")
            GPIO.output(config["gpio_pin"]["motor_direction"], 0)
            time.sleep(0.2)
            # hidupkan motor n detik
            GPIO.output(config["gpio_pin"]["motor_on"], 1)
            time.sleep(config["timer_calibration"]["close"])

            # matikan motor
            GPIO.output(config["gpio_pin"]["motor_on"], 0)
            # untuk relay koplak only
            # GPIO.output(config["gpio_pin"]["motor_direction"], 1)

        cur = db.cursor()
        cur.execute(
            "UPDATE nasabah SET saldo = ? WHERE id = ?",
            (self.saldo, self.nasabah[0])
        )
        cur.execute(
            "INSERT INTO transaksi (nasabah_id, jenis_transaksi, jumlah) VALUES (?, 'ambil', ?)",
            (self.nasabah[0], self.ambil)
        )
        cur.close()
        db.commit()

        try:
            data = {"id": config["id"], "saldo": config["selection"]}
            r = requests.post(config["api_url"] + '/atm/update', data=data, timeout=3)
        except Exception as e:
            logger.debug("Failed to sync to server. " + str(e))


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

    def scan_card(self):
        while True:
            uid = pn532.read_passive_target()
            if uid is "no_card":
                continue
            return str(binascii.hexlify(uid))

    def card_is_registered(self, card_id):
        cur = db.cursor()
        cur.execute("SELECT * FROM nasabah WHERE card_id = ?", (card_id,))
        nasabah = cur.fetchone()
        cur.close()
        return nasabah

    def daftar(self):
        try:
            nama = raw_input('Nama: ')

            if not nama:
                return

            logger.info("Pendaftaran atas nama " + nama)
            print("Tempelkan kartu ATMB...")
            card_id = self.scan_card()

            if self.card_is_registered(card_id):
                logger.info("Pendaftaran gagal. Kartu telah terdaftar")
                print("Pendaftaran gagal. Kartu telah terdaftar")
                continue

            cur = db.cursor()
            cur.execute(
                "INSERT INTO nasabah (nama, saldo, pin, card_id, alamat) VALUES (?, 15, ?, ?, '-')",
                (nama, card_id)
            )
            cur.close()
            db.commit()

            logger.info("Pendaftaran atas nama " + nama + " Berhasil!")
            print("Pendaftaran Berhasil")

        except KeyboardInterrupt:
            return

    def test_keypad(self):
        try:
            while True:
                for j in range(len(config["gpio_pin"]["keypad_col"])):
                    GPIO.output(config["gpio_pin"]["keypad_col"][j], 0)

                    for i in range(len(config["gpio_pin"]["keypad_row"])):
                        if GPIO.input(config["gpio_pin"]["keypad_row"][i]) == 0:
                            key = keypad_matrix[i][j]
                            print(key)
                            time.sleep(0.27)

                    GPIO.output(config["gpio_pin"]["keypad_col"][j], 1)
                    time.sleep(0.03)

        except KeyboardInterrupt:
            return

    def test_relay(self):
        try:
            print("1. Relay Motor ON/OF")
            print("2. Relay Arah Motor maju/mundur")
        except KeyboardInterrupt:
            return

    def test_motor(self):
        pass

    def test_nfc(self):
        print("Tempelkan kartu...")
        try:
            card_id = self.scan_card()
            nasabah = self.card_is_registered()

            if nasabah is None:
                print("Kartu belum terdaftar")
            else:
                print("Kartu terdaftar atas nama", nasabah[1])

        except KeyboardInterrupt:
            return

    def test_audio(self):
        try:
            audios = os.listdir(os.path.join(os.path.dirname(__file__), "audio"))
            data = [["INDEX", "NAMA FILE"]]

            for i, f in enumerate(audios):
                data.append([str(i), f])

            table = AsciiTable(data)
            print(table.table)

            audio = raw_input("Masukkan index file audio yang akan anda mainkan : ")

            play_audio(int(audio))

        except Exception as e:
            mixer.music.stop()
            print(str(e))
            return

    def sync_data(self):
        pass

    def drain(self):
        try:
            confirm = raw_input("Anda yakin? (y/n) : ")

            if confirm != "y":
                return



        except Exception as e:
            return

    def simulasi(self):
        try:
            confirm = raw_input('Anda yakin? (y/n) :')
            if confirm != "y":
                return

            # buka katup
            print("Membuka katup...")
            GPIO.output(config["gpio_pin"]["motor_direction"], 1)
            time.sleep(0.2)
            # hidupkan motor selama n detik
            GPIO.output(config["gpio_pin"]["motor_on"], 1)
            time.sleep(config["timer_calibration"]["open"])

            # matikan motor
            print("Tunggu beras turun")
            GPIO.output(config["gpio_pin"]["motor_on"], 0)
            # tunggu sampai beras turun semua
            time.sleep(config["timer_calibration"]["wait"])

            # tutup katup
            print("Tutup katup")
            GPIO.output(config["gpio_pin"]["motor_direction"], 0)
            time.sleep(0.2)
            # hidupkan motor n detik
            GPIO.output(config["gpio_pin"]["motor_on"], 1)
            time.sleep(config["timer_calibration"]["close"])

            # matikan motor
            GPIO.output(config["gpio_pin"]["motor_on"], 0)
            # untuk relay koplak only
            # GPIO.output(config["gpio_pin"]["motor_direction"], 1)

        except KeyboardInterrupt:
            return

    def help(self):
        data = [
            ['PERINTAH', 'KETERANGAN'],
            ['?', 'Menampilkan pesan ini'],
            ['daftar', 'Mendaftarkan kartu baru'],
            ['simulasi', 'Simulasi pengambilan beras untuk test mekanikal'],
            ['test relay', 'Untuk test relay'],
            ['test motor', 'Untuk test motor'],
            ['test keypad', 'Untuk test matix keypad'],
            ['test nfc', 'Untuk test nfc'],
            ['sync data', 'Sinkronisasi data ke server'],
            ['drain', 'Mengosongkan isi beras'],
            ['quit', 'Keluar dari progam CLI']
        ]

        table = AsciiTable(data)
        print(table.table)

    def run(self):
        try:
            while True:
                cmd = raw_input('atmb> ')

                if cmd == "daftar":
                    self.daftar()

                elif cmd == "test relay":
                    self.test_relay()

                elif cmd == "test keypad":
                    self.test_keypad()

                elif cmd == "test nfc":
                    self.test_nfc()

                elif cmd == "test audio":
                    self.test_audio()

                elif cmd == "help" or cmd == "?":
                    self.help()

                elif cmd == "quit":
                    print("Bye")
                    break

                elif cmd.strip():
                    print("Perintah tidak dikenal. Ketik '?' untuk bantuan.")

                else:
                    pass

        except KeyboardInterrupt:
            print("Bye")
            exit()


def play_audio(audio_file, loops=0):
    audio = os.path.join(os.path.dirname(__file__), "audio/" + audio_file)
    mixer.music.stop()

    if os.path.isfile(audio):
        try:
            mixer.music.load(audio)
        except Exception as e:
            logger.debug("Failed to play " + audio_file + " : " + str(e))
            return
        mixer.music.play(loops)


if __name__ == "__main__":
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        with open(config_file_path) as config_file:
            config = json.load(config_file)
    except Exception as e:
        print("Gagal membuka file konfigurasi (config.json)" + str(e))
        exit()

    message = "Initializing logger..."
    logger.debug(message)
    print(message)

    log_level = {
        "NOTSET": 0,
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }

    log_file_path = os.path.join(os.path.dirname(__file__), 'atmb.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level[config["log_level"]])
    handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=1024000, backupCount=100)
    handler.setLevel(log_level[config["log_level"]])
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    message = "Initializing database..."
    logger.debug(message)
    print(message)

    if config["db"]["driver"] == "sqlite":
        logger.debug("Creating database schema...")
        db = sqlite3.connect(os.path.join(os.path.dirname(__file__), config["db"]["name"]), check_same_thread=False)

        db.execute("CREATE TABLE IF NOT EXISTS `penerima` ( \
            `id` INTEGER PRIMARY KEY AUTOINCREMENT, \
            `uuid` varchar(50) NULL, \
            `nama` varchar(30) NOT NULL, \
            `card_id` varchar(20) NULL, \
            `waktu_daftar` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)");

        db.execute("CREATE TABLE IF NOT EXISTS `log_transaksi` ( \
            `id` INTEGER PRIMARY KEY AUTOINCREMENT, \
            `nasabah_id` int(11) NULL, \
            `jenis_transaksi` VARCHAR(30) NOT NULL, \
            `jumlah` int(11) NULL, \
            `waktu` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")

        db.execute("CREATE TABLE IF NOT EXISTS `status` ( \
            `saldo` int(11) NOT NULL DEFAULT 0, \
            `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    else:
        message = "Hanya bisa memakai sqlite"
        print(message)
        logger.error(message)
        exit()

    logger.debug("Waiting NFC ready...")
    time.sleep(3)
    message = "Initializing NFC Reader..."
    logger.debug(message)
    print(message)

    try:
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

    message = "Initializing GPIO..."
    logger.debug(message)
    print(message)

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

    mixer.init()

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        message = "Starting GUI Application..."
        logger.debug(message)
        print(message)

        app = QtGui.QApplication(sys.argv)
        ui = Main()
        sys.exit(app.exec_())

    else:
        message = "Starting console application..."
        logger.debug(message)
        print(message)

        console = Console()
        console.run()
