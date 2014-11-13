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

import time

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from pmutils import *
from pmlogging import logger

class OperationManager(QObject):
    def __init__(self, state):
        QObject.__init__(self)
        self.nop = ["System.Manager.clearCache", "System.Manager.setCache", "System.Manager.setConfig",
                    "System.Manager.setRepoActivities", "System.Manager.setRepositories"]
        self.state = state
        self.state.setExceptionHandler(self.exceptionHandler)
        self.state.setActionHandler(self.handler)
        self.initialize()

    def initialize(self):
        self.packageNo = 0
        self.totalPackages = 0
        self.totalSize = 0
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0
        self.desktopFiles = []
        self._operation_signals = {"installing":i18n('installing'),
                                   "removing":i18n('removing'),
                                   "extracting":i18n('extracting'),
                                   "configuring":i18n('configuring')}

    def setTotalPackages(self, totalPackages):
        self.totalPackages = totalPackages

    def calculateTimeLeft(self, rate, symbol):
        factor = {"B/s":1, "KB/s":1024, "MB/s":1048576, "GB/s":1073741824}
        if symbol == "--/-":
            return "--:--:--"
        rates = float(rate) * factor[symbol.strip()]
        total = self.totalSize
        downloaded = self.totalDownloaded + self.curPkgDownloaded
        left = total - downloaded

        try:
            timeLeft = '%02d:%02d:%02d' % tuple([i for i in time.gmtime(left/rates)[3:6]])
            self.emit(SIGNAL("elapsedTime(QString)"), timeLeft)
        except ZeroDivisionError:
            pass

    def updateTotalDownloaded(self, pkgDownSize, pkgTotalSize, rate, symbol):
        symbol = symbol.replace('K', 'k')
        if rate == 0:
            self.rate = "-- kB/s"
        else:
            self.rate = "%s %s" % (rate, symbol)

        if self.totalPackages == 0:
            self.totalSize = pkgTotalSize

        if pkgDownSize == pkgTotalSize:
            self.totalDownloaded += int(pkgTotalSize)
            self.curPkgDownloaded = 0
        else:
            self.curPkgDownloaded = int(pkgDownSize)

        completed = humanReadableSize(self.totalDownloaded + self.curPkgDownloaded, ".2")
        total = humanReadableSize(self.totalSize, ".2")

        self.emit(SIGNAL("downloadInfoChanged(QString, QString, QString)"), completed, total, self.rate)

    def updateTotalOperationPercent(self):
        totalDownloaded = self.totalDownloaded + self.curPkgDownloaded
        try:
            percent = (totalDownloaded * 100) / self.totalSize
        except ZeroDivisionError:
            percent = 100

        percent = min(100, percent)
        self.emit(SIGNAL("progress(int)"), percent)

    def updatePackageProgress(self):
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("progress(int)"), percent)

    def addDesktopFile(self, desktopFile):
        if not self.state.inInstall():
            return

        places = ('usr/share/applications/',
                  'usr/kde/4/share/applications/kde4/',
                  'usr/kde/3.5/share/applications/kde/')

        for place in places:
            if desktopFile.startswith(place):
                self.desktopFiles.append(desktopFile)

    def exceptionHandler(self, exception):
        self.emit(SIGNAL("exception(QString)"), str(exception))

    def handler(self, package, signal, args):

        if signal in ["started", "finished"]:
            logger.debug("Signal: %s" % str(signal))
            logger.debug("Args: %s" % str(args))

        # FIXME: iface should just send either a status or signal
        if signal in ["status", "progress"]:
            signal = args[0]
            args = args[1:]
        ####

        if signal == "finished":
            self.state.chainAction(args[0])
            if args[0] in self.nop: # no operation
                return
            self.emit(SIGNAL("finished(QString)"), args[0])

        elif signal == "fetching":
            if not args[0].startswith("pisi-index.xml"):
                self.emit(SIGNAL("operationChanged(QString, QString)"), i18n("downloading"), args[0])
            self.updateTotalDownloaded(args[4], args[5], args[2], args[3])
            self.calculateTimeLeft(args[2], args[3])
            self.updateTotalOperationPercent()

        elif signal == "updatingrepo":
            self.emit(SIGNAL("operationChanged(QString, QString)"), signal, args[0])

        elif signal == "error":
            self.emit(SIGNAL("exception(QString)"), unicode(args[0]))

        elif signal == "started":
            if args[0] in self.nop: # no operation
                return
            self.initialize()
            self.emit(SIGNAL("started(QString)"), args[0])

        elif signal in ["installing", "removing", "extracting", "configuring"]:
            self.emit(SIGNAL("operationChanged(QString, QString)"), self._operation_signals[signal], args[0])

        if signal == "cancelled":
            self.emit(SIGNAL("operationCancelled()"))

        elif signal == "desktopfile":
            self.addDesktopFile(str(args[0]))

        elif signal == "cached":
            self.totalSize = int(args[0])

        elif signal in ["removed", "installed", "upgraded"]:
            # Bug 4030
            if not self.state.inRemove() and signal == "removed":
                return
            self.packageNo += 1
            # If the number of operated packages more than total packages just fix them
            # The issue is related to the pm-install remote package installs
            if self.packageNo > self.totalPackages:
                self.totalPackages = self.packageNo
            self.updatePackageProgress()
            self.emit(SIGNAL("packageChanged(int, int, QString)"), self.packageNo, self.totalPackages, i18n(signal))
