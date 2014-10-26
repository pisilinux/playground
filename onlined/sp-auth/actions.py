#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def install():
    pisitools.doexe("sp-sc-auth","/usr/bin")
    pisitools.dosym("sp-sc-auth","/usr/bin/sp-auth")
    pisitools.dosym("sp-sc-auth","/usr/bin/sc-auth")
    pisitools.dosym("sp-sc-auth","/usr/bin/sopcast")
    pisitools.dodoc("Readme")