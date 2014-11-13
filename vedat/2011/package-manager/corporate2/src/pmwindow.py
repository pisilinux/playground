#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
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

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import *

from statemanager import StateManager
from operationmanager import OperationManager

from pmutils import *

from ui_pminstall import Ui_PmWindow
from summarydialog import SummaryDialog
from progressdialog import ProgressDialog

from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagedelegate import PackageDelegate

class PmWindow(QDialog, PM, Ui_PmWindow):

    def __init__(self, app = None, packages = [], hide_summary = False):
        QDialog.__init__(self, None)
        self.setupUi(self)

        self.hide_summary = hide_summary
        self.state = StateManager(self)
        self.iface = self.state.iface
        self.state._selected_packages = packages
        self._packages = packages[:]
        self._started = False

        self._postexceptions = [lambda: sys.exit(1)]

        # Check if another pisi instance already running
        if isPisiRunning():
            self.exceptionCaught("ALREADY RUNNING", block = True)

        # Check given package names available in repositories
        if not any(package.endswith('.pisi') for package in packages):
            available_packages = self.state.packages()
            for package in packages:
                if package not in available_packages:
                    self.exceptionCaught('HTTP Error 404', package, block = True)

        # Check if local/remote packages mixed with repo packages
        # which pisi does not support to handle these at the same time
        else:
            if not all(package.endswith('.pisi') for package in packages):
                self.exceptionCaught('MIXING PACKAGES', block = True)

            # Check given local packages if exists
            for package in get_real_paths(packages):
                if '://' not in package and package.endswith('.pisi'):
                    if not os.path.exists(package):
                        self.exceptionCaught('FILE NOT EXISTS', package, block = True)

        self.state.state = StateManager.INSTALL

        # Get a list of package names from given args.
        # It may include a path to local package, a path to remote package
        # or just a package name; following crypted code will remove
        # remote paths, appends package name as is and uses the pisi.api
        # to get package name from given local package path.
        #
        # Example:
        # input : ['/tmp/ax-2.3-1.pisi', 'http://pardus.org.tr/tt-2.3.pisi', 'yali']
        # output: ['ax', 'yali']
        _pkgs = map(lambda x: pisi.api.info_file(x)[0].package.name \
                        if x.endswith('.pisi') \
                        else x, filter(lambda x: '://' not in x,
                                        get_real_paths(self.state._selected_packages)))

        _pkgs = filter(lambda x: self.iface.pdb.has_package(x), _pkgs)

        extras = self.state.iface.getExtras(_pkgs, self.state.state)
        if extras:
            self.state._selected_packages.extend(extras)

        self.model = PackageModel(self)
        self.model.setCheckable(False)

        proxy = PackageProxy(self)
        proxy.setSourceModel(self.model)

        self.packageList.setModel(proxy)
        self.packageList.setPackages(packages)
        self.packageList.selectAll(packages)
        self.packageList.setItemDelegate(PackageDelegate(self, self, showDetailsButton=False))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.hideSelectAll()

        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state, self)
        self.summaryDialog = SummaryDialog()

        self.connectOperationSignals()

        self.button_install.clicked.connect(self.installPackages)
        self.button_install.setIcon(KIcon(("list-add", "add")))

        self.button_cancel.clicked.connect(self.actionCancelled)
        self.button_cancel.setIcon(KIcon("cancel"))

        self.rejected.connect(self.actionCancelled)

    def reject(self):
        if self.iface.operationInProgress() and self._started:
            return
        QDialog.reject(self)

    def installPackages(self):
        reinstall = False
        answer = True
        self.button_install.setEnabled(False)
        actions = self.state.checkInstallActions(self.model.selectedPackages())
        if actions:
            answer = askForActions(actions,
                   i18n("Selected packages are already installed.<br>"
                        "If you continue, the packages will be reinstalled"),
                   i18n("Already Installed Packages"),
                   i18n("Installed Packages"))

        if not answer:
            self.button_install.setEnabled(True)
            return

        if actions:
            reinstall = True

        connection_required = True
        if isAllLocal(self.model.selectedPackages()):
            connection_required = False

        operation = self.state.operationAction(self._packages,
                                               reinstall = reinstall,
                                               silence = True,
                                               connection_required = connection_required)
        self._started = True
        if operation == False:
            sys.exit(1)

    def actionStarted(self, operation):
        totalPackages = len(self.state._selected_packages)

        self.progressDialog.reset()
        if not operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.operation.setTotalPackages(totalPackages)
            self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())

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

        if operation == "System.Manager.installPackage" and not self.hide_summary:
            self.summaryDialog.setDesktopFiles(self.operation.desktopFiles)
            self.summaryDialog.showSummary()
            self.hide()

        if not self.summaryDialog.hasApplication():
            # Package install succesfull return value is 0
            QTimer.singleShot(10, lambda: sys.exit(0))

    def actionCancelled(self):
        # Package install failed with user cancel, return value is 3
        sys.exit(3)

