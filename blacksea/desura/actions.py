#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir="desura"
NoStrip = ["/"]

#def setup():
    
#def build():

    
def install():  
    pisitools.insinto("/opt/desura/", "desura", "desura")
    shelltools.chmod("%s/opt/desura/desura" % get.installDIR())
    shelltools.chown("%s/opt/desura/desura" % get.installDIR())