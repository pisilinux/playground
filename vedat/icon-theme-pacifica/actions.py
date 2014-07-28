#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "./"

def install():
    pisitools.insinto("/usr/share/icons", "pacifica-icon-theme-master/Pacifica")
    shelltools.chmod("%s/usr/share/icons/Pacifica/index.theme" % get.installDIR(), 0644)
    shelltools.chmod("%s/usr/share/icons/Pacifica/CREDITS" % get.installDIR(), 0644)
    
#    pisitools.dodoc("AUTHORS", "LICENSE")
