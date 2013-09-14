#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    
    cmaketools.configure("-DCMAKE_BUILD_TYPE=release", installPrefix="/usr")

def build():
    cmaketools.make()

def install():
    shelltools.cd("src")
    pisitools.dosed("cmake_install.cmake", "/lib64","/lib")
    shelltools.cd("..")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("ChangeLog", "COPYING", "NEWS", "README")
