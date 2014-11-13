#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import parted
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.util
import yali.context as ctx
from pardus import grubutils

class BootLoaderError(yali.Error):
    pass

class ReleaseError(BootLoaderError):
    pass

class KernelError(BootLoaderError):
    pass


dos_filesystems = ('FAT', 'fat16', 'fat32', 'ntfs', 'hpfs')
linux_filesystems = ('ext4', 'ext3', 'reisersfs', 'xfs')
allParameters = ["root", "initrd", "init", "xorg", "yali", "BOOT_IMAGE", \
                 "lang", "mudur", "copytoram"]

BOOT_TYPE_NONE = 0
BOOT_TYPE_MBR = 1
BOOT_TYPE_PARTITION = 2
BOOT_TYPE_RAID = 4

boot_type_strings = {BOOT_TYPE_PARTITION: "None",
                     BOOT_TYPE_MBR: "Master Boot Record(MBR)",
                     BOOT_TYPE_PARTITION: "First sector of Pardus Boot partition",
                     BOOT_TYPE_RAID: "RAID Device"}

def get_configs(rootpath):
    try:
        releasePath = os.path.join(rootpath, "etc/pardus-release")
        release = file(releasePath).readlines()[0].strip()
        bootDir = os.path.join(rootpath, "boot")
        kernels = glob.glob(bootDir + "/kernel-*")
        kernel = os.path.basename(sorted(kernels)[-1])
        kernelVersion = kernel[len("kernel-"):]
        initramfs = "initramfs-%s" % kernelVersion
    except IOError, msg:
        raise ReleaseError, msg
    except IndexError, msg:
        raise KernelError, msg
    else:
        return (release, kernel, initramfs)

def get_commands(rootDevice, swapDevice=None):
    def is_required(parameter):
        for p in allParameters:
            if parameter.startswith("%s=" % p):
                return False
        return True

    _commands = []
    _commands.append("root=%s" % (rootDevice.fstabSpec))

    if swapDevice:
        _commands.append("resume=%s" % swapDevice.path)

    for parameter in [x for x in open("/proc/cmdline", "r").read().split()]:
        if is_required(parameter):
            _commands.append(parameter)

    if ctx.blacklistedKernelModules:
        _commands.append("blacklist=%s" % ",".join(ctx.blacklistedKernelModules))

    return " ".join(_commands).strip()

grub_conf = """\
default 0
timeout 10
gfxmenu %(bootpath)sgrub/message
background 10333C

title %(release)s
uuid %(uuid)s
kernel %(bootpath)s%(kernel)s %(commands)s
initrd %(bootpath)s%(initramfs)s

"""

windows_conf = """
title %(title)s on %(device)s
rootnoverify %(root)s
makeactive
chainloader +1

"""
windows_conf_multiple_disks = """
title %(title)s on %(device)s
map (hd0) %(root)s
map %(root)s (hd0)
rootnoverify %(root)s
makeactive
chainloader +1

"""

def get_physical_devices(storage, device):
    _devices = []
    _physicalDevices = []
    if device.type == "mdarray":
        if device.level != 1:
            ctx.logger.error("Ignoring non level 1 raid array %s" % device.name)
            return _devices
        _devices = device.parents
    else:
        _devices = [device]

    for _device in _devices:
        if _device in storage.disks or _device.type == "partition":
            _physicalDevices.append(device)
        else:
            ctx.logger.error("Ignoring %s" % device.name)

    return _physicalDevices


class BootLoader(object):
    _conf = "boot/grub/grub.conf"
    _deviceMap = "device.map"
    def __init__(self, storage=None):
        self.storage = storage
        self.path = "/boot/"
        self._stage1Device = None
        self._stage2Device = None
        self._rootDevice = None
        self._swapDevice = None
        self._type = BOOT_TYPE_NONE
        self.grubConf = None
        self.removableExists = False

    def _setStage1Device(self, device):
        self._stage1Device = device

        if device:
            partition = yali.util.get_disk_partition(self.storage.devicetree.getDeviceByName(device))[1]
            if partition is None:
                self._type = BOOT_TYPE_MBR
            else:
                self._type = BOOT_TYPE_PARTITION

    def _getStage1Device(self):
        return self._stage1Device

    stage1Device = property(lambda f: f._getStage1Device(),
                            lambda f,d: f._setStage1Device(d))

    def _setStage2Device(self, device):
        self._stage2Device = device

    def _getStage2Device(self):
        if not self._stage2Device:
            self._stage2Device = self.storage.storageset.bootDevice

        return self._stage2Device

    stage2Device = property(lambda f: f._getStage2Device(),
                            lambda f,d: f._setStage2Device(d))

    def _setRootDevice(self, device):
        self._rootDevice = device

    def _getRootDevice(self):
        if not self._rootDevice:
            self._rootDevice = self.storage.rootDevice

        return self._rootDevice

    rootDevice = property(lambda f: f._getRootDevice(),
                          lambda f,d: f._setRootDevice(d))
    def _setSwapDevice(self, device):
        self._swapDevice = device

    def _getSwapDevice(self):
        if not self._swapDevice and self.storage.swaps:
            self._swapDevice = self.storage.swaps[0]

        return self._swapDevice

    swapDevice = property(lambda f: f._getSwapDevice(),
                          lambda f,d: f._setSwapDevice(d))

    def _setBootType(self, type):
        self._type = type

    def _getBootType(self):
        return self._type

    bootType = property(lambda f: f._getBootType(),
                       lambda f,d: f._setBootType(d))

    @property
    def choices(self):
        _choices = {}

        if not self.stage2Device:
            return _choices

        if self.stage2Device.type == "mdarray":
            _choices[BOOT_TYPE_RAID] = (self.stage2Device.name, _("%s" % boot_type_strings[BOOT_TYPE_RAID]))
            _choices[BOOT_TYPE_MBR] = (self.drives[0], _("%s" % boot_type_strings[BOOT_TYPE_MBR]))
        else:
            _choices[BOOT_TYPE_PARTITION] = (self.stage2Device.name, _("%s" % boot_type_strings[BOOT_TYPE_PARTITION]))
            _choices[BOOT_TYPE_MBR] = (self.drives[0], _("%s" % boot_type_strings[BOOT_TYPE_MBR]))

        return _choices

    @property
    def drives(self):
        disks = self.storage.disks
        partitioned = self.storage.partitioned
        drives = [d.name for d in disks if d in partitioned]
        drives.sort(cmp=self.storage.compareDisks)
        return drives

    def write(self):
        self.writeGrubConf()

        usedDevices = set()
        usedDevices.update(get_physical_devices(self.storage, self.storage.devicetree.getDeviceByName(self.stage1Device)))
        usedDevices.update(get_physical_devices(self.storage, self.stage2Device))

        self.writeDeviceMap(usedDevices)

    def writeGrubConf(self):
        bootDevices = get_physical_devices(self.storage, self.stage2Device)
        rootDevice = self.rootDevice
        swapDevice = self.swapDevice
        (release, kernel, initramfs ) = get_configs(ctx.consts.target_dir)
        s = grub_conf % {"uuid": bootDevices[0].fstabSpec.split("=")[1].lower(),
                         "bootpath" : self.path,
                         "release": release,
                         "kernel": kernel,
                         "commands": get_commands(rootDevice, swapDevice),
                         "initramfs": initramfs}
        ctx.logger.debug("uuid:%s -  bootpath:%s - release:%s - kernel:%s -commands:%s - initramfs:%s" %
                        (bootDevices[0].fstabSpec.split("=")[1].lower(), self.path, release, kernel,
                         get_commands(rootDevice, swapDevice), initramfs))
        ctx.logger.debug("conf:%s" % os.path.join(ctx.consts.target_dir, self._conf))
        with open(os.path.join(ctx.consts.target_dir, self._conf), "w") as grubConfFile:
            grubConfFile.write(s)

        target_conf_dir = os.path.join(ctx.consts.target_dir, "etc")
        if os.path.exists(target_conf_dir):
            ctx.logger.debug("Target grub.conf file is writing")
            self.writeGrubInstallConf(os.path.join(target_conf_dir, "grub.conf"), removableExists=False)

        yali.util.cp(os.path.join(target_conf_dir, "grub.conf"), "/tmp/batch")
        ctx.logger.debug("Target grub.conf file is copying to use with grub")
        self.appendOtherSystems()

    def appendOtherSystems(self):
        for partition in [p for p in self.storage.partitions if p.exists]:
            if partition.partType not in (parted.PARTITION_NORMAL, parted.PARTITION_LOGICAL) or not partition.format:
                continue

            if not partition.getFlag(parted.PARTITION_DIAG):
                if partition.format.type in  ('fat32', 'ntfs-3g') and \
                        yali.util.check_dual_boot():
                    if partition.format.type == "fat32":
                        self.appendDOSSystems(partition.path, "vfat")
                    else:
                        self.appendDOSSystems(partition.path, "ntfs")

                elif partition.format.type in ('ext4', 'ext3', 'reisersfs', 'xfs'):
                    bootDevice = get_physical_devices(self.storage, self.stage2Device)[0]
                    if partition.path != bootDevice.path:
                        self.appendLinuxSystems(partition.path, partition.format.type)

    def appendDOSSystems(self, device, formatType):
        if not os.path.isdir(ctx.consts.tmp_mnt_dir):
            ctx.logger.debug("Creating temporary mount point %s for %s to check partitions" % (ctx.consts.tmp_mnt_dir, device))
            os.makedirs(ctx.consts.tmp_mnt_dir)
        else:
            yali.util.umount(ctx.consts.tmp_mnt_dir)

        try:
            ctx.logger.debug("Mounting %s to %s to check partition" % (device, ctx.consts.tmp_mnt_dir))
            yali.util.mount(device, ctx.consts.tmp_mnt_dir, formatType)
        except Exception:
            ctx.logger.debug("Mount failed for %s " % device)
            return None
        else:
            is_exist = lambda f: os.path.exists(os.path.join(ctx.consts.tmp_mnt_dir, f))
            if is_exist("boot.ini") or is_exist("command.com") or is_exist("bootmgr"):
                with open(os.path.join(ctx.consts.target_dir, self._conf), "a") as grubConfFile:
                    windowsBoot = yali.util.grub_partition_name(self.storage, self.storage.devicetree.getDeviceByPath(device))
                    bootDevice = get_physical_devices(self.storage, self.stage2Device)[0]
                    ctx.logger.debug("Windows boot on %s" % windowsBoot)

                    if bootDevice.name == self.storage.devicetree.getDeviceByPath(device).parents[0]:
                        s = windows_conf % {"title": _("Windows"),
                                            "device": device,
                                            "root": windowsBoot}
                    else:
                        s = windows_conf_multiple_disks % {"title": _("Windows"),
                                                           "device": device,
                                                           "root": windowsBoot}
                    grubConfFile.write(s)

            yali.util.umount(ctx.consts.tmp_mnt_dir)

    def appendLinuxSystems(self, device, formatType):
        additional_conf = yali.util.get_grub_conf(device, formatType)
        if additional_conf and len(additional_conf.entries):
            self.grubConf = grubutils.grubConf()
            self.grubConf.parseConf(os.path.join(ctx.consts.target_dir, self._conf))
            for entry in additional_conf.entries:
                stage2Device = None
                if entry.getCommand("uuid"):
                    stage2Device = entry.getCommand("uuid").value
                elif entry.getCommand("root"):
                    stage2Device = entry.getCommand("root").value
                if stage2Device:
                    entry.title = entry.title + " [ %s ]" % device
                    self.grubConf.addEntry(entry)

            self.grubConf.write(os.path.join(ctx.consts.target_dir, self._conf))

    def writeDeviceMap(self, usedDevices):
        with open(os.path.join(ctx.consts.target_dir, "boot/grub", self._deviceMap), "w+") as deviceMapFile:
            deviceMapFile.write("# this device map was generated by YALI\n")
            usedDisks = set()
            for device in usedDevices:
                drive = yali.util.get_disk_partition(device)[0]
                usedDisks.add(drive)
            devices = list(usedDisks)
            devices.sort(key=lambda d: d.name)
            for device in devices:
                deviceMapFile.write("(%s)     %s\n" % (yali.util.grub_disk_name(self.storage, device), device.path))

        yali.util.cp(os.path.join(ctx.consts.target_dir, "boot/grub", self._deviceMap), "/tmp/device.map")

    def writeGrubInstallConf(self, path, removableExists=False):
        stage1Devices = get_physical_devices(self.storage, self.storage.devicetree.getDeviceByName(self.stage1Device))
        bootDevices = get_physical_devices(self.storage, self.stage2Device)

        stage1Path = yali.util.grub_partition_name(self.storage, stage1Devices[0], exists=removableExists)
        bootPartitionPath = yali.util.grub_partition_name(self.storage, bootDevices[0], exists=removableExists)

        batch_template = """root %s
setup %s
quit
""" % (bootPartitionPath, stage1Path)

        ctx.logger.debug("Writing Batch template to %s:\n%s" % (path, batch_template))
        file(path,'w').write(batch_template)


    def install(self, batch=False):
        if batch:
            return self.install_batch()
        else:
            return self.install_devicemap()

    def install_batch(self):
        rc = yali.util.run_batch("grub", ["--no-floppy", "--batch < ", "/tmp/batch"])[0]
        yali.util.sync()
        return rc

    def install_devicemap(self):
        rc = yali.util.run_batch("grub", ["--no-floppy", "--device-map=/tmp/device.map", "--batch < ", "/tmp/batch"])[0]
        yali.util.sync()
        return rc
