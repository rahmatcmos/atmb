# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form-daftar-1.ui'
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
        Form.resize(707, 437)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        self.tgl_lahir = QtGui.QDateEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tgl_lahir.setFont(font)
        self.tgl_lahir.setObjectName(_fromUtf8("tgl_lahir"))
        self.gridLayout.addWidget(self.tgl_lahir, 3, 1, 1, 2)
        self.simpan_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.simpan_btn.setFont(font)
        self.simpan_btn.setObjectName(_fromUtf8("simpan_btn"))
        self.gridLayout.addWidget(self.simpan_btn, 5, 1, 1, 1)
        self.laki_laki = QtGui.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.laki_laki.setFont(font)
        self.laki_laki.setChecked(True)
        self.laki_laki.setObjectName(_fromUtf8("laki_laki"))
        self.gridLayout.addWidget(self.laki_laki, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        self.perempuan = QtGui.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.perempuan.setFont(font)
        self.perempuan.setObjectName(_fromUtf8("perempuan"))
        self.gridLayout.addWidget(self.perempuan, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_4 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.reset_btn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.reset_btn.setFont(font)
        self.reset_btn.setObjectName(_fromUtf8("reset_btn"))
        self.gridLayout.addWidget(self.reset_btn, 5, 2, 1, 1)
        self.nama = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nama.setFont(font)
        self.nama.setObjectName(_fromUtf8("nama"))
        self.gridLayout.addWidget(self.nama, 1, 1, 1, 2)
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.alamat = QtGui.QLineEdit(Form)
        self.alamat.setObjectName(_fromUtf8("alamat"))
        self.gridLayout.addWidget(self.alamat, 4, 1, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.info = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet(_fromUtf8("color:red;"))
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)
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
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "FORM PENDAFTARAN", None))
        self.tgl_lahir.setDisplayFormat(_translate("Form", "yyyy-MM-dd", None))
        self.simpan_btn.setText(_translate("Form", "SIMPAN", None))
        self.laki_laki.setText(_translate("Form", "Laki - Laki", None))
        self.label_2.setText(_translate("Form", "JENIS KELAMIN", None))
        self.perempuan.setText(_translate("Form", "Perempuan", None))
        self.label_3.setText(_translate("Form", "TANGGAL LAHIR", None))
        self.label_4.setText(_translate("Form", "ALAMAT", None))
        self.reset_btn.setText(_translate("Form", "RESET", None))
        self.label.setText(_translate("Form", "NAMA", None))
        self.info.setText(_translate("Form", "TEMPELKAN KARTU", None))
        self.pin.setText(_translate("Form", "------", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

