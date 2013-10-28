#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

import os


datadir = "/opt/utorrent-server-v3_0"

def fixperms(d):
    for root, dirs, files in os.walk(d):
        for name in dirs:
            shelltools.chmod(os.path.join(root, name), 0755)
        for name in files:
            shelltools.chmod(os.path.join(root, name), 0644)

def install():
    for dir in ["docs", "webui.zip","utserver"]:
        fixperms(dir)
        pisitools.insinto(datadir, dir)
    #pisitools.dosym("/opt/utorrent-server-v3_0/utserver","/usr/bin/utserver") 
    shelltools.cd("docs")
    pisitools.dodoc("Changes.txt", "license.txt")

