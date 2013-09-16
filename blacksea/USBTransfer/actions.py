#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir="."

def install():
     
    pisitools.insinto("/usr/share/USBTransfer", "./*.py")
    pisitools.insinto("/usr/share/USBTransfer", "lang")
    pisitools.insinto("/usr/share/USBTransfer", "qt")
    pisitools.insinto("/usr/share/USBTransfer", "ts")

