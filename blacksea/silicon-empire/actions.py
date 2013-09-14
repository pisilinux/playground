#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "silicon-empire"

def setup():
    shelltools.cd("src")
    cmaketools.configure()
                                      
      
def build():
    shelltools.cd("src")
    cmaketools.make()

def install():
    shelltools.cd("src")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.chmod("%s/usr/bin/silicon" % get.installDIR(), 0755)
    shelltools.cd("..")
    pisitools.dodoc("README","COPYING","Authors")
    