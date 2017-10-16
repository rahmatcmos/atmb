# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ubah_pin.ui'
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
        Form.resize(809, 380)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.info = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet(_fromUtf8("color:red"))
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pin = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.pin.setFont(font)
        self.pin.setAlignment(QtCore.Qt.AlignCenter)
        self.pin.setObjectName(_fromUtf8("pin"))
        self.verticalLayout.addWidget(self.pin)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.ulangi_btn = QtGui.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.ulangi_btn.setFont(font)
        self.ulangi_btn.setStyleSheet(_fromUtf8(""))
        self.ulangi_btn.setObjectName(_fromUtf8("ulangi_btn"))
        self.kembali_btn = QtGui.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.kembali_btn.setFont(font)
        self.kembali_btn.setStyleSheet(_fromUtf8(""))
        self.kembali_btn.setObjectName(_fromUtf8("kembali_btn"))
        self.verticalLayout.addWidget(self.splitter)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "UBAH PIN", None))
        self.info.setText(_translate("Form", "MASUKKAN PIN BARU ANDA", None))
        self.pin.setText(_translate("Form", "----", None))
        self.ulangi_btn.setText(_translate("Form", "[*] ULANGI", None))
        self.kembali_btn.setText(_translate("Form", "[#] KEMBALI ", None))

