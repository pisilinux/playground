#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "."

NoStrip = ["/opt/teamviewer/teamviewer/7/wine/drive_c/Program Files/TeamViewer/Version7/tvwine.dll.so"]

def setup():
    shelltools.system("rpm2targz -v %s/teamviewer_linux.rpm" %get.workDIR())
    shelltools.system("tar xfvz %s/teamviewer_linux.tar.gz --exclude=usr" %get.workDIR())
    shelltools.chmod("%s/opt/teamviewer/teamviewer/7/bin/*" %get.workDIR())

def install():
    pisitools.insinto("/opt/", "./opt/*")
    pisitools.dosym("/opt/teamviewer/teamviewer/7/bin/teamviewer", "/usr/bin/teamviewer")