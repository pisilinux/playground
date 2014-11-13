#!/usr/bin/python
#
# Copyright (C) 2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import os
import grp
import shutil
import subprocess
import string
import stat
import errno
import time
import dbus
import ConfigParser
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

import comar
import pisi
import piksemel
import yali
import yali.sysutils
import yali.localedata
import yali.context as ctx
from pardus import diskutils, grubutils

EARLY_SWAP_RAM = 512 * 1024 # 512 MB

def cp(source, destination):
    source = os.path.join(ctx.consts.target_dir, source)
    destination = os.path.join(ctx.consts.target_dir, destination)
    ctx.logger.info("Copying from '%s' to '%s'" % (source, destination))
    shutil.copyfile(source, destination)

def touch(path, mode=0644):
    f = os.path.join(ctx.consts.target_dir, path)
    open(f, "w", mode).close()

def chgrp(path, group):
    f = os.path.join(ctx.consts.target_dir, path)
    gid = int(grp.getgrnam(group)[2])
    os.chown(f, 0, gid)

def product_name(path=None):
    if not path:
        path = ctx.consts.root_dir
    filename = os.path.join(path, ctx.consts.pardus_release_file)
    release_str = ""
    if os.access(filename, os.R_OK):
        with open(filename) as release_file:
            try:
                release_str = release_file.readline().strip()
            except (IOError, AttributeError):
                pass
    return release_str

def produc_id():
    release = product_name().split()
    return release[1].lower()

def product_release():
    release = product_name().split()
    return "".join(release[:2]).lower()

def is_text_valid(text):
    allowed_chars = string.ascii_letters + string.digits + '.' + '_' + '-'
    return len(text) == len(filter(lambda u: [x for x in allowed_chars if x == u], text))

def numeric_type(num):
    """ Verify that a value is given as a numeric data type.

        Return the number if the type is sensible or raise ValueError
        if not.
    """
    if num is None:
        num = 0
    elif not (isinstance(num, int) or \
              isinstance(num, long) or \
              isinstance(num, float)):
        raise ValueError("value (%s) must be either a number or None" % num)

    return num

def insert_colons(a_string):
    """
    Insert colon between every second character.

    E.g. creates 'al:go:ri:th:ms' from 'algoritms'. Useful for formatting MAC
    addresses and wwids for output.
    """
    suffix = a_string[-2:]
    if len(a_string) > 2:
        return insert_colons(a_string[:-2]) + ':' + suffix
    else:
        return suffix

def get_edd_dict(devices):
    eddDevices = {}

    if not os.path.exists("/sys/firmware/edd"):
        rc = run_batch("modprobe", ["edd"])[0]
        if rc > 0:
            ctx.logger.error("Inserting EDD Module failed !")
            return eddDevices

    edd = diskutils.EDD()
    edds = edd.list_edd_signatures()
    mbrs = edd.list_mbr_signatures()

    for number, signature in edds.items():
        if mbrs.has_key(signature):
            if mbrs[signature] in devices:
                eddDevices[os.path.basename(mbrs[signature])] = number
    return eddDevices

def run_batch(cmd, argv=[]):
    """Run command and report return value and output."""
    ctx.logger.info('Running %s' % "".join(cmd))
    env = os.environ.copy()
    env.update({"LC_ALL": "C"})
    cmd = "%s %s" % (cmd, ' '.join(argv))
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    out, error = p.communicate()
    ctx.logger.info('return value for "%(command)s" is %(return)s' % {"command":cmd, "return":p.returncode})
    if ctx.flags.debug:
        ctx.logger.debug('output for "%(command)s" is %(output)s' % {"command":cmd, "output":out})
        ctx.logger.debug('error value for "%(command)s" is %(error)s' % {"command":cmd, "error":error})
    return (p.returncode, out, error)


# TODO: it might be worthwhile to try to remove the
# use of ctx.stdout, and use run_batch()'s return
# values instead. but this is good enough :)
def run_logged(cmd, argv):
    """Run command and get the return value."""
    ctx.logger.info('Running %s' % " ".join(cmd))
    env = os.environ.copy()
    env.update({"LC_ALL": "C"})
    if ctx.stdout:
        stdout = ctx.stdout
    else:
        if ctx.flags.debug:
            stdout = None
        else:
            stdout = subprocess.PIPE
    if ctx.stderr:
        stderr = ctx.stderr
    else:
        if ctx.flags.debug:
            stderr = None
        else:
            stderr = subprocess.STDOUT

    cmd = "%s %s" % (cmd, ' '.join(argv))
    p = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr, env=env)
    out, error = p.communicate()
    ctx.logger.debug('return value for "%(command)s" is %(return)s' % {"command":cmd, "return":p.returncode})
    ctx.logger.debug('output for "%(command)s" is %(output)s' % {"command":cmd, "output":out})
    ctx.logger.debug('error value for "%(command)s" is %(error)s' % {"command":cmd, "error":error})

    return (p.returncode, out, error)

efi = None
def isEfi():
    global efi
    if efi is not None:
        return efi

    efi = False
    if os.path.exists("/sys/firmware/efi"):
        efi = True

    return efi

def getArch():
    if isX86(bits=32):
        return 'i686'
    elif isX86(bits=64):
        return 'x86_64'
    else:
        return os.uname()[4]

def isX86(bits=None):
    arch = os.uname()[4]

    if bits is None:
        if (arch.startswith('i') and arch.endswith('86')) or arch == 'x86_64':
            return True
    elif bits == 32:
        if arch.startswith('i') and arch.endswith('86'):
            return True
    elif bits == 64:
        if arch == 'x86_64':
            return True

    return False

def memInstalled():
    f = open("/proc/meminfo", "r")
    lines = f.readlines()
    f.close()

    for line in lines:
        if line.startswith("MemTotal:"):
            fields = line.split()
            mem = fields[1]
            break

    return int(mem)

def swap_suggestion(quiet=0):
    mem = memInstalled()/1024
    mem = ((mem/16)+1)*16
    if not quiet:
        ctx.logger.info("Detected %sM of memory", mem)

    if mem <= 256:
        minswap = 256
        maxswap = 512
    else:
        if mem > 2048:
            minswap = 1024
            maxswap = 2048 + mem
        else:
            minswap = mem
            maxswap = 2*mem

    if not quiet:
        ctx.logger.info("Swap attempt of %sM to %sM", minswap, maxswap)

    return (minswap, maxswap)

def notify_kernel(path, action="change"):
    """ Signal the kernel that the specified device has changed. """
    ctx.logger.debug("notifying kernel of '%s' event on device %s" % (action, path))
    path = os.path.join(path, "uevent")
    if not path.startswith("/sys/") or not os.access(path, os.W_OK):
        ctx.logger.debug("sysfs path '%s' invalid" % path)
        raise ValueError("invalid sysfs path")

    f = open(path, "a")
    f.write("%s\n" % action)
    f.close()

def get_sysfs_path_by_name(dev_name, class_name="block"):
    dev_name = os.path.basename(dev_name)
    sysfs_class_dir = "/sys/class/%s" % class_name
    dev_path = os.path.join(sysfs_class_dir, dev_name)
    if os.path.exists(dev_path):
        return dev_path

def mkdirChain(dir):
    try:
        os.makedirs(dir, 0755)
    except OSError as e:
        try:
            if e.errno == errno.EEXIST and stat.S_ISDIR(os.stat(dir).st_mode):
                return
        except:
            pass

        ctx.logger.error("could not create directory %s: %s" % (dir, e.strerror))

def swap_amount():
    f = open("/proc/meminfo", "r")
    lines = f.readlines()
    f.close()

    for l in lines:
        if l.startswith("SwapTotal:"):
            fields = string.split(l)
            return int(fields[1])
    return 0

def mount(device, location, filesystem, readOnly=False,
          bindMount=False, remount=False, options=None, createDir=True):
    flags = None
    location = os.path.normpath(location)
    if not options:
        opts = ["defaults"]
    else:
        opts = options.split(",")

    if ctx.mountCount.has_key(location) and ctx.mountCount[location] > 0:
        ctx.mountCount[location] = ctx.mountCount[location] + 1
        return

    if createDir and not os.path.exists(location):
        ctx.logger.debug("Creating temporary directory %s for %s" % (location, device))
        os.makedirs(location)

    if readOnly or bindMount or remount:
        if readOnly:
            opts.append("ro")
        if bindMount:
            opts.append("bind")
        if remount:
            opts.append("remount")

    flags = ",".join(opts)
    argv = ["-t", filesystem, device, location, "-o", flags]
    rc = run_batch("mount", argv)[0]
    if not rc:
        ctx.mountCount[location] = 1

    return rc

def umount(location, removeDir=True):
    location = os.path.normpath(location)

    if not os.path.isdir(location):
        raise ValueError, "util.umount() can only umount by mount point. %s is not existing directory" % location

    if ctx.mountCount.has_key(location) and ctx.mountCount[location] > 1:
        ctx.mountCount[location] = ctx.mountCount[location] - 1
        return

    ctx.logger.debug("util.umount()- going to unmount %s, removeDir = %s" % (location, removeDir))
    rc = run_batch("umount", [location])[0]

    if removeDir and os.path.isdir(location):
        try:
            os.rmdir(location)
        except:
            pass

    if not rc and ctx.mountCount.has_key(location):
        del ctx.mountCount[location]

    return rc

def createAvailableSizeSwapFile(storage):
    (minsize, maxsize) = swap_suggestion()
    filesystems = []

    for device in storage.storageset.devices:
        if not device.format:
            continue
        if device.format.mountable and device.format.linuxNative:
            if not device.format.status:
                continue
            space = yali.sysutils.available_space(ctx.consts.target_dir + device.format.mountpoint)
            if space > 16:
                info = (device, space)
                filesystems.append(info)

    for (device, availablespace) in filesystems:
        if availablespace > maxsize and (size > (suggestion + 100)):
            suggestedDevice = device


def chroot(command):
    if ctx.storage.storageset.active:
        run_batch("chroot", [ctx.consts.target_dir, command])
    else:
        ctx.logger.error("util.chroot:StorageSet not activated")


def start_dbus():
    chroot("/sbin/ldconfig")
    chroot("/sbin/update-environment")
    chroot("/bin/service dbus start")

def stop_dbus():
    filesdb = pisi.db.filesdb.FilesDB()
    if filesdb.is_initialized():
        filesdb.close()

    # stop dbus
    chroot("/bin/service dbus stop")
    # kill comar in chroot if any exists
    chroot("/bin/killall comar")

def comarLinkInitialized():
    if ctx.flags.install_type == ctx.STEP_BASE or \
       ctx.flags.install_type == ctx.STEP_DEFAULT or \
       ctx.flags.install_type == ctx.STEP_RESCUE:
        if ctx.storage.storageset.active:
            ctx.socket = os.path.join(ctx.consts.target_dir, ctx.consts.dbus_socket)
            if not os.path.exists(ctx.socket):
                ctx.logger.debug("initializeComar: Dbus has not started")
                start_dbus()
                ctx.logger.debug("wait 2 second for dbus activation")
                time.sleep(2)
        else:
            ctx.logger.debug("initializeComar: StorageSet not activated")
            return False

    elif ctx.flags.install_type == ctx.STEP_FIRST_BOOT:
        ctx.socket = os.path.join(ctx.consts.root_dir, ctx.consts.dbus_socket)

    for i in range(40):
        try:
            ctx.logger.info("Trying to activate Comar")
            ctx.link = comar.Link(socket=ctx.socket)
        except dbus.DBusException:
            time.sleep(1)
            ctx.logger.debug("wait 1 second for dbus activation")
        else:
            if ctx.link:
                break

    if not ctx.link:
        ctx.logger.debug("Comar not activated")
        return False

    ctx.logger.info("Comar activated")
    return True

def check_link():
    active = True
    if not ctx.link:
        active = comarLinkInitialized()
    return active

def getUsers():
    users = []
    if check_link():
        ctx.logger.info("Getting users from system")
        all_users = ctx.link.User.Manager["baselayout"].userList()
        system_users = filter(lambda user: user[0] == 0 or (user[0] >= 1000 and user[0] <= 65000), all_users)
        ctx.logger.info("System Users :%s" % system_users)
        for user in system_users:
            u = yali.users.User(user[1])
            u.realname = user[2]
            u.uid = user[0]
            users.append(u)
    return users

def backup_log(remove=False):
    try:
        # store log content
        shutil.copyfile("/var/log/yali.log", os.path.join(ctx.consts.target_dir, "var/log/yaliInstall.log"))
        if remove:
            os.remove("/var/log/yali.log")
    except IOError, msg:
        ctx.logger.debug("YALI log file doesn't exists.")
        return False
    except Exception, msg:
        ctx.logger.debug("File paths are the same.")
        return False
    else:
        return True

def reboot():
    run_batch("/tmp/reboot", ["-f"])

def shutdown():
    run_batch("/tmp/shutdown", ["-h", "now"])

def eject(mount_point=ctx.consts.source_dir):
    if "copytoram" not in open("/proc/cmdline", "r").read().strip().split():
        run_batch("eject", ["-m", mount_point])
    else:
        reboot()

def sync():
    os.system("sync")
    os.system("sync")
    os.system("sync")

def check_dual_boot():
    return isX86()

def writeLocaleFromCmdline():
    locale_file_path = os.path.join(ctx.consts.target_dir, "etc/env.d/03locale")
    f = open(locale_file_path, "w")

    f.write("LANG=%s\n" % yali.localedata.locales[ctx.consts.lang]["locale"])
    f.write("LC_ALL=%s\n" % yali.localedata.locales[ctx.consts.lang]["locale"])

def setKeymap(keymap, variant=None, root=False):
    ad = ""
    if variant:
        ad = "-variant %s" % variant
    else:
        variant = "\"\""

    if not root:
        if "," in keymap:
            ad += " -option grp:alt_shift_toggle"
        return run_batch("setxkbmap", ["-option", "-layout", keymap, ad])

    elif os.path.exists("/usr/libexec/xorg-save-xkb-config.sh"):
        return run_batch("/usr/libexec/xorg-save-xkb-config.sh", [ctx.consts.target_dir])

    else:
        chroot("hav call zorg Xorg.Display setKeymap %s %s" % (keymap, variant))

def writeKeymap(keymap):
    mudur_file_path = os.path.join(ctx.consts.target_dir, "etc/conf.d/mudur")
    lines = []
    for l in open(mudur_file_path, "r").readlines():
        if l.strip().startswith('keymap=') or l.strip().startswith('# keymap='):
            l = 'keymap="%s"\n' % keymap
        if l.strip().startswith('language=') or l.strip().startswith('# language='):
            if ctx.consts.lang == "pt":
                l = 'language="pt_BR"\n'
            else:
                l = 'language="%s"\n' % ctx.consts.lang
        lines.append(l)

    open(mudur_file_path, "w").writelines(lines)

def write_config_option(conf_file, section, option, value):
    configParser = ConfigParser.ConfigParser()
    configParser.read(conf_file)
    if not configParser.has_section(section):
        configParser.add_section(section)
    configParser.set(section, option, value)
    with open(conf_file, "w")  as conf:
        configParser.write(conf)

def parse_branding_screens(release_file):
    try:
        document = piksemel.parse(release_file)
    except OSError, msg:
        if msg.errno == 2:
            raise yali.Error, _("Release file is missing")
    except piksemel.ParseError:
        raise yali.Error, _("Release file is inconsistent")

    if document.name() != "Release":
        raise yali.Error, _("Invalid xml file")

    screens = {}
    screens_tag = document.getTag("screens")
    if screens_tag:
        for screen_tag in screens_tag.tags("screen"):
            name = screen_tag.getTagData("name")
            icon = screen_tag.getTagData("icon")
            if not icon:
                icon  = ""

            title_tags = screen_tag.tags("title")
            if title_tags:
                titles = {}
                for title_tag in title_tags:
                    lang = title_tag.getAttribute("xml:lang")
                    if not lang:
                        lang = "en"
                    titles[lang] = unicode(title_tag.firstChild().data())

            help_tags = screen_tag.tags("help")
            if help_tags:
                helps = {}
                for help_tag in help_tags:
                    lang = help_tag.getAttribute("xml:lang")
                    if not lang:
                        lang = "en"
                    helps[lang] = unicode(help_tag.firstChild().data())

            screens[name] = (icon, titles, helps)

    return screens

def parse_branding_slideshows(release_file):
    try:
        document = piksemel.parse(release_file)
    except OSError, msg:
        if msg.errno == 2:
            raise yali.Error, _("Release file is missing")
    except piksemel.ParseError:
        raise yali.Error, _("Release file is inconsistent")

    if document.name() != "Release":
        raise yali.Error, _("Invalid xml file")

    slideshows = []
    slideshows_tag = document.getTag("slideshows")
    if slideshows_tag:
        for slideshow_tag in slideshows_tag.tags("slideshow"):
            picture = slideshow_tag.getTagData("picture")

            description_tags = slideshow_tag.tags("description")
            if description_tags:
                descriptions = {}
                for description_tag in description_tags:
                    lang = description_tag.getAttribute("xml:lang")
                    if not lang:
                        lang = "en"
                    descriptions[lang] = unicode(description_tag.firstChild().data())

            slideshows.append((picture, descriptions))

    return slideshows

def set_partition_privileges(device, mode, uid, gid):
    device_path =  os.path.join(ctx.consts.target_dir, device.format.mountpoint.lstrip("/"))
    ctx.logger.debug("Trying to change privileges %s path" % device_path)
    if os.path.exists(device_path):
        try:
            os.chmod(device_path, mode)
            os.chown(device_path, uid, gid)
        except OSError, msg:
                ctx.logger.debug("Unexpected error: %s" % msg)

def grub_disk_name(storage, device, exists=False):
    if exists:
        return "hd%d" % (storage.drives.index(device.name) + 1)
    else:
        return "hd%d" % storage.drives.index(device.name)

def grub_partition_name(storage, device, exists=False):
    (disk, number) = get_disk_partition(device)
    if number is not None:
        return "(%s,%d)" % (grub_disk_name(storage, disk, exists), number - 1)
    else:
        return "(%s)" % (grub_disk_name(storage, disk, exists))

def get_disk_partition(device):
    if device.type == "partition":
        number = device.partedPartition.number
        disk = device.disk
    else:
        number = None
        disk = device

    return (disk, number)

def get_grub_conf(device_path, format_type):
    if os.path.exists(ctx.consts.tmp_mnt_dir):
        umount(ctx.consts.tmp_mnt_dir)

    grub_conf = None
    ctx.logger.debug("Mounting %s to %s to check partition" % (device_path, ctx.consts.tmp_mnt_dir))
    rc = mount(device_path, ctx.consts.tmp_mnt_dir, format_type)
    if rc:
        ctx.logger.debug("Mount failed for %s " % device_path)
    else:
        is_exist = lambda p, f: os.path.exists(os.path.join(ctx.consts.tmp_mnt_dir, p, f))

        grub_path = None
        if is_exist("boot/grub", "grub.conf") or is_exist("boot/grub", "menu.lst"):
            grub_path = "boot/grub"
        elif is_exist("grub", "grub.conf") or is_exist("grub", "menu.lst"):
            grub_path = "grub"

        if grub_path:
            ctx.logger.debug("%s device has bootloader configuration to parse." % device_path)
            menulst = os.path.join(ctx.consts.tmp_mnt_dir, grub_path, "menu.lst")
            grubconf = os.path.join(ctx.consts.tmp_mnt_dir, grub_path, "grub.conf")
            if os.path.islink(menulst):
                ctx.logger.debug("Additional grub.conf found on device %s" % device_path)
                grub_path = grubconf
            else:
                ctx.logger.debug("Additional menu.lst found on device %s" % device_path)
                grub_path = menulst

            grub_conf = grubutils.grubConf()
            grub_conf.parseConf(grub_path)
        else:
            ctx.logger.debug("%s device has not any bootloader configuration to parse." % device_path)

        umount(ctx.consts.tmp_mnt_dir)

    return grub_conf

class PackageCollection(object):
    def __init__(self, id, title, description, icon, translations, default=False):
        self.default = default
        self.id = id
        self.title = title
        self.description = description
        self.icon = icon
        self.translations = translations
        self.index =  os.path.join(ctx.consts.source_dir, "repo/%s-index.xml.bz2" % id)

def get_collections():
    packageCollection = []

    def _setLocale(id, translations):
        title = ""
        description = ""
        locale = os.environ["LANG"].split(".")[0]
        if not translations.has_key(locale):
            ctx.logger.debug("Collection (%s) has no translation in %s locale. Default language (%s) is setting ..." %
                                                            (id, locale, translations["default"]))
            locale = translations["default"]

        title = translations[locale][0]
        description = translations[locale][1]
        return (title, description)

    try:
        piksemelObj = piksemel.parse(ctx.consts.pisi_collection_file)
    except OSError, msg:
        ctx.logger.debug("Unexcepted error:%s" % msg)
    else:
        default = False
        translations = {}
        for collection in piksemelObj.tags("Collection"):
            default = collection.getAttribute("default")
            if default:
                default = True

            id = collection.getTagData("id")
            icon = collection.getTagData("icon")
            translationsTag = collection.getTag("translations")
            translations["default"] = translationsTag.getAttribute("default")
            for translation in translationsTag.tags("translation"):
                translations[translation.getAttribute("language")]= (unicode(translation.getTagData("title")),
                                                                     unicode(translation.getTagData("description")))
            title, description = _setLocale(id, translations)
            packageCollection.append(PackageCollection(id, title, description, icon, translations, default))

    return packageCollection

