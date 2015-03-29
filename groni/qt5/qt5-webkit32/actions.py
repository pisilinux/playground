#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import qt5
from pisi.actionsapi import get

def setup():
    shelltools.system ("qmake-qt5 WebKit.pro -config\
                        -no-use-gold-linker")

    if get.buildTYPE() == "emul32":
        autotools.configure(" --bindir=/usr/bin32 \
                              --libexecdir=/usr/libexec32 \ ")

        shelltools.export("PKG_CONFIG_PATH", "/usr/lib32/pkgconfig")

def build():
    qt5.make()
    # Fix docs build when qt is not installed
    shelltools.system('sed -i "s|/usr/lib/qt/bin/qhelpgenerator|${QTDIR}/qttools/bin/qhelpgenerator|g" Source/Makefile.api')
    shelltools.system("find -name Makefile -exec sed -i 's|/usr/lib/qt/bin/qmlplugindump|${QTDIR}/qtdeclarative/bin/qmlplugindump|g' {} +")
def install():
    qt5.install("INSTALL_ROOT=%s" % get.installDIR())

    if get.buildTYPE() == "emul32":
        pisitools.removeDir("/usr/l32")
        pisitools.removeDir("/usr/libexec32")

    #pisitools.insinto("/usr/share/licenses/qt5-webkit/", "LGPL_EXCEPTION.txt")
