#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def setup():
    shelltools.export("CFLAGS","%s -mtune=generic -O2 -pipe -fstack-protector --param=ssp-buffer-size=4 -D_FORTIFY_SOURCE=2 -fPIC" % get.CFLAGS())
    shelltools.export("CXXFLAGS","%s -mtune=generic -O2 -pipe -fstack-protector --param=ssp-buffer-size=4 -D_FORTIFY_SOURCE=2 -fPIC" % get.CXXFLAGS())
    shelltools.system("./autogen.sh")
    autotools.configure("--prefix=/usr \
                         --enable-shared")

def build():
    shelltools.system("jam || true -j2")

def install():
    shelltools.system('jam -sDESTDIR="%s" \
                      install || true' % get.installDIR())

