#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir="mdic"

def setup():
    cmaketools.configure(sourceDir=".")
    pisitools.dosed("src/config/mdicconv.cpp", "local/bin/mdicconv", "bin/mdicconv")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.dodir("/usr/lib/mdic/dictionaries/")
    pisitools.dodoc("AUTHORS", "changelog", "COPYING", "README", "TODO")