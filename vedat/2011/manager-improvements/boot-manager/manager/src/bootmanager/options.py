#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui


# UI
from bootmanager.ui_options import Ui_OptionsWidget

class OptionsWidget(QtGui.QWidget, Ui_OptionsWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.spinTimeout.valueChanged.connect(parent.slotTimeoutChanged)

    def getTimeout(self):
        return self.spinTimeout.value()

    def setTimeout(self, timeout):
        self.spinTimeout.blockSignals(True)
        self.spinTimeout.setValue(int(timeout))
        self.spinTimeout.blockSignals(False)
