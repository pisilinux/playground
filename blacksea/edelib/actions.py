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
    shelltools.system("./autogen.sh")
    
    shelltools.export("CFLAGS","%s -fPIC" % get.CFLAGS())
    shelltools.export("CXXFLAGS","%s -fPIC" % get.CXXFLAGS())
    
    autotools.configure("--prefix=/usr")

                         

def build():
    shelltools.system("jam -j2")

def install():
    shelltools.system('jam -sDESTDIR="%s" \
                      -sdocdir="%s/usr/share/doc" \
                      install' % (get.installDIR(), get.installDIR()))
    pisitools.remove("/usr/share/doc/edelib-2.0.0/INSTALL")
