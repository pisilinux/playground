#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.export("LINUX_BASE", "/proc")
    shelltools.export("LSOF_LDFLAGS", get.LDFLAGS())

    shelltools.touch(".neverInv")
    
    shelltools.system("tar -xvf lsof_4.88_src.tar")
    
    shelltools.cd("%s/lsof_4.88/lsof_4.88_src" % get.workDIR())
    shelltools.system("./Configure -n linux")

def build():
    shelltools.cd("%s/lsof_4.88/lsof_4.88_src" % get.workDIR())
    autotools.make()

def install():
    
    shelltools.cd("%s/lsof_4.88/lsof_4.88_src" % get.workDIR())
    pisitools.dodoc("00*")
    pisitools.dobin("lsof")
    pisitools.doman("lsof.8")
    pisitools.insinto("/usr/share/lsof/scripts", "%s/lsof_4.88/lsof_4.88_src/scripts/*" % get.workDIR())