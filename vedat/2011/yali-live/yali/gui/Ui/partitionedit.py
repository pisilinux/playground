# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/partitionedit.ui'
#
# Created: Mon Nov 24 20:29:52 2014
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

class Ui_partitioneditwdiget(object):
    def setupUi(self, partitioneditwdiget):
        partitioneditwdiget.setObjectName(_fromUtf8("partitioneditwdiget"))
        partitioneditwdiget.resize(606, 335)
        partitioneditwdiget.setWindowTitle(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(partitioneditwdiget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.deviceGroup = QtGui.QGroupBox(partitioneditwdiget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceGroup.sizePolicy().hasHeightForWidth())
        self.deviceGroup.setSizePolicy(sizePolicy)
        self.deviceGroup.setMinimumSize(QtCore.QSize(580, 0))
        self.deviceGroup.setMaximumSize(QtCore.QSize(16777215, 145))
        self.deviceGroup.setAutoFillBackground(False)
        self.deviceGroup.setStyleSheet(_fromUtf8(""))
        self.deviceGroup.setTitle(_fromUtf8(""))
        self.deviceGroup.setObjectName(_fromUtf8("deviceGroup"))
        self.gridLayout = QtGui.QGridLayout(self.deviceGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.deviceGroup)
        font = QtGui.QFont()
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.mountpoint = QtGui.QComboBox(self.deviceGroup)
        self.mountpoint.setMinimumSize(QtCore.QSize(0, 30))
        self.mountpoint.setObjectName(_fromUtf8("mountpoint"))
        self.gridLayout.addWidget(self.mountpoint, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(233, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.deviceGroup)
        font = QtGui.QFont()
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.partitionSizeCombo = QtGui.QSpinBox(self.deviceGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partitionSizeCombo.sizePolicy().hasHeightForWidth())
        self.partitionSizeCombo.setSizePolicy(sizePolicy)
        self.partitionSizeCombo.setMinimumSize(QtCore.QSize(120, 30))
        self.partitionSizeCombo.setMinimum(20)
        self.partitionSizeCombo.setMaximum(100)
        self.partitionSizeCombo.setSingleStep(50)
        self.partitionSizeCombo.setProperty("value", 20)
        self.partitionSizeCombo.setObjectName(_fromUtf8("partitionSizeCombo"))
        self.gridLayout.addWidget(self.partitionSizeCombo, 1, 3, 1, 1)
        self.fileSystem = QtGui.QLabel(self.deviceGroup)
        self.fileSystem.setText(_fromUtf8(""))
        self.fileSystem.setObjectName(_fromUtf8("fileSystem"))
        self.gridLayout.addWidget(self.fileSystem, 2, 1, 2, 2)
        self.fileSystemBox = QtGui.QComboBox(self.deviceGroup)
        self.fileSystemBox.setMinimumSize(QtCore.QSize(0, 30))
        self.fileSystemBox.setObjectName(_fromUtf8("fileSystemBox"))
        self.gridLayout.addWidget(self.fileSystemBox, 3, 2, 2, 1)
        spacerItem1 = QtGui.QSpacerItem(233, 25, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.deviceGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 28))
        self.label_8.setMaximumSize(QtCore.QSize(0, 16777215))
        self.label_8.setText(_fromUtf8(""))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 4, 1, 1)
        self.label_7 = QtGui.QLabel(self.deviceGroup)
        font = QtGui.QFont()
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.partitionSizeSlider = QtGui.QSlider(self.deviceGroup)
        self.partitionSizeSlider.setStyleSheet(_fromUtf8("QSlider::groove:horizontal {\n"
"                     height: 12px;\n"
"                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #FFFFFF);\n"
"                     margin: 2px 0;\n"
"                 }\n"
"\n"
"                 QSlider::handle:horizontal {\n"
"                     background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5A2848, stop:1 #8f8f8f);\n"
"                     border: 1px solid #5c5c5c;\n"
"                     width: 18px;\n"
"                     margin: 0 0;\n"
"                     border-radius: 2px;\n"
"                 }\n"
""))
        self.partitionSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.partitionSizeSlider.setObjectName(_fromUtf8("partitionSizeSlider"))
        self.gridLayout.addWidget(self.partitionSizeSlider, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.deviceGroup)
        spacerItem2 = QtGui.QSpacerItem(20, 41, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem2)
        self.optionCheck = QtGui.QCheckBox(partitioneditwdiget)
        self.optionCheck.setObjectName(_fromUtf8("optionCheck"))
        self.verticalLayout.addWidget(self.optionCheck)
        spacerItem3 = QtGui.QSpacerItem(20, 42, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(236, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.buttonBox = QtGui.QDialogButtonBox(partitioneditwdiget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(partitioneditwdiget)
        QtCore.QMetaObject.connectSlotsByName(partitioneditwdiget)

    def retranslateUi(self, partitioneditwdiget):
        self.label_4.setText(i18n("Use :"))
        self.label_5.setText(i18n("Size :"))
        self.partitionSizeCombo.setSuffix(i18n(" MB"))
        self.label_7.setText(i18n("File System :"))
        self.optionCheck.setText(i18n("Force to be primary partition"))

