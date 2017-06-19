# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'saldo.ui'
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
        Form.resize(695, 500)
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
        self.info.setFont(font)
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.saldo = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.saldo.setFont(font)
        self.saldo.setStyleSheet(_fromUtf8("color: red"))
        self.saldo.setAlignment(QtCore.Qt.AlignCenter)
        self.saldo.setObjectName(_fromUtf8("saldo"))
        self.verticalLayout.addWidget(self.saldo)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        # self.ambil_beras_btn = QtGui.QPushButton(Form)
        # font = QtGui.QFont()
        # font.setPointSize(30)
        # self.ambil_beras_btn.setFont(font)
        # self.ambil_beras_btn.setStyleSheet(_fromUtf8("text-align:left;"))
        # self.ambil_beras_btn.setObjectName(_fromUtf8("ambil_beras_btn"))
        # self.verticalLayout.addWidget(self.ambil_beras_btn)
        # self.kembali_btn = QtGui.QPushButton(Form)
        # font = QtGui.QFont()
        # font.setPointSize(30)
        # self.kembali_btn.setFont(font)
        # self.kembali_btn.setStyleSheet(_fromUtf8("text-align:left;"))
        # self.kembali_btn.setObjectName(_fromUtf8("kembali_btn"))
        # self.verticalLayout.addWidget(self.kembali_btn)
        # self.selesai_btn = QtGui.QPushButton(Form)
        # font = QtGui.QFont()
        # font.setPointSize(30)
        # self.selesai_btn.setFont(font)
        # self.selesai_btn.setStyleSheet(_fromUtf8("text-align:left;"))
        # self.selesai_btn.setObjectName(_fromUtf8("selesai_btn"))
        # self.verticalLayout.addWidget(self.selesai_btn)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "CEK SALDO BERAS", None))
        self.info.setText(_translate("Form", "SISA SALDO BERAS ANDA ADALAH", None))
        self.saldo.setText(_translate("Form", "saldo", None))
        # self.ambil_beras_btn.setText(_translate("Form", "  [1] AMBIL BERAS", None))
        # self.kembali_btn.setText(_translate("Form", "  [2] KEMBALI", None))
        # self.selesai_btn.setText(_translate("Form", "  [3] SELESAI", None))

