#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "."
NoStrip = ["/"]

def setup():
    shelltools.system("rpm2targz -v %s/draftSight.rpm" %get.workDIR())
    shelltools.system("tar xfvz %s/draftSight.tar.gz" %get.workDIR())

    shelltools.chmod(get.workDIR() + "/opt/dassault-systemes/draftsight/*", 0755)

def install():
    pisitools.insinto("/usr/", "./usr/*")
    pisitools.insinto("/opt/", "./opt/*")
    pisitools.insinto("/var/", "./var/*")
    
    pisitools.dosym("/usr/bin/draftsight", "/usr/bin/draftsight.bin")
    if get.ARCH() == "x86_64":
        pisitools.dosym("/usr/bin/draftsight", "/usr/bin/32/draftsight.bin")
        pisitools.insinto("/opt/dassault-systemes/draftsight/lib", "libaudio.so.2")

    pisitools.dosym("/opt/dassault-systemes/draftsight/mime/pixmaps/32x32/dassault-systemes_draftsight.png", "/usr/share/pixmaps/dassault-systemes_draftsight.png")

    pisitools.dohtml("opt/dassault-systemes/draftsight/Eula/english/*")