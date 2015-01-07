#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    shelltools.system("ar x chrome-remote-desktop_current_amd64.deb")
    shelltools.system("tar xfvz data.tar.gz")

def install():
    pisitools.insinto("/opt/", "./opt/*")
    pisitools.insinto("/usr/", "./usr/*")
    pisitools.insinto("/etc/", "./etc/*")
    shelltools.chmod("%s/opt/google/*" % get.installDIR(),0777)
