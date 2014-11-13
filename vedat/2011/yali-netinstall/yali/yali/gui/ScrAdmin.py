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
import pardus.xorg
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QLineEdit, QTimer
from pds.thread import PThread
from pds.gui import PMessageBox, MIDCENTER, CURRENT, OUT

import yali.util
import yali.postinstall
import yali.storage
import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.rootpasswidget import Ui_RootPassWidget

class Widget(QWidget, ScreenWidget):
    name = "admin"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_RootPassWidget()
        self.ui.setupUi(self)
        self.intf = ctx.interface

        self.host_valid = True
        self.pass_valid = False

        if ctx.flags.install_type == ctx.STEP_DEFAULT:
            self.pthread = PThread(self, self.startInit, self.dummy)

        self.pds_messagebox = PMessageBox(self)
        self.pds_messagebox.enableOverlay()

        self.connect(self.ui.pass1, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.pass2, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.pass2, SIGNAL("returnPressed()"),
                     self.slotReturnPressed)
        self.connect(self.ui.hostname, SIGNAL("textChanged(const QString &)"),
                     self.slotHostnameChanged)

    def update(self):
        if self.host_valid and self.pass_valid:
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()

    def shown(self):
        if ctx.installData.hostName:
            self.ui.hostname.setText(str(ctx.installData.hostName))
        else:
            # Use first added user's name as machine name if its exists
            release_hostname = yali.util.product_release()
            if self.ui.hostname.text() == '':
                self.ui.hostname.setText(release_hostname)

        if ctx.installData.rootPassword:
            self.ui.pass1.setText(ctx.installData.rootPassword)
            self.ui.pass2.setText(ctx.installData.rootPassword)

        self.update()
        self.checkCapsLock()
        self.ui.pass1.setFocus()


    def dummy(self):
        pass

    def execute(self):
        ctx.installData.rootPassword = unicode(self.ui.pass1.text())
        ctx.installData.hostName = unicode(self.ui.hostname.text())

        if ctx.flags.install_type == ctx.STEP_DEFAULT:
            #FIXME:Refactor dirty code
            if ctx.storageInitialized:
                disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
                if len(disks) == 1:
                    ctx.storage.clearPartDisks = [disks[0].name]
                    ctx.mainScreen.step_increment = 2
                else:
                    ctx.mainScreen.step_increment = 1
            else:
                self.pds_messagebox.setMessage(_("Storage Devices initialising..."))
                self.pds_messagebox.animate(start=MIDCENTER, stop=MIDCENTER)
                ctx.mainScreen.step_increment = 0
                self.pthread.start()
                QTimer.singleShot(2, self.startStorageInitialize)
                return False

        return True

    def startInit(self):
        self.pds_messagebox.animate(start=MIDCENTER, stop=MIDCENTER)

    def startStorageInitialize(self):
        ctx.storageInitialized = yali.storage.initialize(ctx.storage, ctx.interface)
        self.initFinished()

    def initFinished(self):
        self.pds_messagebox.animate(start=CURRENT, stop=CURRENT, direction=OUT)
        disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
        if ctx.storageInitialized:
            if len(disks) == 1:
                ctx.storage.clearPartDisks = [disks[0].name]
                ctx.mainScreen.step_increment = 2
            else:
                ctx.mainScreen.step_increment = 1
            ctx.mainScreen.slotNext(dry_run=True)
        else:
            ctx.mainScreen.enableBack()

    def setCapsLockIcon(self, child):
        if type(child) == QLineEdit:
            if pardus.xorg.capslock.isOn():
                child.setStyleSheet("""QLineEdit {
                        background-image: url(:/gui/pics/caps.png);
                        background-repeat: no-repeat;
                        background-position: right;
                        padding-right: 35px;
                        }""")
            else:
                child.setStyleSheet("""QLineEdit {
                        background-image: none;
                        padding-right: 0px;
                        }""")

    def checkCapsLock(self):
        for child in self.ui.groupBox.children():
            self.setCapsLockIcon(child)

    def keyReleaseEvent(self, event):
        self.checkCapsLock()

    def slotTextChanged(self):

        password = str(self.ui.pass1.text())
        password_confirm = str(self.ui.pass2.text())

        if password and password == password_confirm:
            if len(password) < 4:
                self.intf.informationWindow.update(_('Password is too short.'), type="error")
                self.pass_valid = False
            else:
                self.intf.informationWindow.hide()
                self.pass_valid = True
        else:
            self.pass_valid = False
            if password_confirm:
                self.intf.informationWindow.update(_('Passwords do not match.'), type="error")

        if password.lower()=="root" or password_confirm.lower()=="root":
            self.pass_valid = False
            if password_confirm:
                self.intf.informationWindow.update(_('Do not use your username as your password.'), type="error")

        if self.pass_valid:
            self.intf.informationWindow.hide()

        self.update()

    def slotHostnameChanged(self, hostname):
        if len(hostname) > 64:
            self.host_valid = False
            self.intf.informationWindow.update(_('Hostname cannot be longer than 64 characters.'), type="error")
            self.update()
            return


        if not hostname.toAscii():
            self.host_valid = False
            self.update()
            return

        self.host_valid = yali.util.is_text_valid(hostname.toAscii())

        if not self.host_valid:
            self.intf.informationWindow.update(_('Hostname contains invalid characters.'), type="error")
        else:
            self.intf.informationWindow.hide()
        self.update()


    def slotReturnPressed(self):
        if ctx.mainScreen.isNextEnabled():
            ctx.mainScreen.slotNext()



