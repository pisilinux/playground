# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/autopartwidget.ui'
#
# Created: Mon Nov 24 20:29:47 2014
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

class Ui_AutoPartWidget(object):
    def setupUi(self, AutoPartWidget):
        AutoPartWidget.setObjectName(_fromUtf8("AutoPartWidget"))
        AutoPartWidget.resize(800, 365)
        AutoPartWidget.setWindowTitle(_fromUtf8(""))
        AutoPartWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout_2 = QtGui.QGridLayout(AutoPartWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(30)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.frame = QtGui.QFrame(AutoPartWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 250))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 250))
        self.frame.setStyleSheet(_fromUtf8("#frame{\n"
"    background-color: rgba(0,0,0,100);\n"
"    background-repeat: no-repeat;\n"
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
""))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame)
        self.gridLayout_4.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_4.setHorizontalSpacing(30)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pix = QtGui.QLabel(self.frame)
        self.pix.setMaximumSize(QtCore.QSize(230, 16777215))
        self.pix.setText(_fromUtf8(""))
        self.pix.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/partitionmanager-big.png")))
        self.pix.setScaledContents(False)
        self.pix.setWordWrap(False)
        self.pix.setObjectName(_fromUtf8("pix"))
        self.horizontalLayout_2.addWidget(self.pix)
        self.autopartType = QtGui.QListWidget(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autopartType.sizePolicy().hasHeightForWidth())
        self.autopartType.setSizePolicy(sizePolicy)
        self.autopartType.setMinimumSize(QtCore.QSize(0, 0))
        self.autopartType.setMaximumSize(QtCore.QSize(16777215, 165))
        self.autopartType.setStyleSheet(_fromUtf8("#autopartType{\n"
"background-color: rgba(255, 255, 255, 0);\n"
"color: white;\n"
"border:0px;\n"
"font-size: 14px;\n"
"text-decoration: normal;\n"
"}"))
        self.autopartType.setFrameShape(QtGui.QFrame.NoFrame)
        self.autopartType.setLineWidth(0)
        self.autopartType.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.autopartType.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.autopartType.setAutoScroll(True)
        self.autopartType.setAutoScrollMargin(16)
        self.autopartType.setAlternatingRowColors(False)
        self.autopartType.setIconSize(QtCore.QSize(30, 30))
        self.autopartType.setFlow(QtGui.QListView.TopToBottom)
        self.autopartType.setProperty("isWrapping", False)
        self.autopartType.setResizeMode(QtGui.QListView.Adjust)
        self.autopartType.setLayoutMode(QtGui.QListView.SinglePass)
        self.autopartType.setSpacing(0)
        self.autopartType.setModelColumn(0)
        self.autopartType.setUniformItemSizes(False)
        self.autopartType.setBatchSize(100)
        self.autopartType.setObjectName(_fromUtf8("autopartType"))
        item = QtGui.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/partscheme-all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.autopartType.addItem(item)
        item = QtGui.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/partscheme-shrink.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        self.autopartType.addItem(item)
        item = QtGui.QListWidgetItem()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/partscheme-freespace.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.autopartType.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.autopartType.addItem(item)
        self.horizontalLayout_2.addWidget(self.autopartType)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(AutoPartWidget)
        QtCore.QMetaObject.connectSlotsByName(AutoPartWidget)

    def retranslateUi(self, AutoPartWidget):
        self.autopartType.setSortingEnabled(False)
        __sortingEnabled = self.autopartType.isSortingEnabled()
        self.autopartType.setSortingEnabled(False)
        item = self.autopartType.item(0)
        item.setText(i18n("Use All Disk"))
        item = self.autopartType.item(1)
        item.setText(i18n("Shrink Current System"))
        item = self.autopartType.item(2)
        item.setText(i18n("Use Free Space"))
        item = self.autopartType.item(3)
        item.setText(i18n("Manual Partitioning"))
        self.autopartType.setSortingEnabled(__sortingEnabled)

