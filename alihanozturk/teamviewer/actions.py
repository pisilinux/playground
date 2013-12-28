#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "."

def setup():
    shelltools.system("rpm2targz -v %s/teamviewer_linux.rpm" %get.workDIR())
    shelltools.system("tar xfvz %s/teamviewer_linux.tar.gz --exclude=usr" %get.workDIR())
    shelltools.chmod("%s/opt/teamviewer9/tv_bin/" %get.workDIR())

def install():
    pisitools.insinto("/etc/", "./etc/*")
    pisitools.insinto("/opt/", "./opt/*")
    pisitools.insinto("/var/", "./var/*")
    pisitools.dosym("/opt/teamviewer9/tv_bin/script/teamviewerd.service", "/usr/lib/systemd/system/teamviewerd.service")
    pisitools.dosym("/opt/teamviewer9/tv_bin/script/teamviewer", "/usr/bin/teamviewer")