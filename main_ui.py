# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
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

class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName(_fromUtf8("main"))
        main.resize(998, 796)
        self.horizontalLayout = QtGui.QHBoxLayout(main)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(50)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.logo = QtGui.QLabel(main)
        self.logo.setText(_fromUtf8(""))
        self.logo.setPixmap(QtGui.QPixmap(_fromUtf8("/home/pi/ATMB/img/logo.png")))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName(_fromUtf8("logo"))
        self.verticalLayout_2.addWidget(self.logo)
        self.label = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tanggal = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.tanggal.setFont(font)
        self.tanggal.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255)"))
        self.tanggal.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.tanggal.setObjectName(_fromUtf8("tanggal"))
        self.verticalLayout.addWidget(self.tanggal)
        self.jam = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.jam.setFont(font)
        self.jam.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255)"))
        self.jam.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.jam.setObjectName(_fromUtf8("jam"))
        self.verticalLayout.addWidget(self.jam)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.info = QtGui.QLabel(main)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0)"))
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        main.setWindowTitle(_translate("main", "ATM BERAS", None))
        self.label_2.setText(_translate("main", "SAMPURASUN", None))
        self.label_3.setText(_translate("main", "Wilujeung Sumping", None))
        self.label_4.setText(_translate("main", "di Bank Perelek", None))
        self.label.setText(_translate("main", "KABUPATEN PURWAKARTA", None))
        self.tanggal.setText(_translate("main", "tanggal", None))
        self.jam.setText(_translate("main", "jam", None))
        self.info.setText(_translate("main", "INFO", None))
