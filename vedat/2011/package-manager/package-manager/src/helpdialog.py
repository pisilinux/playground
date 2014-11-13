# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QTextBrowser
from PyQt4.QtCore import QUrl

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from localedata import *

(MAINAPP, PREFERENCES) = (1, 2)

help_files = {
    MAINAPP     : "main_help.html",
    PREFERENCES : "preferences_help.html"
}

class HelpDialog(QDialog):
    def __init__(self, parent, help):
        QDialog.__init__(self, parent)

        self.setWindowTitle(i18n("Package Manager Help"))
        self.resize(700,500)
        self.setModal(True)

        self.layout = QGridLayout(self)
        self.htmlPart = QTextBrowser(self)
        self.layout.addWidget(self.htmlPart, 1, 1)

        locale = setSystemLocale(justGet = True)

        if locale in ["tr", "es", "en", "fr", "nl", "de", "sv"]:
            self.htmlPart.setSource(
                    QUrl("/usr/share/kde4/apps/package-manager/help/%s/%s" %
                        (locale, help_files[help])))

        else:
            self.htmlPart.setSource(
                    QUrl("/usr/share/kde4/apps/package-manager/help/en/%s" %
                        help_files[help]))

