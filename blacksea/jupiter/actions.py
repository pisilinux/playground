#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

NoStrip = ["/usr/share/applications/jupiter.desktop"]


def install():
    pisitools.insinto("/etc/pm/", "./pm/*")
    pisitools.insinto("/usr/", "./usr/*")
    shelltools.chmod("%s/usr/bin/jupiter" % get.installDIR(), 0755)

