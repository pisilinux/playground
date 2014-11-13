#!/usr/bin/python
#-*- coding: utf-8 -*-
#
#  Copyright (C) 2011 TUBITAK/BILGEM
#  Renan Çakırerk <renan at pardus.org.tr>
#  Batuhan Bayrakçı <batuhanbayrakci at gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#  (See COPYING)

import dbus

from PyQt4 import QtGui

BUSES = ["usb", "firewire", "platform","sdio"]

class Volume:

    def __init__(self, volume):
        self.volume = volume

        bus = dbus.SystemBus()

        # objects about get_volume_property method 
        self.proxy_dbus_volume_properties = bus.get_object("org.freedesktop.UDisks", volume)
        self.iface_dbus_volume_properties = dbus.Interface(self.proxy_dbus_volume_properties, "org.freedesktop.DBus.Properties")

        # object about get_device_property method
        self.proxy_dbus_device_properties = bus.get_object("org.freedesktop.UDisks", self.get_volume_property("PartitionSlave"))
        self.iface_dbus_device_properties = dbus.Interface(self.proxy_dbus_device_properties, "org.freedesktop.DBus.Properties")

        if self.get_volume_property("PartitionSlave") == "/":
            raise Exception()

        self.device_bus = self.get_device_bus()
        self.device_path = self.get_device_path()
        self.device_name = self.get_device_name()

        self.icon = self.get_volume_icon()
        self.name = self.get_volume_name()
        self.path = self.get_volume_path()
        self.file_system = self.get_volume_file_system()
        self.size = self.get_volume_size()


    def get_volume_property(self, prop):
        """gets a property of the volume"""
        try:
            return self.iface_dbus_volume_properties.Get("org.freedesktop.UDisks.Device", prop)
        except Exception, vol_exception:
            return "GET VOLUME PROPERTY FAILED: ", vol_exception

    def get_device_property(self, prop):
        """gets a property of the device"""
        try:
            return self.iface_dbus_device_properties.Get("org.freedesktop.UDisks.Device", prop)
        except Exception, dev_exception:
            return "GET DEVICE PROPERTY FAILED: ", dev_exception

    def get_all_properties(self):
        """gets all properties of device"""
        return self.iface_dbus_properties.GetAll("org.freedesktop.UDisks.Device")

    def has_accepted_bus(self):
        """ controls if the device is appropriate for formatting """
        if self.device_bus in BUSES:
            return True

    # Get Device Information

    def get_device_bus(self):
        """ returns the bus of the device """
        return self.get_device_property("DriveConnectionInterface")

    def get_device_path(self):
        return self.get_device_property("DeviceFile")

    def get_device_name(self):
        """ returns the device name that the volume resides on """
        # product
        return self.get_device_property("DriveVendor") + " " +  self.get_device_property("DriveModel")

    # Get Volume Information

    def get_volume_icon(self):
        if self.get_device_property("DriveModel").lower().find("sd/mmc") >= 0 or self.get_device_property("DriveConnectionInterface") == "sdio":
            return QtGui.QPixmap(":/images/images/media-flash-sd-mmc.png")
        elif self.get_device_property("DriveAtaSmartIsAvailable") > 0:
            return QtGui.QPixmap(":/images/images/drive-removable-media-usb.png")
        else:
            return QtGui.QPixmap(":/images/images/drive-removable-media-usb-pendrive.png")

    def get_volume_name(self):
        return self.get_volume_property("IdLabel")

    def get_volume_path(self):
        # such as /dev/sdb1
        return self.get_volume_property("DeviceFile")

    def get_volume_file_system(self):
        # such as vfat
        return self.get_volume_property("IdType") 

    def get_volume_size(self):
        return self.get_volume_property("PartitionSize")

