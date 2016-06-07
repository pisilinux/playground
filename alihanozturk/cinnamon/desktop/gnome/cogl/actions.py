#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools

def setup():
    autotools.autoreconf("-vfi")
    autotools.configure("--enable-gles1 \
                         --enable-wayland-egl-server=yes \
                         --enable-wayland-egl-platform=yes \
                         --enable-kms-egl-platform=yes \
                         --enable-cogl-gst=yes \
                         --enable-gles2")
                        
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make("-j1")

def install():
    autotools.install()

    pisitools.dodoc("COPYING", "README")

