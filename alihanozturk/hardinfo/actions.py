#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    pisitools.dosed("hardinfo.desktop", "Categories=System;", "Categories=System;Settings;HardwareSettings;")
    shelltools.system("sed -i -e 's|/usr/lib64|/usr/lib|' configure")
    autotools.configure("--prefix=/usr")
    shelltools.system("sed -i -e 's|lib64|lib|' binreloc.c")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.removeDir("/usr/local/")
    
    pisitools.dodoc("LICENSE", "TODO")
