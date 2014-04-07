#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pisitools

def install():
    pisitools.insinto("/usr/share/applications/", "usr/share/applications/etakip.desktop")
    pisitools.insinto("/usr/share/java/e-takip/", "usr/share/java/e-takip/lib.jar")
    pisitools.insinto("/usr/share/java/e-takip/", "usr/share/java/e-takip/etakip.sh")
    pisitools.insinto("/usr/bin/", "usr/share/java/e-takip/etakip.sh")
    pisitools.insinto("/usr/share/pixmaps/", "usr/share/pixmaps/etakip.png")