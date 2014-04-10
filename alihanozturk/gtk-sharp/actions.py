#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("LC_ALL", "C")

def build():
    shelltools.export("MONO_SHARED_DIR", get.workDIR())
    shelltools.system("./bootstrap-2.12 --prefix=/usr --sysconfdir=/etc --disable-static")
    autotools.make()

def install():
    shelltools.export("MONO_SHARED_DIR", get.workDIR())
    autotools.install()
