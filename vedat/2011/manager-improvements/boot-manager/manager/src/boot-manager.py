#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4 import QtCore

from bootmanager.about import *
from bootmanager.main import MainWidget

# Pds stuff
from bootmanager.context import *

if ctx.Pds.session == ctx.pds.Kde4:

    # PyKDE4 Stuff
    from PyKDE4.kdecore import KGlobal
    from PyKDE4.kdeui import KCModule

    import dbus

    class Module(KCModule):
        def __init__(self, component_data, parent):
            KCModule.__init__(self, component_data, parent)

            KGlobal.locale().insertCatalog(catalog)

            if not dbus.get_default_main_loop():
                from dbus.mainloop.qt import DBusQtMainLoop
                DBusQtMainLoop(set_as_default=True)

            MainWidget(self, embed=True)

    def CreatePlugin(widget_parent, parent, component_data):
        """
            Enable plugin if session is Kde
        """
        return Module(component_data, parent)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)

if __name__ == "__main__":

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)


    if ctx.Pds.session == ctx.pds.Kde4:

        # Boot Manager PyKDE4 Stuff
        from PyKDE4.kdeui import KMainWindow, KApplication, KCModule, KIcon
        from PyKDE4.kdecore import KCmdLineArgs, KGlobal

        # Set Command Line arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        # Create a Kapplication instance
        app = KApplication()

        # Create Main Window
        window = MainWindow()
        window.show()

    else:
        # Boot Manager Pds stuff
        from pds.quniqueapp import QUniqueApplication
        from bootmanager.context import KIcon, i18n

        # Create a QUniqueApplication instance
        app=QUniqueApplication(sys.argv, catalog="boot-manager")

        # Create Main Window
        window= MainWindow()

        window.show()
        window.resize(640,480)

        # Set Main  Window Title
        window.setWindowTitle(i18n("Boot Manager"))

        # Set Main Window Icon
        window.setWindowIcon(KIcon("computer"))

    # Run the application
    app.exec_()
