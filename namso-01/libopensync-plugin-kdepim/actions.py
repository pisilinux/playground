#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
	pisitools.dosed("CMakeLists.txt", "Qt3", "Qt4")
	#pisitools.dosed("CMakeLists.txt", "KDEPIM3", "KDEPIM4")
	pisitools.dosed("cmake/modules/FindKDEPIM3.cmake", "3", "4")
	shelltools.makedirs("build")
	shelltools.cd("build")
	cmaketools.configure(sourceDir="..")


def build():
    shelltools.cd("build")
    cmaketools.make()

def install():
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
