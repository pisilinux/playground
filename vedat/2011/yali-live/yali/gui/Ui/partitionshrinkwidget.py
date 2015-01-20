# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/partitionshrinkwidget.ui'
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

class Ui_PartShrinkWidget(object):
    def setupUi(self, PartShrinkWidget):
        PartShrinkWidget.setObjectName(_fromUtf8("PartShrinkWidget"))
        PartShrinkWidget.resize(758, 547)
        PartShrinkWidget.setWindowTitle(_fromUtf8(""))
        PartShrinkWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout_2 = QtGui.QGridLayout(PartShrinkWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 60, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.mainFrame = QtGui.QFrame(PartShrinkWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy)
        self.mainFrame.setMinimumSize(QtCore.QSize(400, 0))
        self.mainFrame.setStyleSheet(_fromUtf8(""))
        self.mainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainFrame.setLineWidth(0)
        self.mainFrame.setObjectName(_fromUtf8("mainFrame"))
        self.gridLayout = QtGui.QGridLayout(self.mainFrame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.mainFrame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.partitions = QtGui.QListWidget(self.mainFrame)
        self.partitions.setObjectName(_fromUtf8("partitions"))
        self.gridLayout.addWidget(self.partitions, 1, 0, 1, 3)
        self.label_2 = QtGui.QLabel(self.mainFrame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.shrinkMBSlider = QtGui.QSlider(self.mainFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shrinkMBSlider.sizePolicy().hasHeightForWidth())
        self.shrinkMBSlider.setSizePolicy(sizePolicy)
        self.shrinkMBSlider.setStyleSheet(_fromUtf8(""))
        self.shrinkMBSlider.setOrientation(QtCore.Qt.Horizontal)
        self.shrinkMBSlider.setObjectName(_fromUtf8("shrinkMBSlider"))
        self.gridLayout.addWidget(self.shrinkMBSlider, 2, 1, 1, 1)
        self.shrinkMB = QtGui.QSpinBox(self.mainFrame)
        self.shrinkMB.setMinimumSize(QtCore.QSize(0, 30))
        self.shrinkMB.setSingleStep(10)
        self.shrinkMB.setObjectName(_fromUtf8("shrinkMB"))
        self.gridLayout.addWidget(self.shrinkMB, 2, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cancelButton = QtGui.QPushButton(self.mainFrame)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.shrinkButton = QtGui.QPushButton(self.mainFrame)
        self.shrinkButton.setObjectName(_fromUtf8("shrinkButton"))
        self.horizontalLayout.addWidget(self.shrinkButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 3)
        self.gridLayout_2.addWidget(self.mainFrame, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 61, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 2, 1, 1, 1)

        self.retranslateUi(PartShrinkWidget)
        QtCore.QObject.connect(self.shrinkMBSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.shrinkMB.setValue)
        QtCore.QMetaObject.connectSlotsByName(PartShrinkWidget)

    def retranslateUi(self, PartShrinkWidget):
        self.label.setText(i18n("Which partition would you like to shrink to make room for your installation?"))
        self.label_2.setText(i18n("Shrink partition to size (in MB) :"))
        self.shrinkMB.setSuffix(i18n(" MB"))
        self.cancelButton.setText(i18n("Cancel"))
        self.shrinkButton.setText(i18n("Shrink"))

