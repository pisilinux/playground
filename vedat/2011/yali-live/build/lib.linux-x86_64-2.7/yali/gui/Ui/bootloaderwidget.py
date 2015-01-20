# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/bootloaderwidget.ui'
#
# Created: Mon Nov 24 20:29:48 2014
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

class Ui_BootLoaderWidget(object):
    def setupUi(self, BootLoaderWidget):
        BootLoaderWidget.setObjectName(_fromUtf8("BootLoaderWidget"))
        BootLoaderWidget.resize(923, 564)
        self.verticalLayout_2 = QtGui.QVBoxLayout(BootLoaderWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(BootLoaderWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
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
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pix = QtGui.QLabel(self.frame)
        self.pix.setMaximumSize(QtCore.QSize(180, 128))
        self.pix.setText(_fromUtf8(""))
        self.pix.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/bootloader-big.png")))
        self.pix.setScaledContents(True)
        self.pix.setWordWrap(False)
        self.pix.setObjectName(_fromUtf8("pix"))
        self.horizontalLayout_2.addWidget(self.pix)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonGroup = QtGui.QGroupBox(self.frame)
        self.buttonGroup.setMinimumSize(QtCore.QSize(350, 0))
        self.buttonGroup.setMaximumSize(QtCore.QSize(350, 16777215))
        self.buttonGroup.setStyleSheet(_fromUtf8("#buttonGroup{border: 0px}"))
        self.buttonGroup.setTitle(_fromUtf8(""))
        self.buttonGroup.setFlat(True)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.gridLayout = QtGui.QGridLayout(self.buttonGroup)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.advancedSettings = QtGui.QRadioButton(self.buttonGroup)
        self.advancedSettings.setObjectName(_fromUtf8("advancedSettings"))
        self.gridLayout.addWidget(self.advancedSettings, 1, 0, 1, 1)
        self.defaultSettings = QtGui.QRadioButton(self.buttonGroup)
        self.defaultSettings.setObjectName(_fromUtf8("defaultSettings"))
        self.gridLayout.addWidget(self.defaultSettings, 0, 0, 1, 1)
        self.advancedSettingsBox = QtGui.QGroupBox(self.buttonGroup)
        self.advancedSettingsBox.setStyleSheet(_fromUtf8("#advancedSettingsBox{border: 0px}"))
        self.advancedSettingsBox.setTitle(_fromUtf8(""))
        self.advancedSettingsBox.setFlat(True)
        self.advancedSettingsBox.setObjectName(_fromUtf8("advancedSettingsBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.advancedSettingsBox)
        self.gridLayout_2.setContentsMargins(15, 0, 4, -1)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.noInstall = QtGui.QRadioButton(self.advancedSettingsBox)
        self.noInstall.setObjectName(_fromUtf8("noInstall"))
        self.gridLayout_2.addWidget(self.noInstall, 3, 0, 1, 2)
        self.installPartition = QtGui.QRadioButton(self.advancedSettingsBox)
        self.installPartition.setObjectName(_fromUtf8("installPartition"))
        self.gridLayout_2.addWidget(self.installPartition, 2, 0, 1, 2)
        self.installMBR = QtGui.QRadioButton(self.advancedSettingsBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installMBR.sizePolicy().hasHeightForWidth())
        self.installMBR.setSizePolicy(sizePolicy)
        self.installMBR.setObjectName(_fromUtf8("installMBR"))
        self.gridLayout_2.addWidget(self.installMBR, 0, 0, 1, 1)
        self.drives = QtGui.QComboBox(self.advancedSettingsBox)
        self.drives.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drives.sizePolicy().hasHeightForWidth())
        self.drives.setSizePolicy(sizePolicy)
        self.drives.setMinimumSize(QtCore.QSize(100, 0))
        self.drives.setMaximumSize(QtCore.QSize(100, 16777215))
        self.drives.setObjectName(_fromUtf8("drives"))
        self.gridLayout_2.addWidget(self.drives, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.advancedSettingsBox, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.buttonGroup)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(BootLoaderWidget)
        QtCore.QObject.connect(self.installMBR, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.drives.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(BootLoaderWidget)

    def retranslateUi(self, BootLoaderWidget):
        self.advancedSettings.setText(i18n("Advanced settings"))
        self.defaultSettings.setText(i18n("Default settings"))
        self.noInstall.setText(i18n("Don\'t install bootloader"))
        self.installPartition.setText(i18n("The partition where Pardus is installed"))
        self.installMBR.setText(i18n("The first sector of"))

