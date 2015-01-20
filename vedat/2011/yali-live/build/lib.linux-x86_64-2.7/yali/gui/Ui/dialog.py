# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/dialog.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(745, 572)
        Form.setWindowTitle(_fromUtf8(""))
        Form.setStyleSheet(_fromUtf8("QFrame#windowTitle {background-color:white;border:1px solid #CCC;border-radius:4px;}"))
        self.gridlayout = QtGui.QGridLayout(Form)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.windowTitle = QtGui.QFrame(Form)
        self.windowTitle.setMaximumSize(QtCore.QSize(9999999, 26))
        self.windowTitle.setObjectName(_fromUtf8("windowTitle"))
        self.hboxlayout = QtGui.QHBoxLayout(self.windowTitle)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0, 0, 4, 0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(self.windowTitle)
        self.label.setStyleSheet(_fromUtf8("padding-left:4px; font:bold 11px"))
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.windowTitle)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setStyleSheet(_fromUtf8("font:bold;"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.hboxlayout.addWidget(self.pushButton)
        self.gridlayout.addWidget(self.windowTitle, 0, 0, 1, 1)
        self.content = QtGui.QWidget(Form)
        self.content.setObjectName(_fromUtf8("content"))
        self.gridlayout.addWidget(self.content, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.pushButton.setText(i18n("X"))

