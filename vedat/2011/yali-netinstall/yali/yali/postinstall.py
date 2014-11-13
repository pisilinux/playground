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

import os
import time
import dbus
import shutil
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

import yali.util
import yali.users
import yali.pisiiface
import yali.context as ctx


class Operation:
    _id = 0
    def __init__(self, information, method):
        self._id = Operation._id
        Operation._id += 1
        self.information = information
        self.method = method
        self.status = False

    def run(self):
        if not ctx.flags.dryRun:
            ctx.logger.debug("Running postinstall : %s" % self.information)
            self.status = self.method()
        ctx.interface.informationWindow.update(self.information)
        if self.status:
            ctx.logger.debug("Operation '%s' finished sucessfully." % self.information)
        else:
            ctx.logger.debug("Operation '%s' finished with failure." % self.information)
        time.sleep(0.5)
        ctx.interface.informationWindow.hide()

def initbaselayout():
    # create /etc/hosts
    yali.util.cp("usr/share/baselayout/hosts", "etc/hosts")

    # create /etc/ld.so.conf
    yali.util.cp("usr/share/baselayout/ld.so.conf", "etc/ld.so.conf")

    # /etc/passwd, /etc/shadow, /etc/group
    yali.util.cp("usr/share/baselayout/passwd", "etc/passwd")
    yali.util.cp("usr/share/baselayout/shadow", "etc/shadow")
    os.chmod(os.path.join(ctx.consts.target_dir, "etc/shadow"), 0600)
    yali.util.cp("usr/share/baselayout/group", "etc/group")

    # create empty log file
    yali.util.touch("var/log/lastlog")

    yali.util.touch("var/run/utmp", 0664)
    yali.util.chgrp("var/run/utmp", "utmp")

    yali.util.touch("var/log/wtmp", 0664)
    yali.util.chgrp("var/log/wtmp", "utmp")

    # create needed device nodes
    os.system("/bin/mknod %s/dev/console c 5 1" % ctx.consts.target_dir)
    os.system("/bin/mknod %s/dev/null c 1 3" % ctx.consts.target_dir)
    os.system("/bin/mknod %s/dev/random c 1 8" % ctx.consts.target_dir)
    os.system("/bin/mknod %s/dev/urandom c 1 9" % ctx.consts.target_dir)

def setupTimeZone():
    if ctx.storage.storageset.active:
        yali.util.chroot("/usr/sbin/zic -l %s" % ctx.installData.timezone)
        with open(os.path.join(ctx.consts.target_dir, "etc/timezone"), "w") as timezone:
            timezone.write("%s" % ctx.installData.timezone)
        return True
    else:
        ctx.logger.debug("setTimeZone: StorageSet not activated")
        return False

def setHostName():
    if yali.util.check_link() and ctx.installData.hostName:
        ctx.logger.info("Setting hostname %s" % ctx.installData.hostName)
        ctx.link.Network.Stack["baselayout"].setHostName(unicode(ctx.installData.hostName))
        if ctx.flags.install_type == ctx.STEP_FIRST_BOOT:
            yali.util.run_batch("hostname", [unicode(ctx.installData.hostName)])
            yali.util.run_batch("update-environment")
            ctx.logger.info("Updating environment...")
        return True
    else:
        ctx.logger.debug("Setting hostname execution failed.")
        return False

def setupUsers():
    if yali.util.check_link() and yali.users.PENDING_USERS:
        for user in yali.users.PENDING_USERS:
            ctx.logger.info("User %s adding to system" % user.username)
            try:
                user_id = ctx.link.User.Manager["baselayout"].addUser(user.uid, user.username, user.realname, "", "",
                                                                      unicode(user.passwd), user.groups, [], [])
            except dbus.DBusException:
                ctx.logger.error("Adding user failed")
                return False
            else:
                ctx.logger.debug("New user's id is %s" % user_id)
                # Set no password ask for PolicyKit
                if user.no_password and ctx.link:
                    ctx.link.User.Manager["baselayout"].grantAuthorization(user_id, "*")

                # If new user id is different from old one, we need to run a huge chown for it
                user_dir = ""
                if ctx.flags.install_type == ctx.STEP_BASE or ctx.flags.install_type == ctx.STEP_DEFAULT:
                    user_dir = os.path.join(ctx.consts.target_dir, 'home', user.username)
                if ctx.flags.install_type == ctx.STEP_FIRST_BOOT:
                    user_dir = os.path.join(ctx.consts.root_dir, 'home', user.username)

                user_dir_id = os.stat(user_dir)[4]
                if not user_dir_id == user_id:
                    ctx.interface.informationWindow.update(_("Preparing home directory for %s...") % user.username)
                    yali.util.run_batch("chown", ["-R", "%d:100" % user_id, user_dir])
                    ctx.interface.informationWindow.hide()

                yali.util.run_batch("chmod", ["0711"])

                # Enable auto-login
                if user.username == ctx.installData.autoLoginUser:
                    user.setAutoLogin()

            return True

        return False

def setPassword(uid=0, password=""):
    if yali.util.check_link() and password:
        ctx.logger.info("Getting users from system")
        info = ctx.link.User.Manager["baselayout"].userInfo(uid)
        ctx.link.User.Manager["baselayout"].setUser(uid, info[1], info[3], info[4], unicode(password), info[5])
        return True
    return False

def setUserPassword():
    if yali.util.check_link() and yali.users.PENDING_USERS:
        for user in yali.users.PENDING_USERS:
            user_id = user.uid
            user_password = user.passwd
            setPassword(uid=user_id, password=user_password)
        return True
    return False

def setAdminPassword():
    return setPassword(uid=0, password=ctx.installData.rootPassword)

def setKeymapLayout():
    ctx.logger.info("Setting keymap layout")
    keymap = ctx.installData.keyData
    yali.util.setKeymap(keymap["xkblayout"], keymap["xkbvariant"], root=True)
    consolekeymap = keymap["consolekeymap"]
    if isinstance(consolekeymap, list):
        consolekeymap = consolekeymap[1]
    yali.util.writeKeymap(consolekeymap)

def setupRepoIndex():
    target = os.path.join(ctx.consts.target_dir, "var/lib/pisi/index/%s" % ctx.consts.pardus_repo_name)

    if os.path.exists(ctx.consts.pisi_index_file):
        # Copy package index
        shutil.copy(ctx.consts.pisi_index_file, target)
        shutil.copy(ctx.consts.pisi_index_file_sum, target)

        # Extract the index
        pureIndex = file(os.path.join(target,"pisi-index.xml"),"w")
        if ctx.consts.pisi_index_file.endswith("bz2"):
            import bz2
            pureIndex.write(bz2.decompress(open(ctx.consts.pisi_index_file).read()))
        else:
            import lzma
            pureIndex.write(lzma.decompress(open(ctx.consts.pisi_index_file).read()))
        pureIndex.close()

        ctx.logger.debug("pisi index files copied.")
    else:
        ctx.logger.debug("pisi index file not found!")

    ctx.logger.debug("Regenerating pisi caches.. ")
    yali.pisiiface.regenerateCaches()
    return True

def writeInitramfsConf():
    conf_path = os.path.join(ctx.consts.target_dir, "etc/initramfs.conf")
    if not os.path.exists(os.path.dirname(conf_path)):
        raise yali.Error("writeInitramfsConf can access %s path" % conf_path)

    parameters = []
    rootDevice = ctx.storage.storageset.rootDevice
    parameters.append("root=%s" % rootDevice.fstabSpec)

    swapDevices = ctx.storage.storageset.swapDevices

    if swapDevices:
        parameters.append("resume=%s" % swapDevices[0].path)

    if ctx.storage.lvs:
        parameters.append("lvm=1")

    if ctx.storage.raidArrays:
        parameters.append("raid=1")

    ctx.logger.info("Writing initramfs.conf file with %s parameters" % " ".join(parameters))

    with open(conf_path, 'w') as initramfs:
        for parameter in parameters:
            try:
                initramfs.write("%s\n" % parameter)
            except IOError, msg:
                raise yali.Error("Unexpected error: %s" % msg)

def writeFstab():
    ctx.logger.info("Generating fstab configuration file")
    if ctx.storage.storageset.active:
        ctx.storage.storageset.write(ctx.consts.target_dir)
        return True

    ctx.logger.debug("writeFstab:StorageSet not activated")
    return False

def setupFirstBoot():
    ctx.logger.info("Generating yali configuration file")
    if ctx.storage.storageset.active:
        yali.util.write_config_option(os.path.join(ctx.consts.target_dir, "etc/yali/yali.conf"), "general", "installation", "firstboot")
        return True

    ctx.logger.debug("setupFirstBoot:StorageSet not activated")
    return False

def teardownFirstBoot():
    yali.util.run_batch("pisi", ["rm", "yali", "yali-theme-pardus", "yali-branding-pardus"])

def setupPrivileges():
    # BUG:#11255 normal user doesn't mount /mnt/archive directory. 
    # We set new formatted partition priveleges as user=root group=disk and change mod as 0770
    ctx.logger.info("Setting user defined mountpoints privileges")
    if ctx.storage.storageset.active:
        default_mountpoints = ['/', '/boot', '/home', '/tmp', '/var', '/opt']
        user_defined_mountpoints = [device for mountpoint, device in ctx.storage.mountpoints.items() if mountpoint not in default_mountpoints]
        if user_defined_mountpoints:
            ctx.logger.debug("User defined mountpoints:%s" % [device.format.mountpoint for device in user_defined_mountpoints])
            for device in user_defined_mountpoints:
                yali.util.set_partition_privileges(device, 0770, 0, 6)

    ctx.logger.debug("setupPrivileges:StorageSet not activated")
    return False

def setupStorage():
    ctx.storage.storageset.mountFilesystems()
    return ctx.storage.storageset.active

def teardownStorage():
    remove = False
    if ctx.flags.install_type == ctx.STEP_FIRST_BOOT:
        remove = True
    yali.util.backup_log(remove)
    ctx.storage.storageset.umountFilesystems()
    return not ctx.storage.storageset.active

def writeBootLooder():
    ctx.logger.info("Generating grub configuration file")
    if ctx.storage.storageset.active:
        ctx.bootloader.write()
        return True

    ctx.logger.debug("writeBootLooder:StorageSet not activated")
    return False

def installBootloader():
    if len(ctx.mountCount):
        ctx.logger.debug("StorageSet is already active. Bootloader installBootloader failed")
        return False

    rc = ctx.bootloader.install()
    if rc:
        ctx.logger.debug("Bootloader installation failed")
        return False
    else:
        ctx.logger.info("Bootloader installation succesed")
        return True
