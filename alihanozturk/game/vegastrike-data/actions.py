#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

import os

WorkDir = "vegastrike-data-0.5.1.r1"
NoStrip = "/"
datadir = "/usr/share/vegastrike"

def fixperms(d):
    for root, dirs, files in os.walk(d):
        for name in dirs:
            shelltools.chmod(os.path.join(root, name), 0755)
        for name in files:
            shelltools.chmod(os.path.join(root, name), 0644)

def install():
    for files in ("*.xml", "*.cur", "*.config", "New_Game"):
        pisitools.insinto(datadir, files)

    for data in os.listdir("."):
        fixperms(data)

        if os.path.isdir(data):
            if data not in ("bin"):
                shelltools.copytree(data, "%s%s" % (get.installDIR(), datadir))

    pisitools.doman("documentation/*.1")
    pisitools.dohtml("documentation/fixers_howto.html")
    pisitools.dodoc("*.txt", "documentation/*.txt", "documentation/Vega_Strike_Players_Guide.pdf")