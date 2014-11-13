#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Python
import os

# PyQtNo protocol specified

from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore
from PyKDE4.kdecore import i18n

# UI
from usermanager.ui_edituser import Ui_EditUserWidget
from usermanager.ui_editgroup import Ui_EditGroupWidget

# Utilities
from usermanager.utility import nickGuess

# PolicyKit
import polkit

class PolicyItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, text, action_id):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.action_id = action_id
        self.type = 0
        self.setText(0, text)
        self.setIcon(0, kdeui.KIcon("security-medium"))

    def getAction(self):
        return self.action_id

    def setType(self, type_):
        self.type = type_
        if type_ == -1:
            self.setIcon(0, kdeui.KIcon("security-low"))
        elif type_ == 0:
            self.setIcon(0, kdeui.KIcon("security-medium"))
        elif type_ == 1:
            self.setIcon(0, kdeui.KIcon("security-high"))

    def getType(self):
        return self.type


class EditUserWidget(QtGui.QWidget, Ui_EditUserWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # List of unavailable nicks
        self.nicklist = []

        # Remove duplicate shells
        self.comboShell.setDuplicatesEnabled(False)

        # Build policy list
        self.buildPolicies()

        # Warning icon
        self.labelSign.setPixmap(kdeui.KIcon("process-stop").pixmap(32, 32))
        self.labelSign.hide(
                )
        # Disables buttons before selecting any object
        self.authGroup.setDisabled(True)
        self.pushAuth.setDisabled(True)

        # Signals
        self.connect(self.checkAutoId, QtCore.SIGNAL("stateChanged(int)"), self.slotCheckAuto)
        self.connect(self.lineUsername, QtCore.SIGNAL("textEdited(const QString&)"), self.slotUsernameChanged)
        self.connect(self.lineFullname, QtCore.SIGNAL("textEdited(const QString&)"), self.slotFullnameChanged)
        self.connect(self.listGroups, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.slotGroupSelected)
        self.connect(self.treeAuthorizations, QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)"), self.slotPolicySelected)
        self.connect(self.radioAuthNo, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.radioAuthDefault, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.radioAuthYes, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.checkAdmin, QtCore.SIGNAL("stateChanged(int)"), self.slotAdmin)
        self.connect(self.pushAuth, QtCore.SIGNAL("clicked()"), self.slotAuth)

        self.connect(self.lineFullname, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.linePassword, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.linePasswordAgain, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.lineUsername, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.lineHomeDir, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)

        self.filterAuthorizations.setTreeWidget(self.treeAuthorizations)
        self.filterGroups.setListWidget(self.listGroups)

        self.advancedGroup.hide()
        self.available_shells = []
        self._new = False


    def reset(self):
        self.wrn = ""
        self.setId(-1)
        self.setUsername("")
        self.setFullname("")
        self.setHomeDir("")
        self.setPassword()
        self.lineUsername.setEnabled(True)
        self.lineHomeDir.setEnabled(True)
        self.pushAdvanced.setChecked(False)
        self.labelWarning.setText("")
        self.labelSign.hide()
        self.advancedGroup.hide()
        self.comboShell.clear()
        self.comboShell.addItems(self.available_shells)
        self.emit(QtCore.SIGNAL("buttonStatusChanged(int)"),1)
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            self.treeAuthorizations.collapseItem(self.treeAuthorizations.topLevelItem(index))

    def buildPolicies(self):
        self.actionItems = {}
        self._vendors = []

        categories = {"tr.org.pardus.comar.user.manager": (i18n("User/group operations"), "system-users"),
                      "tr.org.pardus.comar.system.manager|org.kde.fontinst": (i18n("Package operations"), "applications-other"),
                      "tr.org.pardus.comar.system.service": (i18n("Service operations"), "services"),
                      "tr.org.pardus.comar.time|org.kde.kcontrol.kcmclock": (i18n("Date/time operations"), "clock"),
                      "tr.org.pardus.comar.boot.modules|org.kde.ksysguard": (i18n("Kernel/Process operations"), "utilities-terminal"),
                      "tr.org.pardus.comar.boot.loader": (i18n("Bootloader settings"), "media-floppy"),
                      "org.kde.kcontrol.kcmpanda": (i18n("Screen settings"), "video-display"),
                      "org.kde.kcontrol.kcmlocale": (i18n("Locale settings"), "preferences-desktop-locale"),
                      "tr.org.pardus.comar.net.filter|tr.org.pardus.comar.net.share|org.freedesktop.network-manager-settings|org.freedesktop.NetworkManager": (i18n("Network settings"), "networkmanager"),
                      "org.kde.kcontrol.kcmkdm": (i18n("Login Manager settings"), "preferences-system-login"),
                      "org.kde.kcontrol.kcmkeyboard": (i18n("Keyboard settings"), "input-keyboard")}

        # do not show policies require policy type yes or no, only the ones require auth_* type
        allActions = filter(lambda x: polkit.action_info(x)['policy_active'].startswith("auth_"),polkit.action_list())
        for _category in categories.keys():
            parent_item = QtGui.QTreeWidgetItem(self.treeAuthorizations)
            parent_item.setIcon(0, kdeui.KIcon(categories[_category][1]))
            parent_item.setText(0, unicode(categories[_category][0]))
            for category in _category.split('|'):
                catactions = filter(lambda x: x.startswith(category), allActions)
                for action_id in catactions:
                    info = polkit.action_info(action_id)
                    item = PolicyItem(parent_item, unicode(info["description"]), action_id)
                    self.actionItems[action_id] = item

    def getAuthorizations(self):
        grant = []
        revoke = []
        block = []
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            tl_item = self.treeAuthorizations.topLevelItem(index)
            for child_index in xrange(tl_item.childCount()):
                item = tl_item.child(child_index)
                if item.getType() == -1:
                    block.append(item.getAction())
                elif item.getType() == 0:
                    revoke.append(item.getAction())
                elif item.getType() == 1:
                    grant.append(item.getAction())

        return grant, revoke, block

    def isNew(self):
        return self._new

    def getId(self):
        if self.checkAutoId.isChecked():
            return int(-1)
        return int(self.spinId.value())

    def setId(self, id):
        if id != -1:
            self.checkAutoId.setCheckState(QtCore.Qt.Unchecked)
            self.checkAutoId.hide()
            self.spinId.setEnabled(False)
        else:
            self.checkAutoId.setCheckState(QtCore.Qt.Checked)
            self.checkAutoId.show()
            self.spinId.setEnabled(False)
        self.spinId.setValue(id)

    def setNickList(self, nicklist):
        self.nicklist = nicklist

    def getUsername(self):
        return unicode(self.lineUsername.text())

    def setUsername(self, username):
        self.lineUsername.setText(unicode(username))
        self.lineUsername.setEnabled(False)

    def getFullname(self):
        return unicode(self.lineFullname.text())

    def setFullname(self, fullname):
        self.lineFullname.setText(unicode(fullname))

    def setHomeDir(self, homedir):
        self.lineHomeDir.setText(unicode(homedir))
        self.lineHomeDir.setEnabled(False)

    def getHomeDir(self):
        return unicode(self.lineHomeDir.text())

    def setShell(self, shell):
        shell_index = self.comboShell.findText(shell)
        if shell_index >= 0:
            self.comboShell.setCurrentIndex(shell_index)
        else:
            self.comboShell.insertItem(0, shell)
            self.comboShell.setCurrentIndex(0)

    def getShell(self):
        return str(self.comboShell.currentText())

    def setPassword(self):
        self.linePassword.setText("")
        self.linePasswordAgain.setText("")

    def getPassword(self):
        if self.linePassword.isModified() and self.linePassword.text() == self.linePasswordAgain.text():
            return unicode(self.linePassword.text())
        return ""

    def setGroups(self, all_groups, selected_groups):
        self.listGroups.clear()
        self.comboMainGroup.clear()
        for group in all_groups:
            # Groups

            item = QtGui.QListWidgetItem(self.listGroups)
            item.setText(group)
            if group in selected_groups:
                item.setCheckState(QtCore.Qt.Checked)
                # Add selected items to mhttp://svn.pardus.org.tr/uludag/trunk/playground/intern/2011/ain group combo
                self.comboMainGroup.addItem(group)
                # Wheel group?
                if group == "wheel":
                    self.checkAdmin.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        # Select main group
        if selected_groups:
            self.comboMainGroup.setCurrentIndex(self.comboMainGroup.findText(selected_groups[0]))

    def getGroups(self):
        groups = []
        for index in range(self.listGroups.count()):
            item = self.listGroups.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                groups.append(unicode(item.text()))
        # Main group
        main_group = unicode(self.comboMainGroup.currentText())
        groups.remove(main_group)
        groups.insert(0, main_group)
        return groups

    def setAuthorizations(self, authorizations):
        for action_id in self.actionItems:
            item = self.actionItems[action_id]
            item.setType(0)
        # print "\n Authorizations: %s " %authorizations
        for action_id, scope, description, policy_active, negative in authorizations:
            if action_id in self.actionItems:
                item = self.actionItems[action_id]
                if scope == negative:
                    item.setType(1)
                elif scope == polkit.SCOPE_ALWAYS:
                    item.setType(-1)
        self.slotPolicySelected(self.treeAuthorizations.currentItem())

    def slotCheckAuto(self, state):
        if state == QtCore.Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)

    def slotAuth(self):
        if self.radioAuthNo.isChecked():
            type_ = -1
        elif self.radioAuthDefault.isChecked():
            type_ = 0
        elif self.radioAuthYes.isChecked():
            type_ = 1
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            tl_item = self.treeAuthorizations.topLevelItem(index)
            for child_index in xrange(tl_item.childCount()):
                item = tl_item.child(child_index)
                item.setType(type_)

    def slotCategoryAuth(self):
        if self.radioAuthNo.isChecked():
            type_ = -1
        elif self.radioAuthDefault.isChecked():
            type_ = 0
        elif self.radioAuthYes.isChecked():
            type_ = 1
        else:
            # If the radio buttons are all unchecked it raises an UnboundLocalError
            # to avoid that i assigned type_ to None
            type_ = None
        category = self.treeAuthorizations.currentItem()
        index = self.treeAuthorizations.indexOfTopLevelItem(category)
        tl_item = self.treeAuthorizations.topLevelItem(index)
        # Iterates the selected category using category index which found above
        for child_index in xrange(tl_item.childCount()):
            item = tl_item.child(child_index)
            item.setType(type_)

    def slotFullnameChanged(self, name):
        if self.lineUsername.isEnabled() and not self.lineUsername.isModified():
            self.lineUsername.setText(nickGuess(name, self.nicklist))
            if self.lineHomeDir.isEnabled() and not self.lineHomeDir.isModified():
                self.lineHomeDir.setText("/home/%s" % self.lineUsername.text())

    def slotUsernameChanged(self, name):
        if self.lineHomeDir.isEnabled() and not self.lineHomeDir.isModified():
            self.lineHomeDir.setText("/home/%s" % self.lineUsername.text())

    def checkLastItem(self):
        if self.comboMainGroup.count() == 1:
            kdeui.KMessageBox.error(self, i18n("There has to be at least one group selected."))
            return False
        return True

    def slotGroupSelected(self):
        item = self.listGroups.currentItem()
        if item.checkState() == QtCore.Qt.Unchecked:
            # You can't remove last item
            if not self.checkLastItem():
                item.setCheckState(QtCore.Qt.Checked)
                return
            # Remove from main group combo
            index = self.comboMainGroup.findText(item.text())
            self.comboMainGroup.removeItem(index)
            # Wheel group?
            if item.text() == "wheel":
                self.checkAdmin.setCheckState(QtCore.Qt.Unchecked)
        else:
            # Add to main group combo
            self.comboMainGroup.addItem(item.text())
            # Wheel group?
            if item.text() == "wheel":
                self.checkAdmin.setCheckState(QtCore.Qt.Checked)

    def slotPolicySelected(self, item, previous = None):
        if not item:
            return
        self.authGroup.setEnabled(True)
        self.pushAuth.setEnabled(True)
        # If selected item is a parent (category) unchecks all radio buttons
        # because a parent has no idea of its childs status
        try:
            if hasattr(item, "setType"):
                #İf selected item is a child
                self.radioAuthNo.setChecked(item.getType() == -1)
                self.radioAuthDefault.setChecked(item.getType() == 0)
                self.radioAuthYes.setChecked(item.getType() == 1)
                self.radioAuthNo.setAutoExclusive(True)
                self.radioAuthDefault.setAutoExclusive(True)
                self.radioAuthYes.setAutoExclusive(True)
            else:
                #if selected item is a parent
                tmp = self.checkChilds()
                if not tmp:
                    self.radioAuthNo.setAutoExclusive(False)
                    self.radioAuthDefault.setAutoExclusive(False)
                    self.radioAuthYes.setAutoExclusive(False)
                    self.radioAuthNo.setChecked(False)
                    self.radioAuthDefault.setChecked(False)
                    self.radioAuthYes.setChecked(False)
                else:
                    self.radioAuthNo.setChecked(self.check == -1)
                    self.radioAuthDefault.setChecked(self.check  == 0)
                    self.radioAuthYes.setChecked(self.check  == 1)
                    self.radioAuthNo.setAutoExclusive(True)
                    self.radioAuthDefault.setAutoExclusive(True)
                    self.radioAuthYes.setAutoExclusive(True)
        except:
            self.authGroup.setEnabled(False)

    def slotPolicyChanged(self, state):
        item = self.treeAuthorizations.currentItem()
        if hasattr(item, "setType"):
            if self.radioAuthNo.isChecked():
                item.setType(-1)
            elif self.radioAuthDefault.isChecked():
                item.setType(0)
            elif self.radioAuthYes.isChecked():
                item.setType(1)
        else:
            #To avoid multiple selections
            self.radioAuthNo.setAutoExclusive(True)
            self.radioAuthDefault.setAutoExclusive(True)
            self.radioAuthYes.setAutoExclusive(True)
            self.slotCategoryAuth()

    def checkChilds(self):
        category = self.treeAuthorizations.currentItem()
        index = self.treeAuthorizations.indexOfTopLevelItem(category)
        tl_item = self.treeAuthorizations.topLevelItem(index)
        self.check=tl_item.child(0).getType()
        # Iterates the selected category using category index which found above
        for child_index in xrange(tl_item.childCount()):
            item = tl_item.child(child_index)
            tmp=item.getType()
            if tmp is not self.check:
                return False
        return True

    def slotAdmin(self, state):
        if state == QtCore.Qt.Unchecked:
            # You can't remove last item
            if not self.checkLastItem():
                self.checkAdmin.setCheckState(QtCore.Qt.Checked)
                return
            # Remove from main group combo
            self.comboMainGroup.removeItem(self.comboMainGroup.findText("wheel"))
        else:
            # Add to combo
            if self.comboMainGroup.findText("wheel") < 0:
                self.comboMainGroup.addItem("wheel")
        # Update group list
        for index in range(self.listGroups.count()):
            item = self.listGroups.item(index)
            if item.text() == "wheel":
                # Change check state
                item.setCheckState(state)
                return

    def listShells(self):
        shells = open('/etc/shells').readlines()
        for shell in shells:
            if not shell.lstrip(' ').startswith('#'):
                shell = shell.rstrip('\n')
                if os.path.exists(shell):
                    self.available_shells.append(shell)

    def checkFields(self, *args):
        err = ""
        self.wrn = ""

        if self.lineFullname.text() == "" and self.lineUsername.text() == "" and self.isNew():
            err = i18n("Start with typing this user's full name.")

        if not err and self.isNew() and self.linePassword.text() == "":
            err = i18n("You should enter a password for this user.")

        if not err:
            pw = unicode(self.linePassword.text())

            # After removing the length check from COMAR backend we need to remove these
            if pw != "" and len(pw) < 4:
                self.wrn = i18n("Password must be longer.")

            if not err:
                if len(pw) and pw == self.lineFullname.text() or pw == self.lineUsername.text():
                    err = i18n("Don't use your full name or user name as a password.")

        if not err and self.linePassword.text() != self.linePasswordAgain.text():
            err = i18n("Passwords don't match.")

        nick = self.lineUsername.text()

        if not err and nick == "":
            err = i18n("You must enter a user name.")

        if not err and self.isNew() and nick in self.nicklist:
            err = i18n("This user name is used by another user.")

        if not err:
            if len(nick) > 0 and nick[0] >= "0" and nick[0] <= "9":
                err = i18n("User name must not start with a number.")

        if err:
            self.labelWarning.setText(u"<font color=red>%s</font>" % err)
            self.labelSign.show()
            self.emit(QtCore.SIGNAL("buttonStatusChanged(int)"),0)
        else:
            self.labelWarning.setText("")
            self.labelSign.hide()
            self.emit(QtCore.SIGNAL("buttonStatusChanged(int)"),1)

class EditGroupWidget(QtGui.QWidget, Ui_EditGroupWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.connect(self.checkAutoId, QtCore.SIGNAL("stateChanged(int)"), self.slotCheckAuto)
        self.connect(self.lineGroupname, QtCore.SIGNAL("textEdited(const QString&)"), self.slotGroupnameChanged)

    def slotGroupnameChanged(self, name):
        self.emit(QtCore.SIGNAL("buttonStatusChanged(int)"),1)

    def reset(self):
        self.setId(-1)
        self.setGroupname("")

    def getId(self):
        if self.checkAutoId.checkState() == QtCore.Qt.Checked:
            return -1
        return int(self.spinId.value())

    def setId(self, id):
        if id != -1:
            self.checkAutoId.setCheckState(QtCore.Qt.Unchecked)
            self.checkAutoId.hide()
            self.spinId.setEnabled(False)
        else:
            self.checkAutoId.setCheckState(QtCore.Qt.Checked)
            self.checkAutoId.show()
            self.spinId.setEnabled(False)
        self.spinId.setValue(id)

    def getGroupname(self):
        return unicode(self.lineGroupname.text())

    def setGroupname(self, groupname):
        self.lineGroupname.setText(unicode(groupname))

    def slotCheckAuto(self, state):
        if state == QtCore.Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)

#endif // EDIT.PY
