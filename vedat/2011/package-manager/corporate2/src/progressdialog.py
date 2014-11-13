#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QSize

from pmutils import *
from pds.gui import *
from pds.qprogressindicator import QProgressIndicator
from ui_progressdialog_v4 import Ui_ProgressDialog
import backend

class ProgressDialog(PAbstractBox, Ui_ProgressDialog):

    def __init__(self, state, parent=None):
        PAbstractBox.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.state = state
        self.setupUi(self)

        self.busy = QProgressIndicator(self, "white")
        self.busy.setMinimumSize(QSize(48, 48))
        self.mainLayout.addWidget(self.busy)

        # PDS Settings
        self._animation = 2
        self._duration = 1
        self.last_msg = None
        self.enableOverlay()
        self.setOverlayOpacity(150)
        self._disable_parent_in_shown = True

        self.registerFunction(FINISHED, self.busy.startAnimation)
        self.registerFunction(OUT, self.busy.stopAnimation)

        self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancel)
        self.cancelButton.setIcon(KIcon("cancel"))
        self.parent = parent

        self.setStyleSheet("QLabel, QTextEdit, QTextBrowser{background:rgba(0,0,0,0);color:white;}")

        self._last_action = ''
        self._shown = False

    def _show(self):
        self.animate(start = MIDCENTER, stop = MIDCENTER)
        self._shown = True

    def _hide(self):
        if self._shown:
            self.animate(direction = OUT, start = MIDCENTER, stop = MIDCENTER)
            self.parent.setWindowTitle(i18n("Package Manager"))
            self._shown = False

    def updateProgress(self, progress):
        self.busy.stopAnimation()
        self.busy.hide()
        self.widget.show()
        if not self.isVisible():
            if not self.parent.cw._started:
                self.disableCancel()
            self._show()
        self.progressBar.setValue(progress)
        self.percentage.setText(i18n("<p align='right'>%1 %</p>", progress))
        self.parent.setWindowTitle(i18n("Operation - %1%", progress))

    def updateOperation(self, operation, arg):
        if operation in [i18n("configuring"),  i18n("extracting")]:
            self.disableCancel()

        if operation == "updatingrepo":
            operationInfo = i18n("Downloading package list of %1", arg)
        else:
            operationInfo = i18n('%1 %2', operation, arg)

        self.operationInfo.setText(operationInfo)

    def updateStatus(self, packageNo, totalPackages, operation):
        text = i18n("[%1 / %2]", packageNo, totalPackages)
        self.actionLabel.setText("%s %s" % (text, self._last_action))

    def updateRemainingTime(self, time):
        self.timeRemaining.setText("<p align='right'>%s</p>" % time)

    def updateCompletedInfo(self, completed, total, rate):
        text = i18n("%1 / %2, %3", completed, total, rate)
        self.completedInfo.setText(text)

    def updateActionLabel(self, action):
        self.actionLabel.setText("<i>%s</i>" % self.state.getActionCurrent(action))
        self._last_action = self.actionLabel.toPlainText()

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

    def disableCancel(self):
        self.cancelButton.setEnabled(False)

    def reset(self):
        self.widget.hide()
        self.busy.show()

        self.actionLabel.setText(i18n("Preparing PiSi..."))
        self.progressBar.setValue(0)
        self.operationInfo.setText("")
        self.completedInfo.setText("")
        self.timeRemaining.setText("<p align='right'>--:--:--</p>")
        self.timeRemaining.show()

    def cancel(self):
        self.widget.hide()
        self.busy.show()

        self.actionLabel.setText(i18n("<b>Cancelling operation...</b>"))
        self.disableCancel()
        QTimer.singleShot(100, self.iface.cancel)

    def repoOperationView(self):
        self.timeRemaining.setText("")
        self.timeRemaining.hide()
