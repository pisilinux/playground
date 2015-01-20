# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/partresize.ui'
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

class Ui_PartResizeWidget(object):
    def setupUi(self, PartResizeWidget):
        PartResizeWidget.setObjectName(_fromUtf8("PartResizeWidget"))
        PartResizeWidget.resize(758, 547)
        PartResizeWidget.setWindowTitle(_fromUtf8(""))
        PartResizeWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout_2 = QtGui.QGridLayout(PartResizeWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 60, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.mainFrame = QtGui.QFrame(PartResizeWidget)
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
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 39, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.resizeMBSlider = QtGui.QSlider(self.mainFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resizeMBSlider.sizePolicy().hasHeightForWidth())
        self.resizeMBSlider.setSizePolicy(sizePolicy)
        self.resizeMBSlider.setStyleSheet(_fromUtf8(""))
        self.resizeMBSlider.setOrientation(QtCore.Qt.Horizontal)
        self.resizeMBSlider.setObjectName(_fromUtf8("resizeMBSlider"))
        self.gridLayout.addWidget(self.resizeMBSlider, 2, 0, 1, 1)
        self.resizeMB = QtGui.QSpinBox(self.mainFrame)
        self.resizeMB.setSingleStep(10)
        self.resizeMB.setObjectName(_fromUtf8("resizeMB"))
        self.gridLayout.addWidget(self.resizeMB, 2, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.cancelButton = QtGui.QPushButton(self.mainFrame)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.resizeButton = QtGui.QPushButton(self.mainFrame)
        self.resizeButton.setObjectName(_fromUtf8("resizeButton"))
        self.horizontalLayout.addWidget(self.resizeButton)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        self.gridLayout_2.addWidget(self.mainFrame, 1, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 1, 2, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 61, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 2, 1, 1, 1)

        self.retranslateUi(PartResizeWidget)
        QtCore.QObject.connect(self.resizeMBSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.resizeMB.setValue)
        QtCore.QMetaObject.connectSlotsByName(PartResizeWidget)

    def retranslateUi(self, PartResizeWidget):
        self.label.setText(i18n("Changes will be applied when you click \"Resize\". To cancel the changes, click <b>\"Cancel\".\n"
"<br><br>\n"
"Warning: A resizing operation may corrupt the partition, rendering the data on it unreachable. Make sure that you have backed up the data. Note that this operation cannot be undone.<b>"))
        self.resizeMB.setSuffix(i18n(" MB"))
        self.cancelButton.setText(i18n("Cancel"))
        self.resizeButton.setText(i18n("Resize"))

