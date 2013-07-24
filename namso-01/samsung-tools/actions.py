#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def install():
    pisitools.dosed("samsung-tools.py", "/usr/bin/python2", "/usr/bin/python")
    pisitools.dosed("samsung-tools-preferences.py", "/usr/bin/python2", "/usr/bin/python")
    pisitools.dosed("session-service.py", "/usr/bin/python2", "/usr/bin/python")
    pisitools.dosed("system-service.py", "/usr/bin/python2", "/usr/bin/python")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("ChangeLog", "LICENSE", "README", "TODO")