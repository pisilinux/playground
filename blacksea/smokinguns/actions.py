#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir="."
NoStrip = ["/"]
datadir = "/usr/share/"
  
def install():
    installdir = get.installDIR()+ datadir
    pisitools.dodir(datadir)
    pisitools.dodir("%s/applications" % datadir)
    
    shelltools.copytree("%s/Smokin' Guns 1.1" % get.workDIR(), "%s/smokinguns" % installdir)
    pisitools.dosym("/usr/share/smokinguns/smokinguns.x86_64", "/usr/bin/smokinguns")