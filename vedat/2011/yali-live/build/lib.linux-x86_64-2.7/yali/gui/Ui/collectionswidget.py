# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/collectionswidget.ui'
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

class Ui_CollectionsWidget(object):
    def setupUi(self, CollectionsWidget):
        CollectionsWidget.setObjectName(_fromUtf8("CollectionsWidget"))
        CollectionsWidget.resize(624, 463)
        CollectionsWidget.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(CollectionsWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(CollectionsWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 270))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 270))
        self.frame.setStyleSheet(_fromUtf8("#frame{background-color: rgba(0,0,0,100)}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(-1, 20, -1, 20)
        self.gridLayout_3.setHorizontalSpacing(30)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setContentsMargins(10, -1, 10, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.collectionList = QtGui.QListWidget(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collectionList.sizePolicy().hasHeightForWidth())
        self.collectionList.setSizePolicy(sizePolicy)
        self.collectionList.setMinimumSize(QtCore.QSize(500, 230))
        self.collectionList.setMaximumSize(QtCore.QSize(500, 230))
        self.collectionList.setStyleSheet(_fromUtf8("#collectionList{background-color: rgba(0,0,0,0);}"))
        self.collectionList.setFrameShape(QtGui.QFrame.NoFrame)
        self.collectionList.setIconSize(QtCore.QSize(0, 0))
        self.collectionList.setSpacing(2)
        self.collectionList.setUniformItemSizes(False)
        self.collectionList.setObjectName(_fromUtf8("collectionList"))
        self.verticalLayout.addWidget(self.collectionList)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(CollectionsWidget)
        QtCore.QMetaObject.connectSlotsByName(CollectionsWidget)

    def retranslateUi(self, CollectionsWidget):
        pass

