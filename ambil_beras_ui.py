# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ambil-beras.ui'
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
        Form.resize(751, 605)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 2, 1, 1)
        self.info = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet(_fromUtf8("color: red;"))
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.info.setObjectName(_fromUtf8("info"))
        self.gridLayout.addWidget(self.info, 2, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.kembali_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.kembali_btn.setFont(font)
        self.kembali_btn.setObjectName(_fromUtf8("kembali_btn"))
        self.horizontalLayout.addWidget(self.kembali_btn)
        self.selesai_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.selesai_btn.setFont(font)
        self.selesai_btn.setObjectName(_fromUtf8("selesai_btn"))
        self.horizontalLayout.addWidget(self.selesai_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 8, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 0, 1, 1)
        self.dua_liter = QtGui.QPushButton(Form)
        self.dua_liter.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.dua_liter.setFont(font)
        self.dua_liter.setStyleSheet(_fromUtf8(""))
        self.dua_liter.setObjectName(_fromUtf8("dua_liter"))
        self.gridLayout.addWidget(self.dua_liter, 5, 1, 1, 1)
        self.satu_liter = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.satu_liter.setFont(font)
        self.satu_liter.setObjectName(_fromUtf8("satu_liter"))
        self.gridLayout.addWidget(self.satu_liter, 4, 1, 1, 1)
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 9, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 3, 1, 1, 1)
        self.tiga_liter = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.tiga_liter.setFont(font)
        self.tiga_liter.setObjectName(_fromUtf8("tiga_liter"))
        self.gridLayout.addWidget(self.tiga_liter, 6, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "AMBIL BERAS", None))
        self.info.setText(_translate("Form", "INFO", None))
        self.kembali_btn.setText(_translate("Form", "[BACK] KEMBALI", None))
        self.selesai_btn.setText(_translate("Form", "[ENTER] SELESAI", None))
        self.dua_liter.setText(_translate("Form", "[2] 2 LITER", None))
        self.satu_liter.setText(_translate("Form", "[1] 1 LITER", None))
        self.label.setText(_translate("Form", "SILAKAN PILIH JUMLAH YANG AKAN ANDA AMBIL", None))
        self.tiga_liter.setText(_translate("Form", "[3] 3 LITER", None))

