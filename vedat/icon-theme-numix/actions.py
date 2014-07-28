#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools

WorkDir = "./"

def install():
    pisitools.insinto("/usr/share/icons", "numix-icon-theme-circle-master/Numix-Circle")
    pisitools.insinto("/usr/share/icons", "numix-icon-theme-master/Numix")
    
    pisitools.dodoc("numix-icon-theme-circle-master/LICENSE", "numix-icon-theme-circle-master/README.md", "numix-icon-theme-master/LICENSE", "numix-icon-theme-master/README.md")
