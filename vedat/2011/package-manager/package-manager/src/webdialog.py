#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from pds.gui import *
from pmutils import *
from pds.thread import PThread

from ui_preview import Ui_Preview
from ui_webdialog import Ui_WebDialog

from pds.qprogressindicator import QProgressIndicator

class WebDialog(PAbstractBox, Ui_WebDialog):
    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)
        self.setupUi(self)

        self.iface = parent.iface

        # PDS Settings
        self._animation = 1
        self._duration = 400
        self.enableOverlay()
        self._disable_parent_in_shown = True

        self.registerFunction(IN, lambda: parent.statusBar().hide())
        self.registerFunction(FINISHED, lambda: parent.statusBar().setVisible(not self.isVisible()))
        self._as = 'http://appinfo.pardus.org.tr'
        self.cancelButton.clicked.connect(self._hide)
        self.cancelButton.setIcon(KIcon("dialog-close"))

        # Hide Scrollbars and context menu in webview
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)

        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webView.page().linkClicked.connect(self.showFullImage)

        self.tabWidget.removeTab(0)

        self.busy = QProgressIndicator(self, "white")
        self.busy.setMaximumSize(QSize(48, 48))
        self.webLayout.addWidget(self.busy)
        self.busy.hide()

        self._filesThread = PThread(self, self.getFiles, self.getFilesFinished)
        self.filterLine.setListWidget(self.filesList)
        self.noconnection.hide()
        self.parent = parent

    def showFullImage(self, url):
        PreviewDialog(self, url)

    def showPage(self, addr):
        if network_available():
            self.webView.load(QUrl(addr))
        else:
            self._sync_template(status = False)
        self.animate(start = BOTCENTER, stop = MIDCENTER)

    def getFiles(self):
        return self.iface.getPackageFiles(str(self.packageName.text()))

    def getFilesFinished(self):
        self.filesList.addItems(self._filesThread.get())
        self.filesList.sortItems()

    def _tabSwitched(self, index):
        if index == 0 and self.tabWidget.count() > 1:
            if self.filesList.count() == 0:
                self._filesThread.start()

    def _sync_template(self, status, package = '', summary = '', description = ''):
        def _replace(key, value):
            self.webView.page().mainFrame().evaluateJavaScript(\
                    '%s.innerHTML="%s";' % (key, value))

        self.busy.hide()
        self.busy.stopAnimation()

        if status:
            _replace('title', package)
            _replace('summary', summary)
            _replace('description', description)
            self.webWidget.show()
            self.noconnection.hide()
        else:
            self.noconnection.show()
            self.webWidget.hide()

        reset_proxy_settings()

    def showPackageDetails(self, package, installed, summary='', description=''):
        self.packageName.setText(package)

        self.filesList.clear()
        self.webView.loadFinished.connect(lambda x: \
                self._sync_template(x, package, summary, description))

        if network_available():
            set_proxy_settings()
            self.webWidget.hide()
            self.busy.show()
            self.busy.startAnimation()
            self.webView.load(QUrl('%s/?p=%s' % (self._as, package)))
        else:
            self._sync_template(status = False)

        self.tabWidget.insertTab(0, self.packageFiles, i18n('Package Files'))
        self.tabWidget.currentChanged.connect(self._tabSwitched)

        if not installed:
            self.tabWidget.removeTab(0)
            self.tabWidget.currentChanged.disconnect(self._tabSwitched)

        self.animate(start = BOTCENTER, stop = MIDCENTER)

    def _hide(self):
        self.busy.stopAnimation()
        try:
            self.webView.loadFinished.disconnect()
        except:
            pass
        self.animate(start = MIDCENTER, stop = BOTCENTER, direction = OUT)

class PreviewDialog(PAbstractBox, Ui_Preview):
    def __init__(self, parent, url):
        PAbstractBox.__init__(self, parent.parent)
        self.setupUi(self)
        self.parent = parent

        # PDS Settings
        self._animation = 1
        self._duration = 400
        self.enableOverlay()
        # self._disable_parent_in_shown = True

        self.cancelButton.clicked.connect(self._hide)
        self.cancelButton.setIcon(KIcon("dialog-close"))

        # Hide Scrollbars and context menu in webview
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)

        self.busy = QProgressIndicator(self, "white")
        self.busy.setMaximumSize(QSize(48, 48))
        self.webLayout.addWidget(self.busy)
        self.busy.hide()

        self.parent._hide()
        QTimer.singleShot(0, lambda: self.showPackageScreenShot(url))

        self.setOverlayClickMethod(lambda x:self._hide())

    def showPackageScreenShot(self, url):
        if network_available():

            self.webView.loadFinished.connect(lambda x: self.webView.setVisible(x))
            self.webView.loadFinished.connect(lambda x: self.busy.setVisible(not x))
            self.webView.loadFinished.connect(lambda x: self.cancelButton.setVisible(x))

            self.registerFunction(FINISHED, lambda: self.webView.load(url))

            self.cancelButton.hide()
            self.webView.hide()
            self.busy.busy()

            self.animate(start = BOTCENTER, stop = MIDCENTER)

    def _hide(self):
        self.busy.stopAnimation()
        self.webView.loadFinished.disconnect()
        self.animate(start = MIDCENTER, stop = BOTCENTER, direction = OUT)
        self.parent.animate(start = BOTCENTER, stop = MIDCENTER)

