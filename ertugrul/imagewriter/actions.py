#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.system("qmake DEFINES=USEUDISKS imagewriter.pro \
                       PREFIX=%s/usr" % get.installDIR())

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING")
    
    pisitools.insinto("/usr/share/pixmaps/", "icons/64x64/imagewriter.png")