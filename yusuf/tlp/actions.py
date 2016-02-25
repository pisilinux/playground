#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def setup():
    shelltools.export("TLP_ULIB","/usr/lib/eudev")
    shelltools.export("TLP_NO_INIT","1")
    shelltools.export("TLP_NO_PMUTILS","1")
def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
