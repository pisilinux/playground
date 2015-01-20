# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/diskItem.ui'
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

class Ui_DiskItem(object):
    def setupUi(self, DiskItem):
        DiskItem.setObjectName(_fromUtf8("DiskItem"))
        DiskItem.resize(142, 184)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DiskItem.sizePolicy().hasHeightForWidth())
        DiskItem.setSizePolicy(sizePolicy)
        DiskItem.setMinimumSize(QtCore.QSize(0, 0))
        DiskItem.setMaximumSize(QtCore.QSize(16777215, 16777215))
        DiskItem.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(DiskItem)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 10, 0, 5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.icon = QtGui.QLabel(DiskItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QtCore.QSize(100, 100))
        self.icon.setMaximumSize(QtCore.QSize(100, 100))
        self.icon.setText(_fromUtf8(""))
        self.icon.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/drive-removable-media-usb-big.png")))
        self.icon.setScaledContents(True)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setMargin(0)
        self.icon.setIndent(0)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.horizontalLayout.addWidget(self.icon)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelDrive = QtGui.QLabel(DiskItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDrive.sizePolicy().hasHeightForWidth())
        self.labelDrive.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelDrive.setFont(font)
        self.labelDrive.setStyleSheet(_fromUtf8("padding-top: 10px"))
        self.labelDrive.setText(_fromUtf8(""))
        self.labelDrive.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelDrive.setWordWrap(True)
        self.labelDrive.setIndent(0)
        self.labelDrive.setObjectName(_fromUtf8("labelDrive"))
        self.verticalLayout.addWidget(self.labelDrive)
        self.labelInfo = QtGui.QLabel(DiskItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.labelInfo.setFont(font)
        self.labelInfo.setText(_fromUtf8(""))
        self.labelInfo.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelInfo.setWordWrap(True)
        self.labelInfo.setMargin(5)
        self.labelInfo.setIndent(0)
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        self.verticalLayout.addWidget(self.labelInfo)

        self.retranslateUi(DiskItem)
        QtCore.QMetaObject.connectSlotsByName(DiskItem)

    def retranslateUi(self, DiskItem):
        pass

