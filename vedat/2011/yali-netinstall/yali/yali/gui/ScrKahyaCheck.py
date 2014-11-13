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

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL

import yali.context as ctx
from yali.kahya import kahya
from yali.gui import ScreenWidget, GUIError
from yali.gui.Ui.kickerwidget import Ui_KickerWidget
from yali.gui.YaliDialog import Dialog

def loadFile(path):
    """Read contents of a file"""
    return file(path).read()

def get_kernel_opt(cmdopt):
    cmdline = loadFile("/proc/cmdline").split()
    for cmd in cmdline:
        pos = len(cmdopt)
        if cmd == cmdopt:
            return cmd
        if cmd.startswith(cmdopt) and cmd[pos] == '=':
            return cmd[pos+1:]
    return ''

class Widget(QWidget, ScreenWidget):
    name = "kahya"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_KickerWidget()
        self.ui.setupUi(self)

    def shown(self):
        ctx.mainScreen.slotNext()

    def execute(self):
        if not ctx.flags.kahya:
            ctx.logger.debug("There is no kahya jumps to the next screen.")
            return True

        ctx.autoInstall = True
        yaliKahya = kahya()
        ctx.logger.debug("Kahya File : %s " % ctx.flags.kahyaFile)


        if ctx.flags.kahya:
            ctx.logger.debug("KAHYA-PARAMS:: %s" % kahyaOpt)
            kahyaFile = kahyaOpt.split(',')[1]
            if kahyaFile == "":
                kahyaFile = ctx.consts.default_kahya_file
        elif ctx.options.useKahya:
            kahyaFile = ctx.consts.default_kahya_file
        else:
            kahyaFile = ctx.options.kahyaFile

        if kahyaFile:
            ctx.logger.debug("Reading kahya from file %s" % kahyaFile)
            yaliKahya.readData(kahyaFile)
            if yaliKahya.checkFileValidity()==True:
                ctx.logger.debug("File is ok")

                # find usable storage devices
                # initialize all storage devices
                if not yali.storage.initDevices():
                    raise GUIError, _("No storage device found.")

                devices = []
                for dev in yali.storage.devices:
                    if dev.getTotalMB() >= ctx.consts.min_root_size:
                        devices.append(dev)

                correctData = yaliKahya.getValues()

                # set keymap
                ctx.yali.setKeymap(correctData.keyData)

                # single types
                ctx.installData.isKahyaUsed = True
                ctx.installData.keyData = correctData.keyData
                ctx.installData.rootPassword = correctData.rootPassword
                ctx.installData.hostName = correctData.hostname
                ctx.installData.autoLoginUser = correctData.autoLoginUser
                yali.storage.setOrderedDiskList()
                ctx.installData.autoPartDev = devices[int(correctData.partitioning[0].disk[-1])]
                ctx.installData.autoPartMethod = {"auto":methodEraseAll,"smartAuto":methodUseAvail}[correctData.partitioningType]
                if ctx.installData.autoPartMethod == methodUseAvail:
                    ctx.installData.autoPartPartition = ctx.yali.getResizableFirstPartition()
                ctx.installData.useYaliFirstBoot = correctData.useYaliFirstBoot
                ctx.installData.timezone = correctData.timezone

                # if exists use different source repo
                ctx.installData.repoAddr = correctData.repoAddr
                ctx.installData.repoName = correctData.repoName

                ctx.logger.debug("HOSTNAME : %s " % ctx.installData.hostName)
                ctx.logger.debug("KEYDATA  : %s " % ctx.installData.keyData["xkblayout"])

                if ctx.installData.repoAddr:
                    ctx.logger.debug("REPOADDR : %s " % ctx.installData.repoAddr)
                    ctx.logger.debug("REPONAME : %s " % ctx.installData.repoName)

                # multi types
                for user in correctData.users:
                    ctx.installData.users.append(user)
                    yali.users.PENDING_USERS.append(user)
                    ctx.logger.debug("USER    : %s " % user.username)

                if ctx.options.dryRun == True:
                    ctx.logger.debug("dryRun activated Yali stopped")
                else:
                    # Summary Screen is 10
                    ctx.mainScreen.setCurrent(10)
            else:
                ctx.logger.debug("This kahya file is not correct !!")
                wrongData = yaliKahya.getValues()
                ctx.logger.debug("".join(wrongData))


