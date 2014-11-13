#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtCore, QtGui
from pds.gui import *
from PyKDE4.kdeui import KIcon
from pds.qprogressindicator import QProgressIndicator
from ui_message import Ui_MessageBox

class PMessageBox(PAbstractBox):

    # STYLE SHEET
    STYLE = """color:white;font-size:16pt;"""
    OUT_POS  = MIDCENTER
    IN_POS   = MIDCENTER
    STOP_POS = MIDCENTER

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)
        self.ui = Ui_MessageBox()
        self.ui.setupUi(self)

        self.busy = QProgressIndicator(self, "white")
        self.busy.setMinimumSize(QtCore.QSize(32, 32))
        self.busy.hide()
        self.ui.mainLayout.insertWidget(1, self.busy)

        self._animation = 2
        self._duration = 500
        self.last_msg = None
        self.setStyleSheet(PMessageBox.STYLE)
        self.enableOverlay()
        self.hide()

    def showMessage(self, message, icon = None, busy = False):
        self.ui.label.setText(message)

        if busy:
            self.busy.busy()
            self.ui.icon.hide()
        else:
            if icon:
                if type(icon) == str:
                    icon = KIcon(icon).pixmap(32,32)
                self.ui.icon.setPixmap(QtGui.QPixmap(icon))
                self.ui.icon.show()
            else:
                self.ui.icon.hide()
            self.busy.hide()

        self.last_msg = self.animate(start = PMessageBox.IN_POS, stop = PMessageBox.STOP_POS)
        QtGui.qApp.processEvents()

    def hideMessage(self, force = False):
        if self.isVisible() or force:
            self.animate(start = PMessageBox.STOP_POS,
                         stop  = PMessageBox.OUT_POS,
                         direction = OUT,
                         dont_animate = True)

