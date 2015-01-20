# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/partitionshrink.ui'
#
# Created: Mon Nov 24 20:29:53 2014
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

class Ui_ShrinkPartitionWidget(object):
    def setupUi(self, ShrinkPartitionWidget):
        ShrinkPartitionWidget.setObjectName(_fromUtf8("ShrinkPartitionWidget"))
        ShrinkPartitionWidget.resize(602, 269)
        self.gridLayout = QtGui.QGridLayout(ShrinkPartitionWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(465, 64, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(56, 118, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 5, 1)
        self.label = QtGui.QLabel(ShrinkPartitionWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(56, 118, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 5, 1)
        self.partitions = QtGui.QComboBox(ShrinkPartitionWidget)
        self.partitions.setMinimumSize(QtCore.QSize(0, 30))
        self.partitions.setObjectName(_fromUtf8("partitions"))
        self.gridLayout.addWidget(self.partitions, 2, 1, 1, 2)
        self.label_2 = QtGui.QLabel(ShrinkPartitionWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 2)
        self.sizeSlider = QtGui.QSlider(ShrinkPartitionWidget)
        self.sizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sizeSlider.setObjectName(_fromUtf8("sizeSlider"))
        self.gridLayout.addWidget(self.sizeSlider, 4, 1, 1, 1)
        self.sizeSpin = QtGui.QSpinBox(ShrinkPartitionWidget)
        self.sizeSpin.setMinimumSize(QtCore.QSize(0, 30))
        self.sizeSpin.setProperty("value", 20)
        self.sizeSpin.setObjectName(_fromUtf8("sizeSpin"))
        self.gridLayout.addWidget(self.sizeSpin, 4, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ShrinkPartitionWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 2)

        self.retranslateUi(ShrinkPartitionWidget)
        QtCore.QObject.connect(self.sizeSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sizeSpin.setValue)
        QtCore.QObject.connect(self.sizeSpin, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sizeSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(ShrinkPartitionWidget)

    def retranslateUi(self, ShrinkPartitionWidget):
        self.label.setText(i18n("Which partition would you like to shrink to make room for your installation?"))
        self.label_2.setText(i18n("Shrink partition to size (in MB)"))

