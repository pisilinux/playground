# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/volumegroup.ui'
#
# Created: Mon Nov 24 20:29:55 2014
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

class Ui_VolumeGroupWidget(object):
    def setupUi(self, VolumeGroupWidget):
        VolumeGroupWidget.setObjectName(_fromUtf8("VolumeGroupWidget"))
        VolumeGroupWidget.resize(560, 591)
        VolumeGroupWidget.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(VolumeGroupWidget)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(VolumeGroupWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(VolumeGroupWidget)
        self.name.setMinimumSize(QtCore.QSize(0, 30))
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(VolumeGroupWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.physicalExtends = QtGui.QComboBox(VolumeGroupWidget)
        self.physicalExtends.setMinimumSize(QtCore.QSize(0, 30))
        self.physicalExtends.setObjectName(_fromUtf8("physicalExtends"))
        self.gridLayout.addWidget(self.physicalExtends, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(VolumeGroupWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.physicals = QtGui.QListWidget(VolumeGroupWidget)
        self.physicals.setObjectName(_fromUtf8("physicals"))
        self.gridLayout.addWidget(self.physicals, 2, 1, 2, 2)
        spacerItem = QtGui.QSpacerItem(78, 98, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(VolumeGroupWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_5 = QtGui.QLabel(VolumeGroupWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(VolumeGroupWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.logicalVolumesTree = QtGui.QTreeWidget(self.groupBox)
        self.logicalVolumesTree.setAllColumnsShowFocus(False)
        self.logicalVolumesTree.setObjectName(_fromUtf8("logicalVolumesTree"))
        self.logicalVolumesTree.headerItem().setText(0, _fromUtf8("Name"))
        self.gridLayout_2.addWidget(self.logicalVolumesTree, 0, 0, 3, 1)
        self.addButton = QtGui.QPushButton(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout_2.addWidget(self.addButton, 0, 1, 1, 1)
        self.editButton = QtGui.QPushButton(self.groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/document-edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon1)
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.gridLayout_2.addWidget(self.editButton, 1, 1, 1, 1)
        self.deleteButton = QtGui.QPushButton(self.groupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/draw-eraser.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon2)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.gridLayout_2.addWidget(self.deleteButton, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 8, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(VolumeGroupWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 2, 1, 1)
        self.totalSpace = QtGui.QLabel(VolumeGroupWidget)
        self.totalSpace.setText(_fromUtf8(""))
        self.totalSpace.setObjectName(_fromUtf8("totalSpace"))
        self.gridLayout.addWidget(self.totalSpace, 4, 1, 1, 2)
        self.freeSpace = QtGui.QLabel(VolumeGroupWidget)
        self.freeSpace.setText(_fromUtf8(""))
        self.freeSpace.setObjectName(_fromUtf8("freeSpace"))
        self.gridLayout.addWidget(self.freeSpace, 6, 1, 1, 2)
        self.label_4 = QtGui.QLabel(VolumeGroupWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.usedSpace = QtGui.QLabel(VolumeGroupWidget)
        self.usedSpace.setText(_fromUtf8(""))
        self.usedSpace.setObjectName(_fromUtf8("usedSpace"))
        self.gridLayout.addWidget(self.usedSpace, 5, 1, 1, 1)

        self.retranslateUi(VolumeGroupWidget)
        QtCore.QMetaObject.connectSlotsByName(VolumeGroupWidget)

    def retranslateUi(self, VolumeGroupWidget):
        self.label.setText(i18n("Volume Group Name:"))
        self.label_2.setText(i18n("Physical Extends"))
        self.label_3.setText(i18n("Physical Volumes to use:"))
        self.label_6.setText(i18n("Total Space:"))
        self.label_5.setText(i18n("Free Space:"))
        self.groupBox.setTitle(i18n("Logical Volumes"))
        self.logicalVolumesTree.headerItem().setText(1, i18n("Mountpoint"))
        self.logicalVolumesTree.headerItem().setText(2, i18n("Size"))
        self.addButton.setText(i18n("Add"))
        self.editButton.setText(i18n("Edit"))
        self.deleteButton.setText(i18n("Delete"))
        self.label_4.setText(i18n("Used Space:"))

