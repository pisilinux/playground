#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "polib-%s" % get.srcVERSION()

def setup():
    shelltools.makedirs("python3")
    shelltools.copytree("../polib-%s" % get.srcVERSION(), "%s/python3" % get.workDIR())
    pythonmodules.compile()
    shelltools.cd("%s/python3" % get.workDIR())
    pythonmodules.compile(pyVer = "3.4")
def install():    
    pythonmodules.install()
    shelltools.cd("%s/python3" % get.workDIR())
    pythonmodules.install(pyVer = "3.4")
