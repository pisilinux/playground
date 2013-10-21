#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
import os

WorkDir="finalterm-master"

#def setup():
   # shelltools.makedirs("%s/build" % get.workDIR())
    #shelltools.cd("%s/build" % get.workDIR())
    #cmaketools.configure("-DCMAKE_BUILD_TYPE=release", installPrefix="/usr")
    
def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr" ,sourceDir = "..")
                          

def build():
    shelltools.cd("build")
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "NEWS", "README")
