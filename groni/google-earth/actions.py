#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "."
NoStrip = ["/"]

def setup():
    shelltools.system("ar x %s/google-earth-stable_current_amd64.deb" %get.workDIR())
    shelltools.system("tar --lzma -xvf %s/data.tar.lzma --exclude=usr/bin --exclude=etc --exclude=opt/google/earth/free/google-earth" %get.workDIR())
    shelltools.chmod("%s/opt/google/earth/*" %get.workDIR())

def install():
    pisitools.insinto("/opt/", "./opt/*")
    pisitools.dosym("/opt/google/earth/free/googleearth", "/usr/bin/googleearth")
    pisitools.dosym("/lib/ld-linux.so.2", "/lib/ld-lsb.so.3")
    pisitools.dosym("/usr/lib32/mesa/libGL.so.1.2","/etc/alternatives/libGL-32bit")
    

