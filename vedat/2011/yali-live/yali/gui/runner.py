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
#

import os
import sys
import imp
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QTimer
from PyQt4.Qt import QStyleFactory
from PyQt4.Qt import QObject
from PyQt4.Qt import QShortcut
from PyQt4.Qt import Qt
from PyQt4.Qt import QApplication
from PyQt4.Qt import SIGNAL
from PyQt4.Qt import SLOT
from PyQt4.Qt import QKeySequence
from PyQt4.Qt import QTranslator
from PyQt4.Qt import QLocale
from PyQt4.Qt import QLibraryInfo

import yali
import yali.util
import yali.context as ctx
import yali.gui
import yali.gui.YaliWindow

class Runner:

    _window = None
    _application = None

    def __init__(self):
        self._application = QApplication(sys.argv)
        self._window = None
        # Main Window Initialized..
        try:
            self._window = yali.gui.YaliWindow.Widget()
        except yali.Error, msg:
            ctx.logger.debug(msg)
            sys.exit(1)

        self._translator = QTranslator()
        self._translator.load("qt_" + QLocale.system().name(), QLibraryInfo.location(QLibraryInfo.TranslationsPath))

        ctx.mainScreen = self._window

        screens = self._get_screens(ctx.flags.install_type)
        self._set_steps(screens)

        # These shorcuts for developers :)
        prevScreenShortCut = QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_F1), self._window)
        nextScreenShortCut = QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_F2), self._window)
        QObject.connect(prevScreenShortCut, SIGNAL("activated()"), self._window.slotBack)
        QObject.connect(nextScreenShortCut, SIGNAL("activated()"), self._window.slotNext)

        # VBox utils
        ctx.logger.debug("Starting VirtualBox tools..")
        #FIXME:sh /etc/X11/Xsession.d/98-vboxclient.sh
        yali.util.run_batch("VBoxClient", ["--autoresize"])
        yali.util.run_batch("VBoxClient", ["--clipboard"])

        # Cp Reboot, ShutDown
        yali.util.run_batch("cp", ["/sbin/reboot", "/tmp/reboot"])
        yali.util.run_batch("cp", ["/sbin/shutdown", "/tmp/shutdown"])

        # base connections
        QObject.connect(self._application, SIGNAL("lastWindowClosed()"),
                        self._application, SLOT("quit()"))
        QObject.connect(self._window, SIGNAL("signalProcessEvents"),
                        self._application.processEvents)
        QObject.connect(self._application.desktop(), SIGNAL("resized(int)"),
                        self._reinit_screen)

        # Font Resize
        fontMinusShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus), self._window)
        fontPlusShortCut  = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus) , self._window)
        QObject.connect(fontMinusShortCut, SIGNAL("activated()"), self._window.setFontMinus)
        QObject.connect(fontPlusShortCut , SIGNAL("activated()"), self._window.setFontPlus)

    def _reinit_screen(self):
        QTimer.singleShot(700,self._init_screen)

    def _init_screen(self):
        # We want it to be a full-screen window
        # inside the primary display.
        screen = self._application.desktop().screenGeometry()
        self._window.resize(screen.size())
        self._window.setMaximumSize(screen.size())
        self._window.move(screen.topLeft())
        self._window.show()

    def _get_screens(self, install_type):
        screens = []
        ctx.logger.info("Install type is %s" % ctx.STEP_TYPE_STRINGS[install_type])
        for name in yali.gui.GUI_STEPS[install_type]:
            screenClass = None
            moduleName = ""
            try:
                module_name  = yali.gui.stepToClass[name]
                found = imp.find_module(module_name, yali.gui.__path__)
                loaded = imp.load_module(module_name, *found)
                screenClass = loaded.__dict__["Widget"]
            except ImportError, msg:
                ctx.logger.debug(msg)
                rc = ctx.interface.messageWindow(_("Error!"),
                                                 _("An error occurred when attempting "
                                                   "to load an installer interface "
                                                   "component.\n\nclassName = %s.Widget") % module_name,
                                                 type="custom", customIcon="warning",
                                                 customButtons=[_("Exit"), _("Retry")])
                if not rc:
                    sys.exit(1)
            else:
                screens.append(screenClass)

        return screens


    def _set_steps(self, screens):
        self._window.createWidgets(screens)
        self._window.setCurrent(ctx.flags.startup)

    def run(self):
        # Use default theme;
        # if you use different Qt4 theme our works looks ugly :)
        self._application.setStyle(QStyleFactory.create('Plastique'))
        self._init_screen()

        self._application.installTranslator(self._translator)

        # For testing..
        # self._window.resize(QSize(800,600))

        # Run run run
        self._application.exec_()

