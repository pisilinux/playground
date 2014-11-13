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

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# UI
from usermanager.ui_question import Ui_DialogQuestion

class DialogQuestion(QtGui.QDialog, Ui_DialogQuestion):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.pixmapIcon.setPixmap(kdeui.KIcon("dialog-information").pixmap(48, 48))

    def setQuestion(self, question):
        self.labelQuestion.setText(question)

    def setCheckBox(self, message):
        self.checkBox.setText(message)

    def getCheckBox(self):
        return self.checkBox.checkState() == QtCore.Qt.Checked
