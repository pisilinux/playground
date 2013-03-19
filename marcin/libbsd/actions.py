#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
# See https://aur.archlinux.org/packages.php?ID=47112

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

def build():
    autotools.make("exec_prefix=/usr \
                    includedir=/usr/include/libbsd")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

# solve conflict with elfutils and glibc-devel
    pisitools.remove("/usr/include/nlist.h")
    pisitools.remove("/usr/lib/libbsd.a")

    pisitools.dodoc("ChangeLog", "COPYING", "README", "TODO", "Versions")

# By PiSiDo 2.0.0
