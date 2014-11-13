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

import sys
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import KMainWindow, KApplication, KCModule, KIcon
from PyKDE4.kdecore import KCmdLineArgs, KGlobal

from usermanager.about import aboutData, catalog
from usermanager.main import MainWidget


class MainWindow(KMainWindow):
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)


if __name__ == "__main__":

    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    window = MainWindow()
    window.show()

    app.exec_()


class Module(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(catalog)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default = True)

        MainWidget(self, embed=True)

def CreatePlugin(widget_parent, parent, component_data):
    return Module(component_data, parent)
