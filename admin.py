#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import admin_ui
import form_ui
import sys
import time
from datetime import datetime
import binascii
import PN532
from config import Db


class NasabahTread(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        pass



class Admin(QtGui.QTabWidget, admin_ui.Ui_TabWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.tambah_warga_btn.clicked.connect(self.open_form)

        self.display_nasabah_list()
        self.display_user_list()
        self.display_transaksi_log()
        self.display_isi_ulang_log()
        self.display_user_log()
        self.showMaximized()

        self.nasabah_thread = NasabahThread()
        self.connect(self.nasabah_thread, QtCore.SIGNAL('nasabahAdded'), self.display_nasabah_list)
        self.nasabah_thread.start()

    def display_nasabah_list(self):
        data = self.get_nasabah_list()
        header = ["Nama", "Jenis Kelamin", "Tanggal Lahir", "Alamat", "Saldo", "Waktu Daftar"]
        self.show_data_on_table(data, header, self.nasabah_list)

    def display_user_list(self):
        data = self.get_user_list()
        header = ["Username", "Active", "Waktu Daftar"]
        self.show_data_on_table(data, header, self.user_list)

    def display_transaksi_log(self):
        data = self.get_transaksi_log()
        header = ["Waktu", "Nama", "Jenis Transaksi", "Jumlah"]
        self.show_data_on_table(data, header, self.log_list)

    def display_isi_ulang_log(self):
        data = self.get_isi_ulang_log()
        header = ["Waktu", "User", "Jumlah"]
        self.show_data_on_table(data, header, self.isi_ulang_log)

    def display_user_log(self):
        data = self.get_user_log()
        header = ["Waktu", "User", "Aktifitas"]
        self.show_data_on_table(data, header, self.log_user)

    def show_data_on_table(self, data, header, element):
        element.setRowCount(len(data))
        element.setColumnCount(len(header))
        element.setHorizontalHeaderLabels(header)

        for column, h in enumerate(header):
            for row, item in enumerate(data):
                element.setItem(row, column, QtGui.QTableWidgetItem(str(item[column])))

        element.resizeColumnsToContents()
        element.resizeRowsToContents()
        element.showMaximized()

    def open_form(self):
        self.form = FormDaftar()

    def get_nasabah_list(self):
        return self.get_db_records("SELECT nama, jenis_kelamin, tanggal_lahir, alamat, saldo, created_at "
                                   "FROM nasabah ORDER BY nama ASC")

    def get_user_list(self):
        return self.get_db_records("SELECT username, active, created_at FROM user ORDER BY username ASC")

    def get_transaksi_log(self):
        return self.get_db_records("SELECT transaksi.waktu, nasabah.nama, transaksi.jenis_transaksi, transaksi.jumlah "
                                   "FROM transaksi JOIN nasabah ON nasabah.id = transaksi.nasabah_id "
                                   "ORDER BY transaksi.waktu DESC")

    def get_isi_ulang_log(self):
        return self.get_db_records("SELECT l.waktu, u.username, l.jumlah FROM log_isi_ulang l "
                                   "JOIN user u ON u.id = l.user_id ORDER BY l.waktu DESC")

    def get_user_log(self):
        return self.get_db_records("SELECT l.waktu, u.username, l.activity FROM log_user l "
                                   "JOIN user u ON u.id = l.user_id ORDER BY l.waktu DESC")

    def get_db_records(self, sql):
        cur = Db.con.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
        return records

class FormDaftar(QtGui.QWidget, form_ui.Ui_Form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.info.setText('')
        self.pin.setText('')
        self.reset_btn.clicked.connect(self.reset_form)
        self.simpan_btn.clicked.connect(self.simpan)
        self.show()

    def simpan(self):
        if self.laki_laki.isChecked():
            jenis_kelamin = 'L'
        else:
            jenis_kelamin = 'P'

        cur = Db.con.cursor()
        cur.execute(
            "INSERT INTO nasabah (nama, jenis_kelamin, tanggal_lahir, alamat) VALUES (%s, %s, %s, %s)",
            (self.nama.text(), jenis_kelamin, self.tgl_lahir.text(), self.alamat.text())
        )
        cur.close()
        Db.con.commit()

    def reset_form(self):
        self.info.setText('')
        self.pin.setText('')
        self.nama.setText('')
        self.alamat.setText('')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Admin()
    sys.exit(app.exec_())