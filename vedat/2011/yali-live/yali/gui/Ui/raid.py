# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/raid.ui'
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

class Ui_RaidWidget(object):
    def setupUi(self, RaidWidget):
        RaidWidget.setObjectName(_fromUtf8("RaidWidget"))
        RaidWidget.resize(580, 589)
        self.gridLayout = QtGui.QGridLayout(RaidWidget)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.raidMinorLabel = QtGui.QLabel(RaidWidget)
        self.raidMinorLabel.setObjectName(_fromUtf8("raidMinorLabel"))
        self.gridLayout.addWidget(self.raidMinorLabel, 0, 0, 1, 2)
        self.raidMinors = QtGui.QComboBox(RaidWidget)
        self.raidMinors.setMinimumSize(QtCore.QSize(0, 30))
        self.raidMinors.setObjectName(_fromUtf8("raidMinors"))
        self.gridLayout.addWidget(self.raidMinors, 0, 2, 1, 2)
        self.label = QtGui.QLabel(RaidWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.mountpointMenu = QtGui.QComboBox(RaidWidget)
        self.mountpointMenu.setMinimumSize(QtCore.QSize(0, 30))
        self.mountpointMenu.setStyleSheet(_fromUtf8("color: #333333"))
        self.mountpointMenu.setEditable(True)
        self.mountpointMenu.setObjectName(_fromUtf8("mountpointMenu"))
        self.mountpointMenu.addItem(_fromUtf8(""))
        self.mountpointMenu.setItemText(0, _fromUtf8(""))
        self.gridLayout.addWidget(self.mountpointMenu, 1, 2, 1, 2)
        self.filesystemLabel = QtGui.QLabel(RaidWidget)
        self.filesystemLabel.setObjectName(_fromUtf8("filesystemLabel"))
        self.gridLayout.addWidget(self.filesystemLabel, 2, 0, 1, 2)
        self.filesystemMenu = QtGui.QComboBox(RaidWidget)
        self.filesystemMenu.setMinimumSize(QtCore.QSize(0, 30))
        self.filesystemMenu.setObjectName(_fromUtf8("filesystemMenu"))
        self.gridLayout.addWidget(self.filesystemMenu, 2, 2, 1, 2)
        self.formatRadio = QtGui.QRadioButton(RaidWidget)
        self.formatRadio.setObjectName(_fromUtf8("formatRadio"))
        self.gridLayout.addWidget(self.formatRadio, 3, 0, 1, 2)
        self.formatCombo = QtGui.QComboBox(RaidWidget)
        self.formatCombo.setEnabled(False)
        self.formatCombo.setMinimumSize(QtCore.QSize(0, 30))
        self.formatCombo.setObjectName(_fromUtf8("formatCombo"))
        self.gridLayout.addWidget(self.formatCombo, 3, 2, 1, 2)
        self.migrateRadio = QtGui.QRadioButton(RaidWidget)
        self.migrateRadio.setObjectName(_fromUtf8("migrateRadio"))
        self.gridLayout.addWidget(self.migrateRadio, 4, 0, 1, 2)
        self.migrateCombo = QtGui.QComboBox(RaidWidget)
        self.migrateCombo.setEnabled(False)
        self.migrateCombo.setMinimumSize(QtCore.QSize(0, 30))
        self.migrateCombo.setObjectName(_fromUtf8("migrateCombo"))
        self.gridLayout.addWidget(self.migrateCombo, 4, 2, 1, 2)
        self.raidLevelLabel = QtGui.QLabel(RaidWidget)
        self.raidLevelLabel.setObjectName(_fromUtf8("raidLevelLabel"))
        self.gridLayout.addWidget(self.raidLevelLabel, 5, 0, 1, 2)
        self.raidLevels = QtGui.QComboBox(RaidWidget)
        self.raidLevels.setMinimumSize(QtCore.QSize(0, 30))
        self.raidLevels.setObjectName(_fromUtf8("raidLevels"))
        self.gridLayout.addWidget(self.raidLevels, 5, 2, 1, 2)
        self.label_5 = QtGui.QLabel(RaidWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 2)
        self.raidMembers = QtGui.QListWidget(RaidWidget)
        self.raidMembers.setObjectName(_fromUtf8("raidMembers"))
        self.gridLayout.addWidget(self.raidMembers, 6, 2, 1, 2)
        self.spareLabel = QtGui.QLabel(RaidWidget)
        self.spareLabel.setObjectName(_fromUtf8("spareLabel"))
        self.gridLayout.addWidget(self.spareLabel, 7, 0, 1, 2)
        self.spareSpin = QtGui.QSpinBox(RaidWidget)
        self.spareSpin.setMinimumSize(QtCore.QSize(0, 30))
        self.spareSpin.setObjectName(_fromUtf8("spareSpin"))
        self.gridLayout.addWidget(self.spareSpin, 7, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RaidWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 7, 3, 1, 1)

        self.retranslateUi(RaidWidget)
        QtCore.QObject.connect(self.formatRadio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.formatCombo.setEnabled)
        QtCore.QObject.connect(self.migrateRadio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.migrateCombo.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(RaidWidget)

    def retranslateUi(self, RaidWidget):
        self.raidMinorLabel.setText(i18n("Raid Device:"))
        self.label.setText(i18n("Use:"))
        self.filesystemLabel.setText(i18n("Filesystem:"))
        self.formatRadio.setText(i18n("Format"))
        self.migrateRadio.setText(i18n("Migrate"))
        self.raidLevelLabel.setText(i18n("Raid Level:"))
        self.label_5.setText(i18n("Raid Members:"))
        self.spareLabel.setText(i18n("Number of spares:"))

