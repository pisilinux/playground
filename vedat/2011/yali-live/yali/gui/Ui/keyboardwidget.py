# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/keyboardwidget.ui'
#
# Created: Mon Nov 24 20:29:51 2014
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

class Ui_KeyboardWidget(object):
    def setupUi(self, KeyboardWidget):
        KeyboardWidget.setObjectName(_fromUtf8("KeyboardWidget"))
        KeyboardWidget.resize(1000, 540)
        KeyboardWidget.setWindowTitle(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(KeyboardWidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.frame = QtGui.QFrame(KeyboardWidget)
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
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(-1, 20, -1, 20)
        self.gridLayout_3.setHorizontalSpacing(30)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 0, 1, 1)
        self.pix = QtGui.QLabel(self.frame)
        self.pix.setText(_fromUtf8(""))
        self.pix.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/input-keyboard-big.png")))
        self.pix.setAlignment(QtCore.Qt.AlignCenter)
        self.pix.setWordWrap(False)
        self.pix.setObjectName(_fromUtf8("pix"))
        self.gridLayout_3.addWidget(self.pix, 0, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(10, -1, 10, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.keyboard_list = QtGui.QComboBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyboard_list.sizePolicy().hasHeightForWidth())
        self.keyboard_list.setSizePolicy(sizePolicy)
        self.keyboard_list.setMinimumSize(QtCore.QSize(250, 30))
        self.keyboard_list.setMaximumSize(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.keyboard_list.setFont(font)
        self.keyboard_list.setFrame(True)
        self.keyboard_list.setObjectName(_fromUtf8("keyboard_list"))
        self.verticalLayout_2.addWidget(self.keyboard_list)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.textLabel1_2 = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel1_2.sizePolicy().hasHeightForWidth())
        self.textLabel1_2.setSizePolicy(sizePolicy)
        self.textLabel1_2.setMinimumSize(QtCore.QSize(250, 0))
        self.textLabel1_2.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textLabel1_2.setFont(font)
        self.textLabel1_2.setWordWrap(False)
        self.textLabel1_2.setObjectName(_fromUtf8("textLabel1_2"))
        self.verticalLayout_3.addWidget(self.textLabel1_2)
        self.lineEdit1 = QtGui.QLineEdit(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit1.sizePolicy().hasHeightForWidth())
        self.lineEdit1.setSizePolicy(sizePolicy)
        self.lineEdit1.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit1.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.lineEdit1.setFont(font)
        self.lineEdit1.setStyleSheet(_fromUtf8(""))
        self.lineEdit1.setObjectName(_fromUtf8("lineEdit1"))
        self.verticalLayout_3.addWidget(self.lineEdit1)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.gridlayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(KeyboardWidget)
        QtCore.QMetaObject.connectSlotsByName(KeyboardWidget)

    def retranslateUi(self, KeyboardWidget):
        self.label.setText(i18n("Keyboard Layouts"))
        self.textLabel1_2.setText(i18n("Test Layout"))

