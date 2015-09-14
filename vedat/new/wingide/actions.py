#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get


def setup():
  
    pythonmodules.run("wing-install.py  --install-binary \
                                        --winghome '%s/opt/wingide' \
                                        --bin-dir %s/usr/bin " % (get.workDIR(), get.workDIR()))
    shelltools.system("sed -i 's|\/var\/pisi\/wing-5.1.7-1\/work\/opt\/wingide|\/opt\/wingide|' %s/opt/wingide/wing-101" % get.workDIR())
 
def install():
  
   
   pisitools.insinto("/usr/bin/", "%s/usr/bin/wing-101-5.1" % get.workDIR(), "wing" )
   pisitools.insinto("/opt", "%s/opt/*" % get.workDIR())
   
   pisitools.dodoc("%s/opt/wingide/LICENSE.txt" % get.workDIR())
   
   #pisitools.dodoc("LICENSE.txt", "VERSION", "CHANGELOG.txt")