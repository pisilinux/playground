#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtGui import qApp
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QActionGroup
from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import *

from ui_mainwindow import Ui_MainWindow

from mainwidget import MainWidget
from pdswidgets import PMessageBox
from statemanager import StateManager
from settingsdialog import SettingsDialog

from pds.qprogressindicator import QProgressIndicator
from tray import Tray
from pmutils import *

import backend
import config

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app = None):
        QMainWindow.__init__(self, None)
        self.setupUi(self)

        self.app = app
        self.iface = backend.pm.Iface()

        self.busy = QProgressIndicator(self)
        self.busy.setFixedSize(QSize(20, 20))

        self.setWindowIcon(QIcon(":/data/package-manager.png"))

        self.setCentralWidget(MainWidget(self))
        self.cw = self.centralWidget()

        self.settingsDialog = SettingsDialog(self)

        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()

        self.pdsMessageBox = PMessageBox(self)

    def connectMainSignals(self):
        self.cw.connectMainSignals()
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Tab),self),
                SIGNAL("activated()"), lambda: self.moveTab('next'))
        self.connect(QShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_Tab),self),
                SIGNAL("activated()"), lambda: self.moveTab('prev'))
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F),self),
                SIGNAL("activated()"), self.cw.searchLine.setFocus)
        self.connect(QShortcut(QKeySequence(Qt.Key_F3),self),
                SIGNAL("activated()"), self.cw.searchLine.setFocus)

        self.connect(self.settingsDialog, SIGNAL("packagesChanged()"), self.cw.initialize)
        self.connect(self.settingsDialog, SIGNAL("packageViewChanged()"), self.cw.updateSettings)
        self.connect(self.settingsDialog, SIGNAL("traySettingChanged()"), self.tray.settingsChanged)
        self.connect(self.cw.state, SIGNAL("repositoriesChanged()"), self.tray.populateRepositoryMenu)
        self.connect(self.cw, SIGNAL("repositoriesUpdated()"), self.tray.updateTrayUnread)
        self.connect(qApp, SIGNAL("shutDown()"), self.slotQuit)

    def moveTab(self, direction):
        new_index = self.cw.stateTab.currentIndex() - 1
        if direction == 'next':
            new_index = self.cw.stateTab.currentIndex() + 1
        if new_index not in range(self.cw.stateTab.count()):
            new_index = 0
        self.cw.stateTab.setCurrentIndex(new_index)

    def initializeTray(self):
        self.tray = Tray(self, self.iface)
        self.connect(self.cw.operation, SIGNAL("finished(QString)"), self.trayAction)
        self.connect(self.cw.operation, SIGNAL("finished(QString)"), self.tray.stop)
        self.connect(self.cw.operation, SIGNAL("operationCancelled()"), self.tray.stop)
        self.connect(self.cw.operation, SIGNAL("started(QString)"), self.tray.animate)
        self.connect(self.tray, SIGNAL("showUpdatesSelected()"), self.trayShowUpdates)

    def trayShowUpdates(self):
        self.showUpgradeAction.setChecked(True)

        self.cw.switchState(StateManager.UPGRADE)

        KApplication.kApplication().updateUserTimestamp()

        self.show()
        self.raise_()

    def trayAction(self, operation):
        if not self.isVisible() and operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.tray.showPopup()
        if self.tray.isVisible() and operation in ["System.Manager.updatePackage",
                                                   "System.Manager.installPackage",
                                                   "System.Manager.removePackage"]:
            self.tray.updateTrayUnread()

    def initializeStatusBar(self):
        self.cw.mainLayout.insertWidget(0, self.busy)
        self.statusBar().addPermanentWidget(self.cw.actions, 1)
        self.statusBar().show()

        self.updateStatusBar('')

        self.connect(self.cw, SIGNAL("selectionStatusChanged(QString)"), self.updateStatusBar)
        self.connect(self.cw, SIGNAL("updatingStatus()"), self.statusWaiting)

    def initializeActions(self):
        self.initializeOperationActions()

    def initializeOperationActions(self):

        self.showAllAction = QAction(KIcon(("applications-other", "package_applications")), i18n("All Packages"), self)
        self.connect(self.showAllAction, SIGNAL("triggered()"), lambda:self.cw.switchState(StateManager.ALL))
        self.cw.stateTab.addTab(QWidget(), KIcon(("applications-other", "package_applications")), i18n("All Packages"))

        self.showInstallAction = QAction(KIcon(("list-add", "add")), i18n("Installable Packages"), self)
        self.connect(self.showInstallAction, SIGNAL("triggered()"), lambda:self.cw.switchState(StateManager.INSTALL))
        self.cw.stateTab.addTab(QWidget(), KIcon(("list-add", "add")), i18n("Installable Packages"))

        self.showRemoveAction = QAction(KIcon(("list-remove", "remove")), i18n("Installed Packages"), self)
        self.connect(self.showRemoveAction, SIGNAL("triggered()"), lambda:self.cw.switchState(StateManager.REMOVE))
        self.cw.stateTab.addTab(QWidget(), KIcon(("list-remove", "remove")), i18n("Installed Packages"))

        self.showUpgradeAction = QAction(KIcon(("system-software-update", "gear")), i18n("Updates"), self)
        self.connect(self.showUpgradeAction, SIGNAL("triggered()"), lambda:self.cw.switchState(StateManager.UPGRADE))
        self.cw.stateTab.addTab(QWidget(), KIcon(("system-software-update", "gear")), i18n("Updates"))

        self.showPreferences = QAction(KIcon(("preferences-system", "package_settings")), i18n("Settings"), self)
        self.connect(self.showPreferences, SIGNAL("triggered()"), self.settingsDialog.show)

        self.actionQuit = QAction(KIcon("exit"), i18n("Quit"), self)
        self.actionQuit.setShortcuts(QKeySequence.Quit)
        self.connect(self.actionQuit, SIGNAL("triggered()"), qApp.exit)

        self.cw.menuButton.setMenu(QMenu('MainMenu', self.cw.menuButton))
        self.cw.menuButton.setIcon(KIcon(("preferences-system", "package_settings")))
        self.cw.menuButton.menu().clear()

        self.cw.contentHistory.hide()

        self.cw.menuButton.menu().addAction(self.showPreferences)
        self.cw.menuButton.menu().addSeparator()
        self.cw.menuButton.menu().addAction(self.actionQuit)

        self.cw._states = {self.cw.state.ALL    :(0, self.showAllAction),
                           self.cw.state.INSTALL:(1, self.showInstallAction),
                           self.cw.state.REMOVE :(2, self.showRemoveAction),
                           self.cw.state.UPGRADE:(3, self.showUpgradeAction)}

        self.showAllAction.setChecked(True)
        self.cw.checkUpdatesButton.hide()
        self.cw.checkUpdatesButton.setIcon(KIcon(("view-refresh", "reload")))
        self.cw.showBasketButton.clicked.connect(self.cw.showBasket)

        # Little time left for the new ui
        self.menuBar().setVisible(False)
        self.cw.switchState(self.cw.state.ALL)

    def statusWaiting(self):
        self.updateStatusBar(i18n('Calculating dependencies...'), busy = True)

    def updateStatusBar(self, text, busy = False):
        if text == '':
            text = i18n("Currently your basket is empty.")
            self.busy.hide()
            self.cw.showBasketButton.hide()
        else:
            self.cw.showBasketButton.show()

        if busy:
            self.busy.busy()
            self.cw.showBasketButton.hide()
        else:
            self.busy.hide()

        self.cw.statusLabel.setText(text)
        self.cw.statusLabel.setToolTip(text)

    def queryClose(self):
        if config.PMConfig().systemTray():
            self.hide()
            return False
        return True

    def queryExit(self):
        if not self.iface.operationInProgress():
            if self.tray:
                del self.tray.notification
            return True
        return False

    def slotQuit(self):
        if self.iface.operationInProgress():
            return
