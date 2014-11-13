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

from PyQt4.QtGui import qApp
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QFontMetrics

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import QVariant

from ui_mainwidget_v3 import Ui_MainWidget

from config import PMConfig

from pds.gui import FINISHED, OUT
from pds.thread import PThread

from pmutils import *

from pdswidgets import PMessageBox
from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagemodel import GroupRole
from statemanager import StateManager
from basketdialog import BasketDialog
from statusupdater import StatusUpdater
from summarydialog import SummaryDialog
from progressdialog import ProgressDialog
from packagedelegate import PackageDelegate
from operationmanager import OperationManager

class MainWidget(QWidget, PM, Ui_MainWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.setupUi(self)
        self.parent = parent

        self._selectedGroups = []
        self._preexceptions  = []
        self._postexceptions = []

        self.state = StateManager(self)
        self.currentState = None
        self.completer = None
        self._updatesCheckedOnce = False

        # Search Thread
        self._searchThread = PThread(self, self.startSearch, self.searchFinished)

        self.statusUpdater = StatusUpdater()
        self.basket = BasketDialog(self.state, self.parent)
        self._postexceptions.append(lambda: self.basket.setActionEnabled(True))
        self.searchButton.setIcon(KIcon(("edit-find", "find")))
        self.initializeUpdateTypeList()

        model = PackageModel(self)
        proxy = PackageProxy(self)
        proxy.setSourceModel(model)
        self.packageList.setModel(proxy)
        self.packageList.setItemDelegate(PackageDelegate(self, self.parent))
        self.packageList.setColumnWidth(0, 32)

        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.statusChanged)
        self.connect(self.packageList, SIGNAL("updateRequested()"), self.initialize)

        self.updateSettings()
        self.setActionButton()

        self.operation = OperationManager(self.state)

        self.progressDialog = ProgressDialog(self.state, self.parent)
        self._preexceptions.append(self.progressDialog._hide)
        self.progressDialog.registerFunction(FINISHED, lambda: self.parent.statusBar().setVisible(not self.progressDialog.isVisible()))
        self.progressDialog.registerFunction(OUT, lambda: self.parent.statusBar().show())
        self.summaryDialog = SummaryDialog()

        self.connectOperationSignals()
        self.pdsMessageBox = PMessageBox(self.content)

    def connectMainSignals(self):
        self.connect(self.actionButton, SIGNAL("clicked()"), self.showBasket)
        self.connect(self.checkUpdatesButton, SIGNAL("clicked()"), self.state.updateRepoAction)
        self.connect(self.searchButton, SIGNAL("clicked()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("textEdited(const QString&)"), self.searchLineChanged)
        self.connect(self.searchLine, SIGNAL("returnPressed()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("clearButtonClicked()"), self.groupFilter)
        self.connect(self.typeCombo, SIGNAL("activated(int)"), self.typeFilter)
        self.connect(self.stateTab, SIGNAL("currentChanged(int)"), self.switchState)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), lambda:self.searchButton.setEnabled(False))
        self.connect(self.packageList.select_all, SIGNAL("clicked(bool)"), self.toggleSelectAll)
        self.connect(self.statusUpdater, SIGNAL("selectedInfoChanged(int, QString, int, QString)"), self.emitStatusBarInfo)
        self.connect(self.statusUpdater, SIGNAL("selectedInfoChanged(QString)"), lambda message: self.emit(SIGNAL("selectionStatusChanged(QString)"), message))
        self.connect(self.statusUpdater, SIGNAL("finished()"), self.statusUpdated)

    def initialize(self):
        waitCursor()
        self.searchLine.clear()
        self._started = False
        self._last_packages = None
        self.state.reset()
        self.initializePackageList()
        self.initializeGroupList()
        self.initializeStatusUpdater()
        self.statusChanged()
        self._selectedGroups = []
        self.packageList.select_all.setChecked(False)
        self.initializeBasket()
        self.searchLine.setFocus(True)
        if self.currentState == self.state.UPGRADE:
            if self.groupList.count() == 0:
                QTimer.singleShot(0, \
                lambda: self.pdsMessageBox.showMessage(i18n("All packages are up to date"), icon = "info"))
        if self.groupList.count() > 0:
            if self.state.inUpgrade():
                self.pdsMessageBox.hideMessage(force = True)
        restoreCursor()

    def initializeStatusUpdater(self):
        self.statusUpdater.calculate_deps = not self.state.state == self.state.ALL
        self.statusUpdater.setModel(self.packageList.model().sourceModel())

    def initializeBasket(self):
        waitCursor()
        self.basket.setModel(self.packageList.model().sourceModel())
        restoreCursor()

    def initializePackageList(self):
        self.packageList.model().reset()
        self.packageList.setPackages(self.state.packages())

        if self.completer:
            self.completer.deleteLater()
            del self.completer

        self.completer = QCompleter(self.state.packages(), self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchLine.setCompleter(self.completer)

    def selectComponent(self, component):
        if not self.state.iface.operationInProgress():
            if self.basket.isVisible():
                self.basket._hide()

            self.stateTab.setCurrentIndex(1)
            self.switchState(self.state.INSTALL)

            if component in self.groupList._list:
                self.groupList.setCurrentItem(self.groupList._list[component])
                self.groupFilter()

    def updateSettings(self):
        self.packageList.showComponents = PMConfig().showComponents()
        self.packageList.showIsA = PMConfig().showIsA()
        self.packageList.setFocus()

    def searchLineChanged(self, text):
        self.searchButton.setEnabled(bool(text))
        if text == '':
            self.searchActivated()

    def statusUpdated(self):
        if self.statusUpdater.needsUpdate:
            self.statusUpdater.needsUpdate = False
            self.statusChanged()

    def statusChanged(self):
        self.setActionEnabled()
        if self.statusUpdater.isRunning():
            self.statusUpdater.needsUpdate = True
        else:
            self.emit(SIGNAL("updatingStatus()"))
            self.statusUpdater.start()

    def initializeGroupList(self):
        self.groupList.clear()
        self.groupList._list = {}
        self.groupList.setAlternatingRowColors(True)
        self.groupList.setIconSize(QSize(32, 32))
        self.groupList.setState(self.state)
        self.groupList.addGroups(self.state.groups())
        if self.state.state == self.state.UPGRADE:
            self.typeCombo.show()
        else:
            self.typeCombo.hide()
            self.state._typeFilter = 'normal'
        self.groupFilter()

    def packageFilter(self, text):
        self.packageList.model().setFilterRole(Qt.DisplayRole)
        self.packageList.model().setFilterRegExp(QRegExp(unicode(text), Qt.CaseInsensitive, QRegExp.FixedString))

    def typeFilter(self, index):
        if self.state.state == self.state.UPGRADE:
            filter = self.typeCombo.itemData(index).toString()
            if not self.state._typeFilter == filter:
                self.state._typeFilter = filter
                self.initializeGroupList()

    def groupFilter(self):
        waitCursor()
        self.packageList.resetMoreInfoRow()
        packages = self.state.groupPackages(self.groupList.currentGroup())
        self.packageList.model().setFilterRole(GroupRole)
        self.packageList.model().setFilterPackages(packages)
        self.packageList.scrollToTop()
        self.packageList.select_all.setChecked(self.groupList.currentGroup() in self._selectedGroups)
        restoreCursor()

    def searchActivated(self):
        if self.currentState == self.state.UPGRADE:
            if self.groupList.count() == 0 and not self.searchUsed:
                return

        if not self.searchLine.text() == '':
            self.pdsMessageBox.showMessage(i18n("Searching..."), busy = True)
            self.groupList.lastSelected = None
            self._searchThread.start()
            self.searchUsed = True
        else:
            self.state.cached_packages = None
            self.state.packages()
            self.searchUsed = False
            self.searchFinished()

    def searchFinished(self):
        if self.state.cached_packages == []:
            self.pdsMessageBox.showMessage(i18n("No results found."), "dialog-information")
        else:
            self.pdsMessageBox.hideMessage()
        self.initializeGroupList()

    def startSearch(self):
        searchText = str(self.searchLine.text()).split()
        sourceModel = self.packageList.model().sourceModel()
        self.state.cached_packages = sourceModel.search(searchText)

    def setActionButton(self):
        self.actionButton.setEnabled(False)
        if self.state.state == self.state.ALL:
            menu = QMenu(self.actionButton)
            self.__install_action = menu.addAction(self.state.getActionIcon(self.state.INSTALL),
                                                   self.state.getActionName(self.state.INSTALL),
                                                   self.showBasket)
            self.__remove_action = menu.addAction(self.state.getActionIcon(self.state.REMOVE),
                                                  self.state.getActionName(self.state.REMOVE),
                                                  self.showBasket)
            self.actionButton.setMenu(menu)
        else:
            self.actionButton.setMenu(None)
        self.actionButton.setIcon(self.state.getActionIcon())
        self.actionButton.setText(self.state.getActionName())

    def actionStarted(self, operation):
        self.pdsMessageBox.hideMessage()
        self.progressDialog.reset()
        if not operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            totalPackages = self.packageList.packageCount()
            self.operation.setTotalPackages(totalPackages)
            self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())
        if self.isVisible():
            if operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
                self.progressDialog.repoOperationView()
            if self.basket.isVisible():
                self.basket._hide()
                QTimer.singleShot(0, self.progressDialog._show)
            else:
                self.progressDialog._show()

        if not self._started:
            self.progressDialog.disableCancel()
        else:
            self.progressDialog.enableCancel()

    def actionFinished(self, operation):
        if operation in ("System.Manager.installPackage",
                         "System.Manager.removePackage",
                         "System.Manager.updatePackage"):
            self.notifyFinished()

        if operation == "System.Manager.installPackage" and self._started:
            KIconLoader.updateAvailableIcons()
            self.summaryDialog.setDesktopFiles(self.operation.desktopFiles)
            self.summaryDialog.showSummary()

        if operation in ("System.Manager.updateRepository",
                         "System.Manager.updateAllRepositories"):
            self.emit(SIGNAL("repositoriesUpdated()"))
        self.searchLine.clear()
        self.state.reset()
        self.progressDialog._hide()
        if not self.currentState == self.state.UPGRADE:
            self.switchState(self.currentState)
        self.initialize()

    def actionCancelled(self):
        self.progressDialog._hide()
        self.progressDialog.reset()
        self.switchState(self.currentState)
        self.groupFilter()

    def setActionEnabled(self):
        enabled = self.packageList.isSelected()
        self.actionButton.setEnabled(enabled)
        self.basket.setActionEnabled(enabled)

    def switchState(self, state):
        self.pdsMessageBox.hideMessage()
        self._states[state][1].setChecked(True)
        self.state.setState(state)
        self.currentState = state
        self._selectedGroups = []
        if not state == self.state.HISTORY:
            self.setActionButton()
            self.state.cached_packages = None
            if state == self.state.UPGRADE or (state == self.state.INSTALL and self.groupList.count() == 1):
                if not self._updatesCheckedOnce:
                    self._updatesCheckedOnce = self.state.updateRepoAction(silence = True)
            self.checkUpdatesButton.setHidden(not state == self.state.UPGRADE)
            self.initialize()

    def emitStatusBarInfo(self, packages, packagesSize, extraPackages, extraPackagesSize):
        self.emit(SIGNAL("selectionStatusChanged(QString)"), self.state.statusText(packages, packagesSize, extraPackages, extraPackagesSize))

    def setSelectAll(self, packages=None):
        if packages:
            self.packageList.reverseSelection(packages)

    def setReverseAll(self, packages=None):
        if packages:
            self.packageList.selectAll(packages)

    def toggleSelectAll(self, toggled):
        self._last_packages = self.packageList.model().getFilteredPackages()

        if toggled:
            if self.groupList.currentGroup() not in self._selectedGroups:
                self._selectedGroups.append(self.groupList.currentGroup())
            self.setReverseAll(self._last_packages)
        else:
            if self.groupList.currentGroup() in self._selectedGroups:
                self._selectedGroups.remove(self.groupList.currentGroup())
            self.setSelectAll(self._last_packages)

        self.packageList.setFocus()
        self.statusChanged()

    def showBasket(self):

        if self.basket.isVisible():
            return

        waitCursor()
        self.statusUpdater.wait()

        if self.currentState == self.state.ALL:
            action = {self.__remove_action:self.state.REMOVE,
                      self.__install_action:self.state.INSTALL}.get(self.sender(), self.state.INSTALL)
            if action:
                if action == self.state.REMOVE:
                    installed_packages = self.state.iface.getInstalledPackages()
                    filtered_packages = filter(lambda x: x not in installed_packages, self.basket.model.selectedPackages())
                    if filtered_packages == self.basket.model.selectedPackages():
                        restoreCursor()
                        QMessageBox(i18n("Select packages"),
                                    i18n("You must select at least one installed package"),
                                    QMessageBox.Information, QMessageBox.Ok, 0, 0).exec_()
                        return
                    self.packageList.model().sourceModel().selectPackages(filtered_packages, state = False)

                self.state.state = action

        self.basket._show()
        restoreCursor()

    def initializeUpdateTypeList(self):
        self.typeCombo.clear()
        UPDATE_TYPES = [['normal', i18n('All Updates'), ('system-software-update', 'ledgreen')],
                        ['security', i18n('Security Updates'), ('security-medium', 'ledyellow')],
                        ['critical', i18n('Critical Updates'), ('security-low', 'ledred')]]

        for type in UPDATE_TYPES:
            self.typeCombo.addItem(KIcon(type[2]), type[1], QVariant(type[0]))

