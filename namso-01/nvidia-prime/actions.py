#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    pisitools.dosed("prime-indicator.desktop", "Hidden=false", "Hidden=false\nIcon=nvidia")

def install():
    pisitools.insinto("/usr/lib/primeindicator/", "igpuon")
    pisitools.insinto("/usr/lib/primeindicator/", "dgpuon")
    pisitools.insinto("/usr/lib/primeindicator/", "*.png")
    pisitools.insinto("/usr/share/applications", "prime-indicator.desktop")
    pisitools.insinto("/etc/xdg/autostart/", "prime-indicator.desktop")
    pisitools.insinto("/usr/bin/", "prime-indicator")
    pisitools.insinto("/etc/sudoers.d/", "prime-indicator-sudoers")
    
    pisitools.dopixmaps("nvidia.png")
    
    pisitools.dodoc("LICENSE", "README*")