#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

def setup():
    autotools.autoreconf("-fi")
    autotools.configure("CONF_DRIVER_MODULE_NVIDIA=nvidia \
                         CONF_LDPATH_NVIDIA=/usr/lib/nvidia-bumblebee:/usr/lib32/nvidia-bumblebee \
                         CONF_MODPATH_NVIDIA=/usr/lib/nvidia-bumblebee/xorg/,/usr/lib/xorg/modules \
                         --prefix=/usr \
                         --sysconfdir=/etc")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dosym("/etc/bash_completion.d/bumblebee", "/etc/bash_completion.d/optirun/bumblebee")
    pisitools.dodoc("VERSION")
