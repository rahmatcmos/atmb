# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proses_ambil_beras.ui'
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
        Form.resize(770, 410)
        Form.setStyleSheet(_fromUtf8("c"))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
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
        self.verticalLayout.addWidget(self.info)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "PROSES AMBIL BERAS", None))
        self.info.setText(_translate("Form", "SEDANG MEMPROSES. SILAKAN TUNGGU...", None))

