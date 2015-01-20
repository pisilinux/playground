# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/collectionitem.ui'
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

class Ui_CollectionItem(object):
    def setupUi(self, CollectionItem):
        CollectionItem.setObjectName(_fromUtf8("CollectionItem"))
        CollectionItem.resize(391, 482)
        self.gridLayout_3 = QtGui.QGridLayout(CollectionItem)
        self.gridLayout_3.setContentsMargins(15, 3, 15, 15)
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(5)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.icon = QtGui.QLabel(CollectionItem)
        self.icon.setMinimumSize(QtCore.QSize(32, 32))
        self.icon.setMaximumSize(QtCore.QSize(32, 32))
        self.icon.setText(_fromUtf8(""))
        self.icon.setPixmap(QtGui.QPixmap(_fromUtf8("pardus_logo.png")))
        self.icon.setScaledContents(True)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.horizontalLayout.addWidget(self.icon)
        self.header = QtGui.QLabel(CollectionItem)
        self.header.setMinimumSize(QtCore.QSize(0, 32))
        self.header.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet(_fromUtf8("color:white"))
        self.header.setText(_fromUtf8("Header"))
        self.header.setObjectName(_fromUtf8("header"))
        self.horizontalLayout.addWidget(self.header)
        self.horizontalLayout.setStretch(1, 2)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.container = QtGui.QScrollArea(CollectionItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.container.sizePolicy().hasHeightForWidth())
        self.container.setSizePolicy(sizePolicy)
        self.container.setStyleSheet(_fromUtf8("background-color: rgba(0,0,0,0)"))
        self.container.setFrameShape(QtGui.QFrame.NoFrame)
        self.container.setWidgetResizable(True)
        self.container.setObjectName(_fromUtf8("container"))
        self.widget = QtGui.QWidget()
        self.widget.setGeometry(QtCore.QRect(0, 0, 346, 275))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.description = QtGui.QLabel(self.widget)
        self.description.setStyleSheet(_fromUtf8("color:white"))
        self.description.setText(_fromUtf8("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus a tortor risus, ac imperdiet magna. Vivamus elementum lacinia mauris. Etiam fringilla porta posuere. Sed vulputate bibendum sollicitudin. Praesent in neque non neque pellentesque dictum. Maecenas ut massa augue, in dapibus ipsum. Ut mollis augue eu lorem vulputate interdum. Ut cursus ligula eget urna aliquet suscipit adipiscing massa posuere. In luctus, est ac placerat consequat, neque dolor rhoncus ipsum, vel euismod neque lorem eu erat. Duis nulla nisi, dignissim suscipit commodo id, aliquet at felis. Phasellus pretium ultricies justo, nec ultricies nisl hendrerit ut. Proin consectetur faucibus mauris ac feugiat. Fusce ut ante sit amet mi porta tristique. Curabitur venenatis magna ante. Donec diam velit, cursus in auctor et, ultricies vitae magna. Donec mauris dolor, pharetra id vehicula ut, accumsan non lectus. Proin aliquet turpis in erat convallis eget laoreet turpis rutrum."))
        self.description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.description.setWordWrap(True)
        self.description.setObjectName(_fromUtf8("description"))
        self.gridLayout.addWidget(self.description, 0, 0, 1, 1)
        self.container.setWidget(self.widget)
        self.gridLayout_3.addWidget(self.container, 1, 0, 1, 1)

        self.retranslateUi(CollectionItem)
        QtCore.QMetaObject.connectSlotsByName(CollectionItem)

    def retranslateUi(self, CollectionItem):
        CollectionItem.setWindowTitle(i18n("Form"))

