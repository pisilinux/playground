#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import libtools

WorkDir = "ros/"

def setup():
    autotools.autoreconf("-fi")
    autotools.configure("--disable-debug --enable-production")

def build():
    autotools.make()

def install():
    libtools.libtoolize()
    autotools.install()
    pisitools.domove("/usr/inc/*", "/usr/include/occ/") 
    pisitools.removeDir("/usr/inc") 
    pisitools.dodoc("LICENSE")