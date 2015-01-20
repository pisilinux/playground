# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/autopartquestion.ui'
#
# Created: Mon Nov 24 20:29:47 2014
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

class Ui_autoPartQuestion(object):
    def setupUi(self, autoPartQuestion):
        autoPartQuestion.setObjectName(_fromUtf8("autoPartQuestion"))
        autoPartQuestion.resize(692, 494)
        self.gridLayout_3 = QtGui.QGridLayout(autoPartQuestion)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(333, 52, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(160, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.mainFrame = QtGui.QFrame(autoPartQuestion)
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
        self.cancelButton = QtGui.QPushButton(self.mainFrame)
        self.cancelButton.setMinimumSize(QtCore.QSize(24, 24))
        self.cancelButton.setMaximumSize(QtCore.QSize(24, 24))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(331, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 1)
        self.bestChoice = QtGui.QRadioButton(self.mainFrame)
        self.bestChoice.setStyleSheet(_fromUtf8("color:white;"))
        self.bestChoice.setObjectName(_fromUtf8("bestChoice"))
        self.gridLayout_2.addWidget(self.bestChoice, 2, 0, 1, 1)
        self.userChoice = QtGui.QRadioButton(self.mainFrame)
        self.userChoice.setStyleSheet(_fromUtf8("color:white;"))
        self.userChoice.setObjectName(_fromUtf8("userChoice"))
        self.gridLayout_2.addWidget(self.userChoice, 3, 0, 1, 1)
        self.partition_list = QtGui.QListWidget(self.mainFrame)
        self.partition_list.setMaximumSize(QtCore.QSize(16777215, 100))
        self.partition_list.setObjectName(_fromUtf8("partition_list"))
        self.gridLayout_2.addWidget(self.partition_list, 4, 0, 1, 1)
        self.useSelectedButton = QtGui.QPushButton(self.mainFrame)
        self.useSelectedButton.setObjectName(_fromUtf8("useSelectedButton"))
        self.gridLayout_2.addWidget(self.useSelectedButton, 5, 0, 1, 1)
        self.gridLayout_3.addWidget(self.mainFrame, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(133, 226, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 2, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 114, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 2, 1, 1, 1)

        self.retranslateUi(autoPartQuestion)
        QtCore.QMetaObject.connectSlotsByName(autoPartQuestion)

    def retranslateUi(self, autoPartQuestion):
        self.label.setText(i18n("There appears to be more than one resizeable partition. You can select a partition from the list below or YALI will select one for you."))
        self.cancelButton.setText(i18n("X"))
        self.bestChoice.setText(i18n("Automatically choose the partition to resize (recommended)"))
        self.userChoice.setText(i18n("I will choose the target"))
        self.useSelectedButton.setText(i18n("Use Selected"))

