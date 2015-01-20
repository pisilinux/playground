# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/createdevicewidget.ui'
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

class Ui_CreateDeviceWidget(object):
    def setupUi(self, CreateDeviceWidget):
        CreateDeviceWidget.setObjectName(_fromUtf8("CreateDeviceWidget"))
        CreateDeviceWidget.resize(529, 468)
        CreateDeviceWidget.setWindowTitle(_fromUtf8(""))
        self.verticalLayout_2 = QtGui.QVBoxLayout(CreateDeviceWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(CreateDeviceWidget)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.partition = QtGui.QRadioButton(self.groupBox_2)
        self.partition.setEnabled(False)
        self.partition.setAutoExclusive(True)
        self.partition.setObjectName(_fromUtf8("partition"))
        self.verticalLayout.addWidget(self.partition)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.partitionLabel = QtGui.QLabel(self.groupBox_2)
        self.partitionLabel.setEnabled(False)
        self.partitionLabel.setObjectName(_fromUtf8("partitionLabel"))
        self.horizontalLayout.addWidget(self.partitionLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.volumeGroup = QtGui.QRadioButton(self.groupBox_2)
        self.volumeGroup.setEnabled(False)
        self.volumeGroup.setAutoExclusive(True)
        self.volumeGroup.setObjectName(_fromUtf8("volumeGroup"))
        self.verticalLayout.addWidget(self.volumeGroup)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.volumeGroupLabel = QtGui.QLabel(self.groupBox_2)
        self.volumeGroupLabel.setEnabled(False)
        self.volumeGroupLabel.setObjectName(_fromUtf8("volumeGroupLabel"))
        self.horizontalLayout_4.addWidget(self.volumeGroupLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.logicalVolume = QtGui.QRadioButton(self.groupBox_2)
        self.logicalVolume.setEnabled(False)
        self.logicalVolume.setObjectName(_fromUtf8("logicalVolume"))
        self.verticalLayout.addWidget(self.logicalVolume)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem2 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.logicalVolumeLabel = QtGui.QLabel(self.groupBox_2)
        self.logicalVolumeLabel.setEnabled(False)
        self.logicalVolumeLabel.setObjectName(_fromUtf8("logicalVolumeLabel"))
        self.horizontalLayout_5.addWidget(self.logicalVolumeLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.physicalVolume = QtGui.QRadioButton(self.groupBox_2)
        self.physicalVolume.setEnabled(False)
        self.physicalVolume.setObjectName(_fromUtf8("physicalVolume"))
        self.verticalLayout.addWidget(self.physicalVolume)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem3 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.physicalVolumeLabel = QtGui.QLabel(self.groupBox_2)
        self.physicalVolumeLabel.setEnabled(False)
        self.physicalVolumeLabel.setObjectName(_fromUtf8("physicalVolumeLabel"))
        self.horizontalLayout_6.addWidget(self.physicalVolumeLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.line_2 = QtGui.QFrame(self.groupBox_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.raidMember = QtGui.QRadioButton(self.groupBox_2)
        self.raidMember.setEnabled(False)
        self.raidMember.setObjectName(_fromUtf8("raidMember"))
        self.verticalLayout.addWidget(self.raidMember)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem4 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.raidArrayLabel = QtGui.QLabel(self.groupBox_2)
        self.raidArrayLabel.setEnabled(False)
        self.raidArrayLabel.setObjectName(_fromUtf8("raidArrayLabel"))
        self.horizontalLayout_3.addWidget(self.raidArrayLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.raidArray = QtGui.QRadioButton(self.groupBox_2)
        self.raidArray.setEnabled(False)
        self.raidArray.setObjectName(_fromUtf8("raidArray"))
        self.verticalLayout.addWidget(self.raidArray)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem5 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.raidMemberLabel = QtGui.QLabel(self.groupBox_2)
        self.raidMemberLabel.setEnabled(False)
        self.raidMemberLabel.setObjectName(_fromUtf8("raidMemberLabel"))
        self.horizontalLayout_2.addWidget(self.raidMemberLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.buttonBox = QtGui.QDialogButtonBox(CreateDeviceWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(CreateDeviceWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateDeviceWidget)

    def retranslateUi(self, CreateDeviceWidget):
        self.partition.setText(i18n("Standard Partition"))
        self.partitionLabel.setText(i18n("General purpose of partition creation"))
        self.volumeGroup.setText(i18n("Volume Group"))
        self.volumeGroupLabel.setText(i18n("Requires at least 1 free LVM formatted partition"))
        self.logicalVolume.setText(i18n("Logical Volume"))
        self.logicalVolumeLabel.setText(i18n("Create Logical Volume on selected Volume Group"))
        self.physicalVolume.setText(i18n("Physical Volume"))
        self.physicalVolumeLabel.setText(i18n("Create LVM formatted partition"))
        self.raidMember.setText(i18n("Raid Member"))
        self.raidArrayLabel.setText(i18n("Create Raid formatted partition"))
        self.raidArray.setText(i18n("Raid Array"))
        self.raidMemberLabel.setText(i18n("Requires at least 2 free Raid formatted partition"))

