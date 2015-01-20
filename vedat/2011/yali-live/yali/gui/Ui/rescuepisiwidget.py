# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/rescuepisiwidget.ui'
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

class Ui_RescuePisiWidget(object):
    def setupUi(self, RescuePisiWidget):
        RescuePisiWidget.setObjectName(_fromUtf8("RescuePisiWidget"))
        RescuePisiWidget.resize(666, 563)
        RescuePisiWidget.setWindowTitle(_fromUtf8(""))
        RescuePisiWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(RescuePisiWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 51, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(RescuePisiWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.labelStatus = QtGui.QLabel(RescuePisiWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelStatus.setFont(font)
        self.labelStatus.setText(_fromUtf8("Offline"))
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.horizontalLayout.addWidget(self.labelStatus)
        self.selectConnection = QtGui.QPushButton(RescuePisiWidget)
        self.selectConnection.setObjectName(_fromUtf8("selectConnection"))
        self.horizontalLayout.addWidget(self.selectConnection)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 2)
        self.line = QtGui.QFrame(RescuePisiWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(131, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.infoLabel_2 = QtGui.QLabel(RescuePisiWidget)
        self.infoLabel_2.setStyleSheet(_fromUtf8(""))
        self.infoLabel_2.setWordWrap(False)
        self.infoLabel_2.setObjectName(_fromUtf8("infoLabel_2"))
        self.gridLayout_2.addWidget(self.infoLabel_2, 0, 0, 1, 2)
        self.historyList = QtGui.QListWidget(RescuePisiWidget)
        self.historyList.setObjectName(_fromUtf8("historyList"))
        self.gridLayout_2.addWidget(self.historyList, 1, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(131, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 3, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 2, 1, 1)

        self.retranslateUi(RescuePisiWidget)
        QtCore.QMetaObject.connectSlotsByName(RescuePisiWidget)

    def retranslateUi(self, RescuePisiWidget):
        self.label.setText(i18n("<b>Connection status:</b>"))
        self.selectConnection.setStatusTip(i18n("To use PiSi\'s history feature, you may need to be online. Select connection profile."))
        self.selectConnection.setText(i18n("Select Connection"))
        self.infoLabel_2.setText(i18n("Select the operation to undo:"))

