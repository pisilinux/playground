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

import re
from os import path

from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtNetwork import QNetworkProxy
from PyQt4.QtCore import *

from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KIcon

import pds
import config
import helpdialog
import repodialog
import pmutils
import backend

from ui_settingsdialog import Ui_SettingsDialog
from pmutils import parse_proxy

Pds = pds.Pds()

class SettingsTab(QObject):
    def __init__(self, settings):
        QObject.__init__(self)
        self.settings = settings
        self.config = config.PMConfig()
        self.iface = backend.pm.Iface()
        self.setupUi()
        self.connectSignals()
        self.changed = False

    def markChanged(self):
        self.changed = True

    def setupUi(self):
        pass

    def connectSignals(self):
        pass

    def save(self):
        pass

    def initialize(self):
        pass

class GeneralSettings(SettingsTab):
    def setupUi(self):
        self.settings.moveUpButton.setIcon(KIcon("arrow-up"))
        self.settings.moveDownButton.setIcon(KIcon("arrow-down"))
        self.settings.addRepoButton.setIcon(KIcon("list-add"))
        self.settings.removeRepoButton.setIcon(KIcon("list-remove"))
        self.initialize()

    def initialize(self):
        self.settings.onlyGuiApp.setChecked(self.config.showOnlyGuiApp())
        self.settings.showComponents.setChecked(self.config.showComponents())
        self.settings.showIsA.setChecked(self.config.showIsA())
        self.settings.intervalCheck.setChecked(self.config.updateCheck())
        self.settings.installUpdates.setChecked(self.config.installUpdatesAutomatically())
        self.settings.intervalSpin.setValue(self.config.updateCheckInterval())
        self.settings.systemTray.setChecked(self.config.systemTray())
        self.settings.hideIfNoUpdate.setChecked(self.config.hideTrayIfThereIsNoUpdate())

    def connectSignals(self):
        self.connect(self.settings.onlyGuiApp, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.showComponents, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.showIsA, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.intervalCheck, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.intervalSpin, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.installUpdates, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.systemTray, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.hideIfNoUpdate, SIGNAL("toggled(bool)"), self.markChanged)

    def save(self):
        if not self.settings.onlyGuiApp.isChecked() == self.config.showOnlyGuiApp():
            self.config.setShowOnlyGuiApp(self.settings.onlyGuiApp.isChecked())
            self.settings.emit(SIGNAL("packagesChanged()"))

        if not self.settings.showComponents.isChecked() == self.config.showComponents():
            self.config.setShowComponents(self.settings.showComponents.isChecked())
            self.settings.emit(SIGNAL("packageViewChanged()"))

        if not self.settings.showIsA.isChecked() == self.config.showIsA():
            self.config.setShowIsA(self.settings.showIsA.isChecked())
            self.settings.emit(SIGNAL("packageViewChanged()"))

        if not self.settings.systemTray.isChecked() == self.config.systemTray() or \
           not self.settings.intervalSpin.value() == self.config.updateCheckInterval() or \
           not self.settings.intervalCheck.isChecked() == self.config.updateCheck() or \
           not self.settings.hideIfNoUpdate.isChecked() == self.config.hideTrayIfThereIsNoUpdate():
            self.config.setSystemTray(self.settings.systemTray.isChecked())
            self.config.setUpdateCheck(self.settings.intervalCheck.isChecked())
            self.config.setUpdateCheckInterval(self.settings.intervalSpin.value())
            self.config.setHideTrayIfThereIsNoUpdate(self.settings.hideIfNoUpdate.isChecked())
            self.settings.emit(SIGNAL("traySettingChanged()"))

        self.config.setInstallUpdatesAutomatically(self.settings.installUpdates.isChecked())

class CacheSettings(SettingsTab):
    def setupUi(self):
        self.initialize()

    def initialize(self):
        config = self.iface.getConfig()

        cache = config.get("general", "package_cache")
        cache_limit = config.get("general", "package_cache_limit")
        cache_limit = int(cache_limit) if cache_limit else 0
        cache_dir = config.get("directories", "cached_packages_dir")
        cache_dir = str(cache_dir) if cache_dir else '/var/cache/pisi/packages'

        # If pisi.conf does not have it yet, default is use package cache
        if not cache or cache == "True":
            enableCache = True
        else:
            enableCache = False

        self.cacheEnabled = enableCache
        self.cacheSize = cache_limit
        self.settings.cacheGroup.setEnabled(self.cacheEnabled)
        self.settings.useCacheCheck.setChecked(enableCache)
        self.settings.useCacheSpin.setValue(cache_limit)
        self.settings.cacheDirPath.setText(cache_dir)

        bandwidth_limit = config.get("general", "bandwidth_limit")
        bandwidth_limit = int(bandwidth_limit) if bandwidth_limit else 0

        self.settings.useBandwidthLimit.setChecked(not bandwidth_limit == 0)
        self.settings.bandwidthSpin.setValue(bandwidth_limit)

    def connectSignals(self):
        self.connect(self.settings.clearCacheButton, SIGNAL("clicked()"), self.clearCache)
        self.connect(self.settings.selectCacheDir, SIGNAL("clicked()"), self.selectCacheDir)
        self.connect(self.settings.useCacheCheck, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useCacheSpin, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.useBandwidthLimit, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.bandwidthSpin, SIGNAL("valueChanged(int)"), self.markChanged)
        self.settings.openCacheDir.clicked.connect(self.openCacheDir)

    def openCacheDir(self):
        cache_dir = unicode(self.settings.cacheDirPath.text())
        if path.exists(cache_dir):
            QDesktopServices.openUrl(QUrl("file://%s" % cache_dir, QUrl.TolerantMode))

    def selectCacheDir(self):
        selected_dir = QFileDialog.getExistingDirectory(self.settings, i18n("Open Directory"), "/",
                                                        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if not selected_dir == '':
            if not selected_dir == self.settings.cacheDirPath.text():
                self.settings.cacheDirPath.setText(selected_dir)
                self.markChanged()

    def clearCache(self):
        if QMessageBox.Yes == QMessageBox.warning(self.settings,
                                                  i18n("Warning"),
                                                  i18n("All the cached packages will be deleted. Are you sure? "),
                                                  QMessageBox.Yes | QMessageBox.No):
            try:
                self.iface.clearCache(0)
            except Exception, e:
                self.settings.parent.cw.exceptionCaught(str(e))

    def save(self):
        self.iface.setCacheLimit(self.settings.useCacheCheck.isChecked(), self.settings.useCacheSpin.value())
        self.iface.setConfig("directories", "cached_packages_dir", unicode(self.settings.cacheDirPath.text()))
        if self.settings.useBandwidthLimit.isChecked():
            self.iface.setConfig("general", "bandwidth_limit", str(self.settings.bandwidthSpin.value()))
        else:
            self.iface.setConfig("general", "bandwidth_limit", "0")

class RepositorySettings(SettingsTab):
    def setupUi(self):
        self.settings.repoListView.horizontalHeader().setStretchLastSection(True)
        self.settings.repoListView.verticalHeader().hide()
        self.settings.repoListView.setColumnWidth(0, 32)
        self.initialize(firstRun = True)

    def connectSignals(self):
        self.connect(self.settings.addRepoButton, SIGNAL("clicked()"), self.addRepository)
        self.connect(self.settings.removeRepoButton, SIGNAL("clicked()"), self.removeRepository)
        self.connect(self.settings.moveUpButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.settings.moveDownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.settings.repoListView, SIGNAL("itemChanged(QTableWidgetItem*)"), self.markChanged)

    def get_repo_names(self):
        repos = []
        for row in range(self.settings.repoListView.rowCount()):
            repos.append(unicode(self.settings.repoListView.item(row, 1).text()))
        return repos

    def initialize(self, firstRun = False):

        self.repositories = self.iface.getRepositories(
                repos = None if firstRun else self.get_repo_names())

        self.__clear()

        for name, address in self.repositories:
            self.__insertRow(unicode(name), address)

    def __clear(self):
        while self.settings.repoListView.rowCount():
            self.settings.repoListView.removeRow(0)

    def __insertRow(self, repoName, repoAddress):
        currentRow = self.settings.repoListView.rowCount()
        self.settings.repoListView.insertRow(currentRow)
        checkbox = QCheckBox(self.settings.repoListView)
        self.connect(checkbox, SIGNAL("toggled(bool)"), self.markChanged)
        self.settings.repoListView.setCellWidget(currentRow, 0, checkbox)
        self.settings.repoListView.cellWidget(currentRow, 0).setChecked(self.iface.isRepoActive(repoName))

        repoNameItem = QTableWidgetItem()
        repoNameItem.setText(repoName)
        repoNameItem.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.settings.repoListView.setItem(currentRow, 1, repoNameItem)

        repoAddressItem = QTableWidgetItem()
        repoAddressItem.setText(repoAddress)
        repoAddressItem.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.settings.repoListView.setItem(currentRow, 2, repoAddressItem)

    def addRepository(self):
        self.repoDialog = repodialog.RepoDialog()
        self.connect(self.repoDialog.buttonBox, SIGNAL("accepted()"), self.__addRepository)
        self.repoDialog.show()

    def __addRepository(self):
        repoName = self.repoDialog.repoName.text()
        repoAddress = self.repoDialog.repoAddress.currentText()
        if not re.match("^[0-9%s\-\\_\\.\s]*$" % str(pmutils.letters()), str(repoName)) or str(repoName) == '':
            QMessageBox.warning(self.settings,
                                i18n("Pisi Error"),
                                i18n("Not a valid repository name"))
            return
        if not repoAddress.endsWith("xml") and not repoAddress.endsWith("xml.bz2") and not repoAddress.endsWith('xz'):
            QMessageBox.warning(self.settings,
                                i18n("Pisi Error"),
                                i18n('<qt>Repository address should end with xml or xml.bz2 or xz suffix.<p>Please try again.</qt>'))
            return
        self.__insertRow(repoName, repoAddress)
        self.markChanged()

    def removeRepository(self):
        self.settings.repoListView.removeRow(self.settings.repoListView.currentRow())
        self.markChanged()

    def __setRow(self, row, rowItems):
        for col in range(self.settings.repoListView.columnCount()):
            self.settings.repoListView.setItem(row, col, rowItems[col])

    def __takeRow(self, row):
        rowItems = []
        for col in range(self.settings.repoListView.columnCount()):
            rowItems.append(self.settings.repoListView.takeItem(row, col))
        return rowItems

    def __move(self, up):
        srcRow = self.settings.repoListView.currentRow()
        dstRow = srcRow - 1 if up else srcRow + 1
        if dstRow < 0 or dstRow >= self.settings.repoListView.rowCount():
            return

        srcRowChecked = self.settings.repoListView.cellWidget(srcRow, 0).checkState()
        dstRowChecked = self.settings.repoListView.cellWidget(dstRow, 0).checkState()
        srcItems = self.__takeRow(srcRow)
        destItems = self.__takeRow(dstRow)

        self.__setRow(srcRow, destItems)
        self.__setRow(dstRow, srcItems)
        self.settings.repoListView.cellWidget(srcRow, 0).setCheckState(dstRowChecked)
        self.settings.repoListView.cellWidget(dstRow, 0).setCheckState(srcRowChecked)

        self.settings.repoListView.setCurrentItem(srcItems[1])
        self.markChanged()

    def moveUp(self):
        self.__move(True)

    def moveDown(self):
        self.__move(False)

    def getRepo(self, row):
        active = self.settings.repoListView.cellWidget(row, 0).checkState() == Qt.Checked
        name  = self.settings.repoListView.item(row, 1).text()
        address  = self.settings.repoListView.item(row, 2).text()
        return (str(name), str(address), active)

    def save(self):
        repos = []
        activities = {}
        for row in range(self.settings.repoListView.rowCount()):
            name, address, active = self.getRepo(row)
            repos.append((name, address))
            activities[name]=active
        self.iface.setRepositories(repos)
        self.iface.setRepoActivities(activities)
        self.iface.updateRepositories(self.get_repo_names())

class ProxySettings(SettingsTab):
    def setupUi(self):
        self.initialize()

    def initialize(self):
        self.settings.useProxy.setChecked(False)
        self.settings.useDe.hide()
        self.clear()

        proxyInUse = False
        config = self.iface.getConfig()

        https = config.get("general", "https_proxy")
        if https and https != "None":
            items = parse_proxy(https)
            self.settings.httpsProxy.setText(items['host'])
            self.settings.httpsProxyPort.setValue(int(items['port']))
            proxyInUse = True

        ftp = config.get("general", "ftp_proxy")
        if ftp and ftp != "None":
            items = parse_proxy(ftp)
            self.settings.ftpProxy.setText(items['host'])
            self.settings.ftpProxyPort.setValue(int(items['port']))
            proxyInUse = True

        http = config.get("general", "http_proxy")
        if http and http != "None":
            items = parse_proxy(http)
            self.settings.httpProxy.setText(items['host'])
            self.settings.httpProxyPort.setValue(int(items['port']))
            proxyInUse = True

        if proxyInUse:
            self.settings.useProxy.setChecked(True)
            if items['domain']:
                self.settings.domainProxy.setText(items['domain'])
            if items['user']:
                self.settings.userProxy.setText(items['user'])
            if items['pass']:
                self.settings.passwordProxy.setText(items['pass'])

    def connectSignals(self):
        self.connect(self.settings.useHttpForAll, SIGNAL("linkActivated(const QString&)"), self.useHttpForAll)
        self.connect(self.settings.httpProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.httpProxyPort, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.httpsProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.httpsProxyPort, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.ftpProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.ftpProxyPort, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.userProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.passwordProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.domainProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.useProxy, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useProxy, SIGNAL("toggled(bool)"), self.checkDeSettings)
        self.connect(self.settings.useDe, SIGNAL("linkActivated(const QString&)"), self.getSettingsFromDe)

    def useHttpForAll(self, link):
        self.settings.httpsProxy.setText(self.settings.httpProxy.text())
        self.settings.httpsProxyPort.setValue(self.settings.httpProxyPort.value())
        self.settings.ftpProxy.setText(self.settings.httpProxy.text())
        self.settings.ftpProxyPort.setValue(self.settings.httpProxyPort.value())

    def clear(self):
        self.settings.httpProxy.setText("")
        self.settings.httpProxyPort.setValue(0)
        self.settings.userProxy.setText("")
        self.settings.passwordProxy.setText("")
        self.settings.domainProxy.setText("")
        self.settings.httpsProxy.setText("")
        self.settings.httpsProxyPort.setValue(0)
        self.settings.ftpProxy.setText("")
        self.settings.ftpProxyPort.setValue(0)

    def checkDeSettings(self, toggled):
        self.settings.useDe.setVisible(self.getSettingsFromDe(just_check = True) and toggled)

    def getSettingsFromDe(self, link = '', just_check = False):
        cf = path.join(Pds.config_path, 'share/config/kioslaverc')
        config = Pds.parse(cf, force=True)
        proxyType = config.value('Proxy Settings/ProxyType').toString()
        if proxyType:
            if int(proxyType) > 0:
                if just_check:
                    return True

                items = parse_proxy(config.value('Proxy Settings/httpProxy').toString())
                self.settings.httpProxy.setText(items['host'])
                self.settings.httpProxyPort.setValue(int(items['port']))

                items = parse_proxy(config.value('Proxy Settings/httpsProxy').toString())
                self.settings.httpsProxy.setText(items['host'])
                self.settings.httpsProxyPort.setValue(int(items['port']))

                items = parse_proxy(config.value('Proxy Settings/ftpProxy').toString())
                self.settings.ftpProxy.setText(items['host'])
                self.settings.ftpProxyPort.setValue(int(items['port']))

                return True

        return False

    def save(self):
        httpProxy, httpProxyPort = self.settings.httpProxy.text().split('://')[-1], self.settings.httpProxyPort.value()
        httpsProxy, httpsProxyPort = self.settings.httpsProxy.text().split('://')[-1], self.settings.httpsProxyPort.value()
        ftpProxy, ftpProxyPort = self.settings.ftpProxy.text().split('://')[-1], self.settings.ftpProxyPort.value()

        userProxy = self.settings.userProxy.text()
        passProxy = self.settings.passwordProxy.text()
        domainProxy = self.settings.domainProxy.text()

        if not self.settings.useProxy.isChecked():
            httpProxy = httpsProxy = ftpProxy = None
            self.clear()

        if userProxy and passProxy:
            auth = '%s:%s@' % (userProxy, passProxy)
            if domainProxy:
                auth = '%s\%s:%s@' % (domainProxy, userProxy, passProxy)
        else:
            auth = ''

        self.iface.setConfig("general", "http_proxy",  "None" if not httpProxy  else "http://%s%s:%s"  % (auth, httpProxy,  httpProxyPort))
        self.iface.setConfig("general", "https_proxy", "None" if not httpsProxy else "https://%s%s:%s" % (auth, httpsProxy, httpsProxyPort))
        self.iface.setConfig("general", "ftp_proxy",   "None" if not ftpProxy   else "ftp://%s%s:%s"   % (auth, ftpProxy,   ftpProxyPort))

class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connectSignals()
        self.parent = parent

        self.generalSettings = GeneralSettings(self)
        self.cacheSettings = CacheSettings(self)
        self.repositorySettings = RepositorySettings(self)
        self.proxySettings = ProxySettings(self)

    def connectSignals(self):
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), self.cancelSettings)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.showHelp)

    def cancelSettings(self):
        for tab in (self.generalSettings, self.cacheSettings, \
                self.repositorySettings, self.proxySettings):
            tab.initialize()
        self.reject()

    def saveSettings(self):
        for settings in [self.generalSettings, self.cacheSettings, self.repositorySettings, self.proxySettings]:
            try:
                if settings.changed:
                    settings.save()
            except Exception, e:
                self.parent.cw.exceptionCaught(str(e))
            finally:
                if settings.changed:
                    settings.initialize()
                settings.changed = False
        self.config = config.PMConfig()

    def showHelp(self):
        helpDialog = helpdialog.HelpDialog(self, helpdialog.PREFERENCES)
        helpDialog.show()

