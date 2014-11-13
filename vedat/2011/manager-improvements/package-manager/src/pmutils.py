#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
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
import pisi
import comar
import urllib
import socket
import unicodedata
import traceback

import backend

from pmlogging import logger

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QEventLoop

from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QApplication

from PyQt4.QtNetwork import QNetworkProxy

import pds
from pds.qiconloader import QIconLoader

Pds = pds.Pds('package-manager', debug = False)
# Force to use Default Session for testing
# Pds.session = pds.DefaultDe
# print 'Current session is : %s %s' % (Pds.session.Name, Pds.session.Version)

i18n = Pds.session.i18n
KIconLoader = QIconLoader(Pds)
KIcon = KIconLoader.icon

class PM:

    def connectOperationSignals(self):
        # Basic connections
        self.connect(self.operation, SIGNAL("exception(QString)"), self.exceptionCaught)
        self.connect(self.operation, SIGNAL("finished(QString)"), self.actionFinished)
        self.connect(self.operation, SIGNAL("started(QString)"), self.actionStarted)
        self.connect(self.operation, SIGNAL("operationCancelled()"), self.actionCancelled)

        # ProgressDialog connections
        self.connect(self.operation, SIGNAL("started(QString)"), self.progressDialog.updateActionLabel)
        self.connect(self.operation, SIGNAL("progress(int)"), self.progressDialog.updateProgress)
        self.connect(self.operation, SIGNAL("operationChanged(QString,QString)"), self.progressDialog.updateOperation)
        self.connect(self.operation, SIGNAL("packageChanged(int, int, QString)"), self.progressDialog.updateStatus)
        self.connect(self.operation, SIGNAL("elapsedTime(QString)"), self.progressDialog.updateRemainingTime)
        self.connect(self.operation, SIGNAL("downloadInfoChanged(QString, QString, QString)"), self.progressDialog.updateCompletedInfo)

    def notifyFinished(self):
        if not self.operation.totalPackages:
            return
        Pds.notify(i18n('Package Manager'), self.state.getSummaryInfo(self.operation.totalPackages))

    def exceptionCaught(self, message, package = '', block = False):
        self.runPreExceptionMethods()

        if any(warning in message for warning in ('urlopen error','Socket Error', 'PYCURL ERROR')):
            errorTitle = i18n("Network Error")
            errorMessage = i18n("Please check your network connections and try again.")
        elif "Access denied" in message or "tr.org.pardus.comar.Comar.PolicyKit" in message:
            errorTitle = i18n("Authorization Error")
            errorMessage = i18n("You are not authorized for this operation.")
        elif "HTTP Error 404" in message and not package == '':
            errorTitle = i18n("Pisi Error")
            errorMessage = unicode(i18n("Package <b>%s</b> not found in repositories.<br>"\
                                        "It may be upgraded or removed from the repository.<br>"\
                                        "Please try upgrading repository informations.")) % package
        elif "MIXING PACKAGES" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Mixing file names and package names not supported yet.")
        elif "FILE NOT EXISTS" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = unicode(i18n("File <b>%s</b> doesn't exists.")) % package
        elif "ALREADY RUNNING" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Another instance of PiSi is running. Only one instance is allowed.")
        else:
            errorTitle = i18n("Pisi Error")
            errorMessage = message

        self.messageBox = QMessageBox(errorTitle, errorMessage, QMessageBox.Critical, QMessageBox.Ok, 0, 0)

        if block:
            self.messageBox.exec_()
            self.runPostExceptionMethods()
        else:
            QTimer.singleShot(0, self.messageBox.exec_)
            self.messageBox.buttonClicked.connect(self.runPostExceptionMethods)

    def runPreExceptionMethods(self):
        if hasattr(self, '_preexceptions'):
            for method in self._preexceptions:
                method()

    def runPostExceptionMethods(self, *args):
        if hasattr(self, '_postexceptions'):
            for method in self._postexceptions:
                method()

def get_real_paths(packages):
    # If packages are not from repo or remote, find their absolute paths
    return map(lambda x: x if not x.endswith('pisi') or '://' in x else os.path.abspath(x), packages)

def isAllLocal(packages):
    return all(map(lambda x: x.endswith('.pisi') and not '://' in x, packages))

def askForActions(packages, reason, title, details_title):
    msgbox = QMessageBox()
    msgbox.setText('<b>%s</b>' % reason)
    msgbox.setInformativeText(i18n("Do you want to continue ?"))
    msgbox.setDetailedText(details_title + '\n' + '-'*60 + '\n  - ' + '\n  - '.join(packages))
    msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msgbox.exec_() == QMessageBox.Yes

def waitCursor():
    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

def restoreCursor():
    # According to the Qt Documentation it should be called twice to reset 
    # cursor to the default if one use waitCursor twice.
    QApplication.restoreOverrideCursor()
    QApplication.restoreOverrideCursor()

def processEvents():
    QApplication.processEvents()

def set_proxy_settings():
    http = backend.pm.Iface().getConfig().get("general", "http_proxy")
    if http and not http == "None":
        items = parse_proxy(http)
        QNetworkProxy.setApplicationProxy(
                QNetworkProxy(QNetworkProxy.HttpProxy,
                            items['host'], int(items['port']),
                            items['user'] or '', items['pass'] or ''))

def reset_proxy_settings():
    QNetworkProxy.setApplicationProxy(QNetworkProxy())

def network_available():
    return pisi.fetcher.Fetcher('http://appinfo.pardus.org.tr').test()

def parse_proxy(line):
    settings = {'domain':None,'user':None,'pass':None,'host':None,'port':None}

    if '://' in line:
        line = line.replace('%s://' % line.split('://')[0], '', 1)

    if '\\' in line:
        settings['domain'] = line.split('\\')[0]
        line = line.replace('%s\\' % settings['domain'], '', 1)

    if '@' in line:
        auth = line.split('@')[0]
        settings['user'], settings['pass'] = auth.split(':')
        line = line.replace('%s@' % auth, '', 1)

    if ':' in line:
        settings['host'], settings['port'] = line.split(':')

    return settings

def repos_available(iface, check_repos = None):
    repos = iface.getRepositories(only_active = True, repos = check_repos)
    if not repos:
        return False

    for name, address in repos:
        if not pisi.fetcher.Fetcher('%s.sha1sum' % address).test():
            return False

    return True

def isPisiRunning():
    link = comar.Link()
    return any(operation.startswith('System.Manager') for operation in link.listRunning())

def handleException(exception, value, tb):
    """
    Exception Handler

    @param exception: exception object
    @param value: exception message
    @param tb: traceback log
    """
    logger.error("".join(traceback.format_exception(exception, value, tb)))

def humanReadableSize(size, precision=".1"):
    if not size:
        return 'N/A'

    symbols, depth = [' B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 0

    while size > 1000 and depth < 8:
        size = float(size / 1024)
        depth += 1

    if size == 0:
        return "0 B"

    fmt = "%%%sf %%s" % precision
    return fmt % (size, symbols[depth])

# Python regex sucks
# http://mail.python.org/pipermail/python-list/2009-January/523704.html
def letters():
    start = end = None
    result = []
    for index in xrange(sys.maxunicode + 1):
        c = unichr(index)
        if unicodedata.category(c)[0] == 'L':
            if start is None:
                start = end = c
            else:
                end = c
        elif start:
            if start == end:
                result.append(start)
            else:
                result.append(start + "-" + end)
            start = None
    return ''.join(result)
