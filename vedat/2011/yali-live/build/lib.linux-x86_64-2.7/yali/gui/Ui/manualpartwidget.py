# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/manualpartwidget.ui'
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

class Ui_ManualPartWidget(object):
    def setupUi(self, ManualPartWidget):
        ManualPartWidget.setObjectName(_fromUtf8("ManualPartWidget"))
        ManualPartWidget.resize(823, 487)
        ManualPartWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(ManualPartWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(ManualPartWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 250))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 300))
        self.frame.setStyleSheet(_fromUtf8("#frame{\n"
"background-color: rgba(0,0,0,100);\n"
"border-top: 1px solid rgba(255,255,255,60);\n"
"border-bottom: 1px solid rgba(255,255,255,60);\n"
"}\n"
"\n"
"\n"
"QListView {\n"
"     show-decoration-selected: 1; /* make the selection span the entire width of the view */\n"
" }\n"
"\n"
" QListView::item{\n"
"    border-radius: 2px;\n"
"    border:0px;\n"
"padding: 5px\n"
"}\n"
"\n"
" QListView::item:selected {\n"
"border:0px;\n"
" }\n"
"\n"
" QListView::item:selected:!active {\n"
"     background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(129, 3, 3, 255), stop:0.0192308 rgba(160, 35, 25, 255), stop:0.521739 rgba(166, 35, 29, 255), stop:0.531585 rgba(184, 46, 40, 255), stop:0.983696 rgba(168, 78, 74, 255), stop:1 rgba(210, 110, 110, 255));\n"
"\n"
" }\n"
"\n"
" QListView::item:selected:active {\n"
"     background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(129, 3, 3, 255), stop:0.0192308 rgba(160, 35, 25, 255), stop:0.521739 rgba(166, 35, 29, 255), stop:0.531585 rgba(184, 46, 40, 255), stop:0.983696 rgba(168, 78, 74, 255), stop:1 rgba(210, 110, 110, 255));\n"
" }\n"
"\n"
" QListView::item:hover {\n"
"     background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(129, 3, 3, 100), stop:0.0192308 rgba(160, 35, 25, 100), stop:0.521739 rgba(166, 35, 29, 100), stop:0.531585 rgba(184, 46, 40, 100), stop:0.983696 rgba(168, 78, 74, 100), stop:1 rgba(210, 110, 110, 100));\n"
" }"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frame)
        self.gridLayout_5.setContentsMargins(0, 20, 0, 20)
        self.gridLayout_5.setHorizontalSpacing(30)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.deviceTree = QtGui.QTreeWidget(self.frame)
        self.deviceTree.setMaximumSize(QtCore.QSize(650, 16777215))
        self.deviceTree.setStyleSheet(_fromUtf8(""))
        self.deviceTree.setAllColumnsShowFocus(False)
        self.deviceTree.setWordWrap(True)
        self.deviceTree.setHeaderHidden(False)
        self.deviceTree.setObjectName(_fromUtf8("deviceTree"))
        self.deviceTree.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deviceTree.headerItem().setFont(0, font)
        self.deviceTree.headerItem().setTextAlignment(1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deviceTree.headerItem().setFont(1, font)
        self.deviceTree.headerItem().setTextAlignment(2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deviceTree.headerItem().setFont(2, font)
        self.deviceTree.headerItem().setTextAlignment(3, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deviceTree.headerItem().setFont(3, font)
        self.deviceTree.headerItem().setTextAlignment(4, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deviceTree.headerItem().setFont(4, font)
        self.deviceTree.headerItem().setTextAlignment(5, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deviceTree.headerItem().setFont(5, font)
        self.deviceTree.header().setCascadingSectionResizes(True)
        self.deviceTree.header().setHighlightSections(False)
        self.deviceTree.header().setMinimumSectionSize(75)
        self.deviceTree.header().setSortIndicatorShown(False)
        self.deviceTree.header().setStretchLastSection(True)
        self.horizontalLayout_3.addWidget(self.deviceTree)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.newButton = QtGui.QToolButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newButton.sizePolicy().hasHeightForWidth())
        self.newButton.setSizePolicy(sizePolicy)
        self.newButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/expand.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newButton.setIcon(icon)
        self.newButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.newButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.newButton.setAutoRaise(False)
        self.newButton.setArrowType(QtCore.Qt.NoArrow)
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.horizontalLayout.addWidget(self.newButton)
        self.editButton = QtGui.QPushButton(self.frame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/document-edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon1)
        self.editButton.setFlat(True)
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.horizontalLayout.addWidget(self.editButton)
        self.deleteButton = QtGui.QPushButton(self.frame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/draw-eraser.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon2)
        self.deleteButton.setFlat(True)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        self.resetButton = QtGui.QPushButton(self.frame)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/view-refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resetButton.setIcon(icon3)
        self.resetButton.setFlat(True)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.horizontalLayout.addWidget(self.resetButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(ManualPartWidget)
        QtCore.QMetaObject.connectSlotsByName(ManualPartWidget)

    def retranslateUi(self, ManualPartWidget):
        self.deviceTree.setSortingEnabled(False)
        self.deviceTree.headerItem().setText(0, i18n("Device"))
        self.deviceTree.headerItem().setText(1, i18n("Mount Point"))
        self.deviceTree.headerItem().setText(2, i18n("Label"))
        self.deviceTree.headerItem().setText(3, i18n("Type"))
        self.deviceTree.headerItem().setText(4, i18n("Format"))
        self.deviceTree.headerItem().setText(5, i18n("Size"))
        self.newButton.setText(i18n("Create"))
        self.editButton.setText(i18n("Edit"))
        self.deleteButton.setText(i18n("Delete"))
        self.resetButton.setText(i18n("Reset"))

