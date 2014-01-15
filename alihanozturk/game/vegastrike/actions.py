#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    pisitools.cxxflags.add("-fpermissive")
    shelltools.system("sed -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure.ac")
    autotools.configure("--prefix=/usr \
                         --disable-ffmpeg \
                         --with-boost=1.45 \
                         --with-data-dir=/usr/share/vegastrike")

def build():
    autotools.make()

    shelltools.cd("setup/src")

def install():
    autotools.install()

    pisitools.rename("/usr/bin/vegastrike", "vegastrike.bin")

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "DOCUMENTATION", "NEWS", "README", "*.txt")