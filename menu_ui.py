# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(509, 445)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ambil_beras_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.ambil_beras_btn.setFont(font)
        self.ambil_beras_btn.setStyleSheet(_fromUtf8("text-align: left;"))
        self.ambil_beras_btn.setObjectName(_fromUtf8("ambil_beras_btn"))
        self.gridLayout.addWidget(self.ambil_beras_btn, 4, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 1, 1, 1)
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 5, 2, 1, 1)
        self.selesai_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.selesai_btn.setFont(font)
        self.selesai_btn.setStyleSheet(_fromUtf8("text-align:left"))
        self.selesai_btn.setObjectName(_fromUtf8("selesai_btn"))
        self.gridLayout.addWidget(self.selesai_btn, 7, 1, 1, 1)
        self.ubah_pin_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.ubah_pin_btn.setFont(font)
        self.ubah_pin_btn.setStyleSheet(_fromUtf8("text-align: left"))
        self.ubah_pin_btn.setObjectName(_fromUtf8("ubah_pin_btn"))
        self.gridLayout.addWidget(self.ubah_pin_btn, 6, 1, 1, 1)
        self.cek_saldo_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.cek_saldo_btn.setFont(font)
        self.cek_saldo_btn.setStyleSheet(_fromUtf8("text-align: left"))
        self.cek_saldo_btn.setObjectName(_fromUtf8("cek_saldo_btn"))
        self.gridLayout.addWidget(self.cek_saldo_btn, 5, 1, 1, 1)
        self.info = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet(_fromUtf8("color: red;"))
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setObjectName(_fromUtf8("info"))
        self.gridLayout.addWidget(self.info, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "MENU", None))
        self.ambil_beras_btn.setText(_translate("Form", "  [1] AMBIL BERAS", None))
        self.label.setText(_translate("Form", "SILAKAN PILIH MENU DI BAWAH INI", None))
        self.selesai_btn.setText(_translate("Form", "  [4] SELESAI", None))
        self.ubah_pin_btn.setText(_translate("Form", "  [3] UBAH PIN", None))
        self.cek_saldo_btn.setText(_translate("Form", "  [2] CEK SALDO BERAS", None))
        self.info.setText(_translate("Form", "info", None))

