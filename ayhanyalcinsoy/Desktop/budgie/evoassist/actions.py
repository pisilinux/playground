#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def install():
    pisitools.insinto("/etc/dbus-1/", "data/system.d")
    pisitools.insinto("/usr/share", "data/polkit-1")
    pisitools.insinto("/usr/share", "data/dbus-1")

    pisitools.insinto("/usr/libexec", "src/backend.sh", "evoassist-wrapper")
    pisitools.insinto("/usr/libexec", "src/backend.py", "evoassist")

    pisitools.insinto("/usr/lib/evoassist", "src/evoassist.py")
    pisitools.insinto("/usr/lib/evoassist", "src/polkit_helper.py")

    pisitools.insinto("/usr/share/applications", "data/evoassist.desktop")

    pisitools.insinto("/usr/bin", "src/evoassist-ui.py", "evo-assist-ui")
    pisitools.chmod("%s/usr/bin/evo-assist-ui" % get.installDIR())

    pisitools.chmod("%s/usr/libexec/evoassist-wrapper" % get.installDIR())
    pisitools.chmod("%s/usr/libexec/evoassist" % get.installDIR())

    shelltools.system("chmod a+r -R %s/etc/dbus-1" % get.installDIR())
    shelltools.system("chmod a+r -R %s/usr/share" % get.installDIR())
 
