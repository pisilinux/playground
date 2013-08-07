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

    
    shelltools.copytree("%s/" % get.workDIR(), "%s/assaultcubereloaded" % installdir)
    pisitools.dosym("/usr/share/assaultcubereloaded/LinuxClient.sh", "/usr/bin/assaultcubereloaded")