#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pisitools

def install():
    pisitools.insinto("/usr/share/adeskbar", "src/*")
    pisitools.insinto("/usr/share/applications", "adeskbar.desktop")
    pisitools.insinto("/usr/bin/", "adeskbar.sh", "adeskbar")
    pisitools.insinto("/usr/share/pixmaps", "src/images/adeskbar.png")
    pisitools.dodoc("README")
    
    pisitools.domo("po/tr.po", "tr", "adeskbar.mo")
    pisitools.domove("/usr/share/locale/tr", "/usr/share/adeskbar/locale")
    pisitools.removeDir("/usr/share/locale")