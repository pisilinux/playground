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

# System
import sys
import dbus

# Qt Stuff
from PyQt4 import QtGui
from PyQt4 import QtCore

# Application Stuff
from diskmanager import about
from diskmanager.main import MainWidget

# Pds stuff
import diskmanager.context as ctx

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)

if ctx.Pds.session == ctx.pds.Kde4:
    def CreatePlugin(widget_parent, parent, component_data):
        from diskmanager.kcmodule import Module
        return Module(component_data, parent)

if __name__ == "__main__":

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)

    if ctx.Pds.session == ctx.pds.Kde4:
        # PyKDE4 Stuff
        from PyKDE4.kdeui import KApplication
        from PyKDE4.kdecore import KCmdLineArgs

        # Set Command Line arguments
        KCmdLineArgs.init(sys.argv, about.aboutData)

        # Create a KApplication instance
        app = KApplication()

        # Create Main Window
        window = MainWindow()
        window.show()

    else:

        # Pds Stuff
        from pds.quniqueapp import QUniqueApplication
        from diskmanager.context import KIcon, i18n

        # Create Main Window
        app = QUniqueApplication(sys.argv, catalog=about.appName)
        window = MainWindow()
        window.show()
        window.resize(640,480)

        # Set Main Window Title and Icon
        window.setWindowTitle(i18n(about.PACKAGE))
        window.setWindowIcon(KIcon(about.icon))

    # Run the application
    app.exec_()
