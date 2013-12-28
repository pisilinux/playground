#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools

WorkDir = "."


def install():
    pisitools.insinto("/usr/share/jes/","jes.jar")
    pisitools.insinto("/usr/share/pixmaps/","jes.png")
    pisitools.insinto("/usr/share/pixmaps/","jes.xpm")
    pisitools.dosym("/usr/share/jes/jes.sh", "/usr/bin/jes")
