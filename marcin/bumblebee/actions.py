#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    autotools.configure("CONF_DRIVER=nvidia CONF_DRIVER_MODULE_NVIDIA=nvidia \
                         CONF_LDPATH_NVIDIA=/usr/lib/nvidia-bumblebee:/usr/lib32/nvidia-bumblebee \
                         CONF_MODPATH_NVIDIA=/usr/lib/nvidia-bumblebee/xorg/,/usr/lib/xorg/modules")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
