#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."
def setup():
  
      shelltools.cd("flareget_2.0-15_x86_64(stable)_rpm")
      shelltools.system("rpm2targz flaremonitor-1.0-2.x86_64.rpm")
      shelltools.system("rpm2targz flareget-2.0-15.x86_64.rpm")
      shelltools.system("tar xfvz flaremonitor-1.0-2.x86_64.tar.gz")
      shelltools.system("tar xfvz flareget-2.0-15.x86_64.tar.gz")

def install():
    shelltools.cd("flareget_2.0-15_x86_64(stable)_rpm")
    pisitools.insinto("/lib/","./lib/*")
    pisitools.insinto("/usr/bin/","./usr/bin/*")
    pisitools.insinto("/usr/sbin/","./usr/sbin/*")
    pisitools.insinto("/usr/share/","./usr/share/*")
    pisitools.insinto("/usr/lib/","./usr/lib64/*")

