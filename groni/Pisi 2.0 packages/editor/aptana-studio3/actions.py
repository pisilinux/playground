#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

NoStrip = "/opt/Aptana_Studio_3"

def install():   
    pisitools.insinto("/opt/Aptana_Studio_3", "*")
    pisitools.insinto("/usr/share/pixmaps/", "icon.xpm")    
    
