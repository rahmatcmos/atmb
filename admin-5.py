# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(596, 513)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cari = QtWidgets.QLineEdit(self.tab)
        self.cari.setObjectName("cari")
        self.horizontalLayout.addWidget(self.cari)
        self.cari_warga = QtWidgets.QPushButton(self.tab)
        self.cari_warga.setObjectName("cari_warga")
        self.horizontalLayout.addWidget(self.cari_warga)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.nasabah_list = QtWidgets.QTableWidget(self.tab)
        self.nasabah_list.setObjectName("nasabah_list")
        self.nasabah_list.setColumnCount(0)
        self.nasabah_list.setRowCount(0)
        self.verticalLayout_4.addWidget(self.nasabah_list)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tambah_warga_btn = QtWidgets.QPushButton(self.tab)
        self.tambah_warga_btn.setObjectName("tambah_warga_btn")
        self.verticalLayout_2.addWidget(self.tambah_warga_btn)
        self.edit_warga_btn = QtWidgets.QPushButton(self.tab)
        self.edit_warga_btn.setObjectName("edit_warga_btn")
        self.verticalLayout_2.addWidget(self.edit_warga_btn)
        self.hapus_warga_btn = QtWidgets.QPushButton(self.tab)
        self.hapus_warga_btn.setObjectName("hapus_warga_btn")
        self.verticalLayout_2.addWidget(self.hapus_warga_btn)
        self.ganti_pin = QtWidgets.QPushButton(self.tab)
        self.ganti_pin.setObjectName("ganti_pin")
        self.verticalLayout_2.addWidget(self.ganti_pin)
        self.ganti_kartu = QtWidgets.QPushButton(self.tab)
        self.ganti_kartu.setObjectName("ganti_kartu")
        self.verticalLayout_2.addWidget(self.ganti_kartu)
        self.hapus_semua_warga_btn = QtWidgets.QPushButton(self.tab)
        self.hapus_semua_warga_btn.setObjectName("hapus_semua_warga_btn")
        self.verticalLayout_2.addWidget(self.hapus_semua_warga_btn)
        self.download_warga_btn = QtWidgets.QPushButton(self.tab)
        self.download_warga_btn.setObjectName("download_warga_btn")
        self.verticalLayout_2.addWidget(self.download_warga_btn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        TabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.username = QtWidgets.QLineEdit(self.tab_2)
        self.username.setObjectName("username")
        self.horizontalLayout_2.addWidget(self.username)
        self.password = QtWidgets.QLineEdit(self.tab_2)
        self.password.setObjectName("password")
        self.horizontalLayout_2.addWidget(self.password)
        self.active = QtWidgets.QCheckBox(self.tab_2)
        self.active.setObjectName("active")
        self.horizontalLayout_2.addWidget(self.active)
        self.save_user_btn = QtWidgets.QPushButton(self.tab_2)
        self.save_user_btn.setObjectName("save_user_btn")
        self.horizontalLayout_2.addWidget(self.save_user_btn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.user_list = QtWidgets.QTableWidget(self.tab_2)
        self.user_list.setObjectName("user_list")
        self.user_list.setColumnCount(0)
        self.user_list.setRowCount(0)
        self.verticalLayout_7.addWidget(self.user_list)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.edit_user_btn = QtWidgets.QPushButton(self.tab_2)
        self.edit_user_btn.setObjectName("edit_user_btn")
        self.verticalLayout_3.addWidget(self.edit_user_btn)
        self.hapus_user_btn = QtWidgets.QPushButton(self.tab_2)
        self.hapus_user_btn.setObjectName("hapus_user_btn")
        self.verticalLayout_3.addWidget(self.hapus_user_btn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        TabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.search_log = QtWidgets.QLineEdit(self.tab_3)
        self.search_log.setObjectName("search_log")
        self.horizontalLayout_3.addWidget(self.search_log)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.log_list = QtWidgets.QTableWidget(self.tab_3)
        self.log_list.setObjectName("log_list")
        self.log_list.setColumnCount(0)
        self.log_list.setRowCount(0)
        self.verticalLayout_5.addWidget(self.log_list)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_6.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_6.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        TabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cari_log_isi_ulang = QtWidgets.QLineEdit(self.tab_4)
        self.cari_log_isi_ulang.setObjectName("cari_log_isi_ulang")
        self.horizontalLayout_7.addWidget(self.cari_log_isi_ulang)
        self.cari_log_isi_ulang_btn = QtWidgets.QPushButton(self.tab_4)
        self.cari_log_isi_ulang_btn.setObjectName("cari_log_isi_ulang_btn")
        self.horizontalLayout_7.addWidget(self.cari_log_isi_ulang_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.isi_ulang_log = QtWidgets.QTableWidget(self.tab_4)
        self.isi_ulang_log.setObjectName("isi_ulang_log")
        self.isi_ulang_log.setColumnCount(0)
        self.isi_ulang_log.setRowCount(0)
        self.verticalLayout.addWidget(self.isi_ulang_log)
        self.horizontalLayout_8.addLayout(self.verticalLayout)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.download_log_isi_ulang_btn = QtWidgets.QPushButton(self.tab_4)
        self.download_log_isi_ulang_btn.setObjectName("download_log_isi_ulang_btn")
        self.verticalLayout_9.addWidget(self.download_log_isi_ulang_btn)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem3)
        self.horizontalLayout_8.addLayout(self.verticalLayout_9)
        TabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.cari_log_user = QtWidgets.QLineEdit(self.tab_5)
        self.cari_log_user.setObjectName("cari_log_user")
        self.horizontalLayout_9.addWidget(self.cari_log_user)
        self.cari_log_user_btn = QtWidgets.QPushButton(self.tab_5)
        self.cari_log_user_btn.setObjectName("cari_log_user_btn")
        self.horizontalLayout_9.addWidget(self.cari_log_user_btn)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.log_user = QtWidgets.QTableWidget(self.tab_5)
        self.log_user.setObjectName("log_user")
        self.log_user.setColumnCount(0)
        self.log_user.setRowCount(0)
        self.verticalLayout_8.addWidget(self.log_user)
        self.horizontalLayout_10.addLayout(self.verticalLayout_8)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.download_log_user_btn = QtWidgets.QPushButton(self.tab_5)
        self.download_log_user_btn.setObjectName("download_log_user_btn")
        self.verticalLayout_10.addWidget(self.download_log_user_btn)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem4)
        self.horizontalLayout_10.addLayout(self.verticalLayout_10)
        TabWidget.addTab(self.tab_5, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "ADMIN ATM BERAS"))
        self.cari_warga.setText(_translate("TabWidget", "CARI"))
        self.tambah_warga_btn.setText(_translate("TabWidget", "TAMBAH"))
        self.edit_warga_btn.setText(_translate("TabWidget", "EDIT"))
        self.hapus_warga_btn.setText(_translate("TabWidget", "HAPUS"))
        self.ganti_pin.setText(_translate("TabWidget", "GANTI PIN"))
        self.ganti_kartu.setText(_translate("TabWidget", "GANTI KARTU"))
        self.hapus_semua_warga_btn.setText(_translate("TabWidget", "HAPUS SEMUA"))
        self.download_warga_btn.setText(_translate("TabWidget", "DOWNLOAD"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "PENERIMA"))
        self.username.setPlaceholderText(_translate("TabWidget", "USERNAME"))
        self.password.setPlaceholderText(_translate("TabWidget", "PASSWORD"))
        self.active.setText(_translate("TabWidget", "AKTIF"))
        self.save_user_btn.setText(_translate("TabWidget", "SIMPAN"))
        self.edit_user_btn.setText(_translate("TabWidget", "EDIT"))
        self.hapus_user_btn.setText(_translate("TabWidget", "HAPUS"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "USER"))
        self.pushButton_3.setText(_translate("TabWidget", "CARI"))
        self.pushButton.setText(_translate("TabWidget", "DOWNLOAD LOG"))
        self.pushButton_2.setText(_translate("TabWidget", "HAPUS LOG"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3), _translate("TabWidget", "LOG TRANSAKSI"))
        self.cari_log_isi_ulang_btn.setText(_translate("TabWidget", "CARI"))
        self.download_log_isi_ulang_btn.setText(_translate("TabWidget", "DOWNLOAD LOG"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_4), _translate("TabWidget", "LOG ISI ULANG"))
        self.cari_log_user_btn.setText(_translate("TabWidget", "CARI"))
        self.download_log_user_btn.setText(_translate("TabWidget", "DOWNLOAD LOG"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_5), _translate("TabWidget", "LOG USER"))

