#
# Copyright (C) 2009-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
import os
import sys
import pardus.xorg

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QListWidgetItem, QIcon, QLineEdit

import yali.util
import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.rescuepasswordwidget import Ui_RescuePasswordWidget

class Widget(QWidget, ScreenWidget):
    name = "passwordRescue"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_RescuePasswordWidget()
        self.ui.setupUi(self)

        self.connect(self.ui.users, SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
                     self.refresh)
        self.connect(self.ui.password, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.confirm, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.password, SIGNAL("focusInEvent(QFocusEvent*)"),
                     self.checkCapsLock)
        self.connect(self.ui.confirm, SIGNAL("focusInEvent(QFocusEvent*)"),
                     self.checkCapsLock)
        self.connect(self.ui.resetPassword, SIGNAL("clicked()"), self.slotResetPassword)

    def refresh(self, current, previous):
        self.ui.password.clear()
        self.ui.confirm.clear()
        self.ui.resetPassword.setEnabled(False)

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
        for child in self.ui.groupBox_2.children():
            self.setCapsLockIcon(child)

    def showError(self, message):
        ctx.interface.informationWindow.update(message, type="error")
        ctx.mainScreen.disableNext()

    def slotResetPassword(self):
        user = self.ui.users.currentItem().user
        user.passwd = unicode(self.ui.password.text())
        user_exist = False
        for pending_user in yali.users.PENDING_USERS:
            if pending_user.uid == user.uid:
                pending_user = user
                break
        else:
            yali.users.PENDING_USERS.append(user)

        self.ui.resetPassword.setEnabled(False)
        ctx.mainScreen.enableNext()

    def slotTextChanged(self):
        self.ui.resetPassword.setEnabled(False)
        user = self.ui.users.currentItem().user
        username = user.username
        realname = user.realname
        password = unicode(self.ui.password.text())
        password_confirm = unicode(self.ui.confirm.text())

        if not password == '' and (password.lower() == username.lower() or
                                   password.lower() == realname.lower()):
            self.showError(_('Don\'t use your user name or name as a password'))
            return
        elif password_confirm and password_confirm != password:
            self.showError(_('Passwords do not match'))
            return
        elif len(password) == len(password_confirm) and len(password_confirm) < 4 and not password =='':
            self.showError(_('Password is too short'))
            return
        else:
            ctx.interface.informationWindow.hide()

        if password and password_confirm:
            self.ui.resetPassword.setEnabled(True)

    def fillUsers(self):
        self.ui.users.clear()
        users = yali.util.getUsers()
        for user in users:
            RescueUser(self.ui.users, user)

        if not self.ui.users.count():
            rc = ctx.interface.messageWindow(_("Cannot Rescue"),
                                             _("Your current installation cannot be rescued."),
                                             type="custom", customIcon="warning",
                                             customButtons=[_("Exit"), _("Continue")])
            if rc == 0:
                sys.exit(0)
            else:
                ctx.mainScreen.disableNext()

    def shown(self):
        ctx.mainScreen.disableBack()
        self.fillUsers()
        self.ui.resetPassword.setEnabled(False)

    def execute(self):
        return True

    def backCheck(self):
        ctx.mainScreen.step_increment += ctx.installData.rescueMode
        return True

class RescueUser(QListWidgetItem):
    def __init__(self, parent, user):
        if user.username == "root":
            icon = "root"
            name = _("Super User")
        else:
            name = user.username
            icon = "normal"

        label = "%s (%s)" % (name, user.realname)
        QListWidgetItem.__init__(self, QIcon(":/gui/pics/user_%s.png" % icon), label, parent)
        self.user = user
