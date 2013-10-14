#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt 

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("CFLAGS", get.CFLAGS())
shelltools.export("CXXFLAGS", get.CXXFLAGS())

def setup():     
    autotools.configure("--disable-silent-rules \
                         --with-equalizer \
                         LDFLAGS=-zmuldefs")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "README")

