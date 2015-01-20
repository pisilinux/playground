# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/help.ui'
#
# Created: Mon Nov 24 20:29:50 2014
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

class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName(_fromUtf8("Help"))
        Help.resize(600, 57)
        Help.setMinimumSize(QtCore.QSize(600, 0))
        Help.setMaximumSize(QtCore.QSize(600, 400))
        Help.setStyleSheet(_fromUtf8(""))
        self.gridLayout_2 = QtGui.QGridLayout(Help)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.helpContentFrame = QtGui.QWidget(Help)
        self.helpContentFrame.setObjectName(_fromUtf8("helpContentFrame"))
        self.gridLayout = QtGui.QGridLayout(self.helpContentFrame)
        self.gridLayout.setMargin(20)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.helpContent = QtGui.QLabel(self.helpContentFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpContent.sizePolicy().hasHeightForWidth())
        self.helpContent.setSizePolicy(sizePolicy)
        self.helpContent.setMinimumSize(QtCore.QSize(0, 0))
        self.helpContent.setScaledContents(False)
        self.helpContent.setWordWrap(True)
        self.helpContent.setMargin(0)
        self.helpContent.setIndent(0)
        self.helpContent.setObjectName(_fromUtf8("helpContent"))
        self.gridLayout.addWidget(self.helpContent, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.helpContentFrame, 0, 0, 1, 1)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        self.helpContent.setText(i18n("help content"))

