# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/rescuegrubwidget.ui'
#
# Created: Mon Nov 24 20:29:54 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('yali', fallback=True)
i18n = __trans.ugettext
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

class Ui_RescueGrubWidget(object):
    def setupUi(self, RescueGrubWidget):
        RescueGrubWidget.setObjectName(_fromUtf8("RescueGrubWidget"))
        RescueGrubWidget.resize(445, 537)
        RescueGrubWidget.setWindowTitle(_fromUtf8(""))
        RescueGrubWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(RescueGrubWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 2)
        self.label = QtGui.QLabel(RescueGrubWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.installFirstMBR = QtGui.QRadioButton(RescueGrubWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.installFirstMBR.setFont(font)
        self.installFirstMBR.setObjectName(_fromUtf8("installFirstMBR"))
        self.verticalLayout.addWidget(self.installFirstMBR)
        self.installSelectedPart = QtGui.QRadioButton(RescueGrubWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.installSelectedPart.setFont(font)
        self.installSelectedPart.setObjectName(_fromUtf8("installSelectedPart"))
        self.verticalLayout.addWidget(self.installSelectedPart)
        self.installSelectedDisk = QtGui.QRadioButton(RescueGrubWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.installSelectedDisk.setFont(font)
        self.installSelectedDisk.setObjectName(_fromUtf8("installSelectedDisk"))
        self.verticalLayout.addWidget(self.installSelectedDisk)
        self.gridLayout.addLayout(self.verticalLayout, 3, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 0, 1, 1)
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.deviceList = QtGui.QListWidget(RescueGrubWidget)
        self.deviceList.setStyleSheet(_fromUtf8(""))
        self.deviceList.setIconSize(QtCore.QSize(22, 22))
        self.deviceList.setObjectName(_fromUtf8("deviceList"))
        self.vboxlayout.addWidget(self.deviceList)
        self.gridLayout.addLayout(self.vboxlayout, 5, 1, 1, 2)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 5, 3, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(308, 81, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 6, 1, 1, 2)

        self.retranslateUi(RescueGrubWidget)
        QtCore.QMetaObject.connectSlotsByName(RescueGrubWidget)
        RescueGrubWidget.setTabOrder(self.installFirstMBR, self.installSelectedPart)
        RescueGrubWidget.setTabOrder(self.installSelectedPart, self.installSelectedDisk)

    def retranslateUi(self, RescueGrubWidget):
        self.label.setText(i18n("Select where to install the GRUB bootloader"))
        self.installFirstMBR.setText(i18n("First bootable disk (recommended)"))
        self.installSelectedPart.setText(i18n("Disk partition where Pardus is installed"))
        self.installSelectedDisk.setText(i18n("Selected disk below"))

