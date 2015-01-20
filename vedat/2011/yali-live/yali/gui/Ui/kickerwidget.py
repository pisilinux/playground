# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/kickerwidget.ui'
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

class Ui_KickerWidget(object):
    def setupUi(self, KickerWidget):
        KickerWidget.setObjectName(_fromUtf8("KickerWidget"))
        KickerWidget.resize(502, 360)
        KickerWidget.setWindowTitle(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(KickerWidget)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))

        self.retranslateUi(KickerWidget)
        QtCore.QMetaObject.connectSlotsByName(KickerWidget)

    def retranslateUi(self, KickerWidget):
        pass

