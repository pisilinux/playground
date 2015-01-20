# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/exception.ui'
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

class Ui_Exception(object):
    def setupUi(self, Exception):
        Exception.setObjectName(_fromUtf8("Exception"))
        Exception.resize(435, 293)
        self.gridLayout = QtGui.QGridLayout(Exception)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.info = QtGui.QLabel(Exception)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet(_fromUtf8(""))
        self.info.setObjectName(_fromUtf8("info"))
        self.gridLayout.addWidget(self.info, 0, 0, 1, 4)
        self.label = QtGui.QLabel(Exception)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 4)
        self.traceback = QtGui.QTextBrowser(Exception)
        self.traceback.setObjectName(_fromUtf8("traceback"))
        self.gridLayout.addWidget(self.traceback, 3, 0, 1, 4)
        spacerItem = QtGui.QSpacerItem(226, 28, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        self.rebootButton = QtGui.QPushButton(Exception)
        self.rebootButton.setObjectName(_fromUtf8("rebootButton"))
        self.gridLayout.addWidget(self.rebootButton, 5, 3, 1, 1)
        self.line = QtGui.QFrame(Exception)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 1, 1, 3)
        self.showBackTrace = QtGui.QPushButton(Exception)
        self.showBackTrace.setObjectName(_fromUtf8("showBackTrace"))
        self.gridLayout.addWidget(self.showBackTrace, 5, 2, 1, 1)

        self.retranslateUi(Exception)
        QtCore.QMetaObject.connectSlotsByName(Exception)

    def retranslateUi(self, Exception):
        self.info.setText(i18n("Unhandled exception occured"))
        self.label.setText(i18n("Please fill a bug report at http://bugs.pardus.org.tr/ attaching the following backtrace."))
        self.rebootButton.setText(i18n("Reboot"))
        self.showBackTrace.setText(i18n("Show Backtrace"))

