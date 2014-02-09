#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import shelltools

def build():
    shelltools.system("sed -i -e '357s/true/false/' usr/share/glib-2.0/schemas/com.linuxmint.mintmenu.gschema.xml")

def install():
    shelltools.cd("usr/lib/linuxmint/mintMenu")
    shelltools.system("./compile.py")
