# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/bg.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1098, 774)
        Form.setStyleSheet(_fromUtf8("#Form{\n"
"      background-image: url(:/gui/pics/bg.png);\n"
"      background-color: rgb(50, 50, 50);\n"
"      /*background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:0.572, y2:0.688, stop:0 rgba(75, 114, 137, 255), stop:1 rgba(29, 42, 51, 255));*/\n"
"      padding: 0px;\n"
"      margin: 0px;\n"
"}"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

