#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 TUBITAK/BILGEM
# Renan Çakırerk <renan at pardus.org.tr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# (See COPYING)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSize, SIGNAL, QThread
from quickformat.disktools import *
from subprocess import Popen, PIPE, STDOUT, call

import parted

class Formatter(QThread):
    def __init__(self):
        QThread.__init__(self)

        # Volume to format
        self.volume = None

        # Volumes current or new file system
        self.new_file_system = None

        # Volumes current or new file system
        self.new_label = None

        # Formatting status
        self.formatting = False

        # Error state
        self.error = False

    def run(self):
        # Send signal for notification
        self.formatting = True
        self.emit(SIGNAL("format_started()"))

        self.formatted = self.format_disk()

        if self.formatted == True:
            try:
                refreshPartitionTable(self.volume.device_path)
            except:
                print "ERROR: Cannot refresh partition table"

            self.emit(SIGNAL("format_successful()"))
        else:
            if self.error:
                self.error = False
                self.emit(SIGNAL("partition_table_error()"))

            else:
                self.emit(SIGNAL("format_failed()"))

        self.formatting = False


    def set_volume_to_format(self, volume, file_system, label):
        self.volume = volume
        self.new_file_system = file_system
        self.new_label = label

    def is_device_mounted(self):
        for mountPoint in getMounted():
            if self.volume.path == mountPoint[0]:
                return True

    def _set_partition_privileges(self, device_path, mode, uid, gid):
        if os.path.exists(device_path):
            try:
                os.chmod(device_path, mode)
                os.chown(device_path, uid, gid)
            except OSError, msg:
                print msg
                #ctx.logger.debug("Unexpected error: %s" % msg)

    def _set_file_system_type(self):
        try:
            print "---------------"
            print "TRYING TO SET FILE SYSTEM of %s to %s" % (self.volume.device_path, self.new_file_system)

            try:
                parted_device = parted.Device(self.volume.device_path)
                parted_disk = parted.Disk(parted_device)
            except:
                parted_device = parted.Device(self.volume.path)
                parted_disk = parted.Disk(parted_device)

            parted_partition = parted_disk.getPartitionByPath(self.volume.path)

            parted_partition.system = parted.fileSystemType.get(self.new_file_system_parted)

            # Commit Changes
            parted_disk.commit()
            print "SUCCCESS"
        except Exception, e:
            print "FAILED TO SET FILE SYSTEM", e
            self.error = True
            self.emit(SIGNAL("partition_table_error()"))

    def _remove_volume_flags(self):
        try:
            print "---------------"
            print "TRYING TO REMOVE FLAGS of %s" % self.volume.device_path

            parted_device = parted.Device(self.volume.device_path)
            parted_disk = parted.Disk(parted_device)

            parted_partition = parted_disk.getPartitionByPath(self.volume.path)

            # Get possible flags
            parted_flags = parted.partitionFlag.values()

            # Remove any Flags
            flags_found = parted_partition.getFlagsAsString().split(", ")

            if flags_found:
                for flag in flags_found:
                    if flag:
                        parted_partition.unsetFlag(parted_flags.index(flag) + 1)

            # Commit Changes
            parted_disk.commit()
            print "SUCCCESS"
        except Exception, e:
            print "FAILED TO REMOVE FLAGS \n", e

    def format_disk(self):
        # If device is mounted then unmount

        if self.is_device_mounted() == True:
            try:
                umount(str(self.volume.path))
                print "---------------"
                print "TRYING TO UNMOUNT"
            except:
                print "UNMOUNTING FAILED"
                return False

        # If NTFS is selected then activate quick formating option
        if self.new_file_system == "ntfs-3g":
            self.new_file_system = "ntfs"
            self.quickOption = "-Q"
        else:
            self.quickOption = ""

        # If volume label empty
        if self.new_label == "":
            self.new_label = "My Disk"

        self.new_file_system_parted = ""

        # If VFAT then labeling parameter changes
        if self.new_file_system == "vfat":
            self.labelingCommand = "-n"
            self.new_file_system_parted = "fat32"
        else:
            self.labelingCommand = "-L"
            self.new_file_system_parted = self.new_file_system

        # Set file system type as the selected one
        self._set_file_system_type()

        # Remove any flags from the partition
        self._remove_volume_flags()

        if self.error:
            return False
        # udev trigger here??

        # Command to execute
        command = "mkfs -t %s %s %s '%s' %s -v" % (self.new_file_system, self.quickOption, self.labelingCommand, self.new_label, self.volume.path)
        print "---------------"
        print "COMMAND: %s" % command


        # Execute
        proc = Popen(command, shell = True, stdout = PIPE,)

        # If theres an error then emmit error signal
        output = proc.communicate()[0]
        print "---------------"
        print "OUTPUT: %s" % output
        print "RETURN: %s" % proc.returncode




        if proc.returncode == 0:
            #if os.path.exists("/tmp/quickformat"):
            #    os.mkdir("/tmp/quickformat")

            #mount(self.volume.device_path, "/tmp/quickformat")

            # Set partition privilages
            #self._set_partition_privileges("/tmp/quickformat", 0770, 0, 6)

            return True
