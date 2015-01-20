# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/connectionlist.ui'
#
# Created: Mon Nov 24 20:29:49 2014
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

class Ui_connectionWidget(object):
    def setupUi(self, connectionWidget):
        connectionWidget.setObjectName(_fromUtf8("connectionWidget"))
        connectionWidget.resize(692, 494)
        connectionWidget.setWindowTitle(_fromUtf8(""))
        self.gridLayout_3 = QtGui.QGridLayout(connectionWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(333, 52, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(160, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.mainFrame = QtGui.QFrame(connectionWidget)
        self.mainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mainFrame.setObjectName(_fromUtf8("mainFrame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.mainFrame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.mainFrame)
        self.label.setStyleSheet(_fromUtf8("color:white;"))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)
        self.buttonCancel = QtGui.QPushButton(self.mainFrame)
        self.buttonCancel.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonCancel.setMaximumSize(QtCore.QSize(24, 24))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.buttonCancel.setFont(font)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.gridLayout.addWidget(self.buttonCancel, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(331, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 1)
        self.connectionList = QtGui.QListWidget(self.mainFrame)
        self.connectionList.setMaximumSize(QtCore.QSize(16777215, 100))
        self.connectionList.setObjectName(_fromUtf8("connectionList"))
        self.gridLayout_2.addWidget(self.connectionList, 2, 0, 1, 1)
        self.buttonConnect = QtGui.QPushButton(self.mainFrame)
        self.buttonConnect.setObjectName(_fromUtf8("buttonConnect"))
        self.gridLayout_2.addWidget(self.buttonConnect, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.mainFrame, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(133, 226, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 2, 2, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 114, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 2, 1, 1, 1)

        self.retranslateUi(connectionWidget)
        QtCore.QMetaObject.connectSlotsByName(connectionWidget)

    def retranslateUi(self, connectionWidget):
        self.label.setText(i18n("To use PiSi History support, you may need to be online. You can use a connection profile from the list below:"))
        self.buttonCancel.setText(i18n("X"))
        self.buttonConnect.setText(i18n("Connect"))

