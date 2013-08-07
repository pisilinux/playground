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
    shelltools.copytree("%s/ supertuxkart-0.8-lin64" % get.workDIR(), "%s/supertuxkart" % installdir)
    pisitools.dosym("/usr/share/supertuxkart/supertuxkart", "/usr/bin/supertuxkart")

