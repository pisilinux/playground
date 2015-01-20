# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/license.ui'
#
# Created: Mon Nov 24 20:29:51 2014
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

class Ui_LicenseWidget(object):
    def setupUi(self, LicenseWidget):
        LicenseWidget.setObjectName(_fromUtf8("LicenseWidget"))
        LicenseWidget.resize(732, 496)
        LicenseWidget.setWindowTitle(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(LicenseWidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.frame = QtGui.QFrame(LicenseWidget)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pix = QtGui.QLabel(self.frame)
        self.pix.setMaximumSize(QtCore.QSize(222, 146))
        self.pix.setText(_fromUtf8(""))
        self.pix.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/welcome.png")))
        self.pix.setScaledContents(True)
        self.pix.setWordWrap(False)
        self.pix.setObjectName(_fromUtf8("pix"))
        self.horizontalLayout_2.addWidget(self.pix)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setContentsMargins(10, -1, 10, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.disclamer = QtGui.QLabel(self.frame)
        self.disclamer.setMinimumSize(QtCore.QSize(350, 0))
        self.disclamer.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.disclamer.setFont(font)
        self.disclamer.setLineWidth(1)
        self.disclamer.setMidLineWidth(0)
        self.disclamer.setScaledContents(False)
        self.disclamer.setAlignment(QtCore.Qt.AlignCenter)
        self.disclamer.setWordWrap(True)
        self.disclamer.setIndent(0)
        self.disclamer.setObjectName(_fromUtf8("disclamer"))
        self.verticalLayout.addWidget(self.disclamer)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.accept = QtGui.QCheckBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accept.sizePolicy().hasHeightForWidth())
        self.accept.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accept.setFont(font)
        self.accept.setCheckable(True)
        self.accept.setObjectName(_fromUtf8("accept"))
        self.horizontalLayout.addWidget(self.accept)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(LicenseWidget)
        QtCore.QMetaObject.connectSlotsByName(LicenseWidget)

    def retranslateUi(self, LicenseWidget):
        self.disclamer.setText(i18n("Before installing Pardus on your computer, please read and accept the terms of free / open source licenses of the softwares included in this installation medium. <a href=\"#\"><span style=\" text-decoration: underline; color:#56a2c0;\">License texts</span></a>"))
        self.accept.setText(i18n("I understand and accept the terms"))

