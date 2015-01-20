# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/rootpasswidget.ui'
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

class Ui_RootPassWidget(object):
    def setupUi(self, RootPassWidget):
        RootPassWidget.setObjectName(_fromUtf8("RootPassWidget"))
        RootPassWidget.resize(986, 858)
        RootPassWidget.setWindowTitle(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(RootPassWidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.frame = QtGui.QFrame(RootPassWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 250))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 250))
        self.frame.setStyleSheet(_fromUtf8("#frame{background-color: rgba(0,0,0,100)}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setContentsMargins(0, 20, 0, 20)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pix = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pix.sizePolicy().hasHeightForWidth())
        self.pix.setSizePolicy(sizePolicy)
        self.pix.setText(_fromUtf8(""))
        self.pix.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/meeting-participant-big.png")))
        self.pix.setAlignment(QtCore.Qt.AlignCenter)
        self.pix.setWordWrap(False)
        self.pix.setObjectName(_fromUtf8("pix"))
        self.horizontalLayout_2.addWidget(self.pix)
        self.groupBox = QtGui.QFrame(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.groupBox.setFrameShadow(QtGui.QFrame.Raised)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.textLabel3 = QtGui.QLabel(self.groupBox)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setIndent(0)
        self.textLabel3.setObjectName(_fromUtf8("textLabel3"))
        self.verticalLayout_2.addWidget(self.textLabel3)
        self.pass1 = QtGui.QLineEdit(self.groupBox)
        self.pass1.setMinimumSize(QtCore.QSize(200, 30))
        self.pass1.setMaximumSize(QtCore.QSize(200, 30))
        self.pass1.setStyleSheet(_fromUtf8(""))
        self.pass1.setInputMask(_fromUtf8(""))
        self.pass1.setEchoMode(QtGui.QLineEdit.Password)
        self.pass1.setObjectName(_fromUtf8("pass1"))
        self.verticalLayout_2.addWidget(self.pass1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.textLabel3_2 = QtGui.QLabel(self.groupBox)
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setIndent(0)
        self.textLabel3_2.setObjectName(_fromUtf8("textLabel3_2"))
        self.verticalLayout_2.addWidget(self.textLabel3_2)
        self.pass2 = QtGui.QLineEdit(self.groupBox)
        self.pass2.setMinimumSize(QtCore.QSize(200, 30))
        self.pass2.setMaximumSize(QtCore.QSize(200, 30))
        self.pass2.setStyleSheet(_fromUtf8(""))
        self.pass2.setInputMask(_fromUtf8(""))
        self.pass2.setEchoMode(QtGui.QLineEdit.Password)
        self.pass2.setObjectName(_fromUtf8("pass2"))
        self.verticalLayout_2.addWidget(self.pass2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.textLabel1_2 = QtGui.QLabel(self.groupBox)
        self.textLabel1_2.setWordWrap(False)
        self.textLabel1_2.setObjectName(_fromUtf8("textLabel1_2"))
        self.verticalLayout_2.addWidget(self.textLabel1_2)
        self.hostname = QtGui.QLineEdit(self.groupBox)
        self.hostname.setMinimumSize(QtCore.QSize(200, 30))
        self.hostname.setMaximumSize(QtCore.QSize(200, 30))
        self.hostname.setStyleSheet(_fromUtf8(""))
        self.hostname.setText(_fromUtf8(""))
        self.hostname.setObjectName(_fromUtf8("hostname"))
        self.verticalLayout_2.addWidget(self.hostname)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_2.addWidget(self.groupBox)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.gridlayout.addWidget(self.frame, 1, 0, 1, 3)
        spacerItem6 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem6, 4, 1, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem7, 0, 1, 1, 1)

        self.retranslateUi(RootPassWidget)
        QtCore.QMetaObject.connectSlotsByName(RootPassWidget)

    def retranslateUi(self, RootPassWidget):
        self.textLabel3.setText(i18n("Administrator password"))
        self.textLabel3_2.setText(i18n("Confirm password"))
        self.textLabel1_2.setText(i18n("Computer Name"))

