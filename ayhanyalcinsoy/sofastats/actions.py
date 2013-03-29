#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("HOME", get.workDIR())

def setup():
    shelltools.system("./INSTALL.sh")

def build():
    autotools.system("./INSTALL.sh")

def install():
    autotools.install()
    pisitools.dodir("/usr/share/sofastats")
    pisitools.insinto("/usr/share/sofastats")
    pisitools.doins("sofa_main/*")
    pisitools.exeinto("/usr/share/sofastats")
    pisitools.doexe("sofa_main/*.py*")
    pisitools.doexe("sofa_main/*/*.py*")
    pisitools.dosym("/usr/share/sofastats/start.py /usr/bin/sofastats")
#    make_desktop_entry sofastats ${PN} /usr/share/sofastats/images/sofa_32x32.ico "Science;"
#    pisitools.dodoc("AUTHORS", "COPYING", "README")
