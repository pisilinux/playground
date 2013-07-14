#!/usr/bin/python
# -*- coding: iso-8859-9 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools

WorkDir = "jdownloader"

def install():
    pisitools.insinto("/usr/share/applications", "jdownloader.desktop")
    pisitools.insinto("/usr/share/pixmaps", "jdownloader.png")
    pisitools.insinto("/usr/bin", "jdownloader")