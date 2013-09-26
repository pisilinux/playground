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
  
      shelltools.cd("flareget_2.1-18_x86_64(stable)_rpm")
      shelltools.system("rpm2targz flareget-2.1-18.x86_64.rpm")
      shelltools.system("tar xfvz flareget-2.1-18.x86_64.tar.gz")
      shelltools.cd("..")
      shelltools.cd("flareget_2.1-18_x86_64(stable)_rpm/Browser Integration/Opera(version < 13 only)")
      shelltools.system("rpm2targz flaremonitor-1.0-2.x86_64.rpm")
      shelltools.system("tar xfvz flaremonitor-1.0-2.x86_64.tar.gz")
      

def install():
      shelltools.cd("flareget_2.1-18_x86_64(stable)_rpm")
      pisitools.insinto("/usr/bin/","./usr/bin/*")
      pisitools.insinto("/usr/share/","./usr/share/*")
      pisitools.insinto("/usr/lib/","./usr/lib64/*")
      shelltools.cd("..")
      shelltools.cd("flareget_2.1-18_x86_64(stable)_rpm/Browser Integration/Opera(version < 13 only)")
      pisitools.insinto("/lib/","./lib/*")
      pisitools.insinto("/usr/sbin/","./usr/sbin/*")
      pisitools.insinto("/usr/share/","./usr/share/*")
     
      shelltools.chmod("%s/usr/bin/flare-grab" % get.installDIR(), 0755)
      shelltools.chown("%s/usr/bin/flare-grab" % get.installDIR(), gid="users")
      shelltools.chmod("%s/usr/bin/flareget" % get.installDIR(), 0755)
      shelltools.chown("%s/usr/bin/flareget" % get.installDIR(), gid="users")