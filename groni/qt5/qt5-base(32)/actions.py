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

import os

WorkDir = "qtbase-opensource-src-5.4.1"

qtbase = qt5.prefix
#absoluteWorkDir = "%s/%s" % (get.workDIR(), WorkDir)


def setup():
    filteredCFLAGS = get.CFLAGS().replace("-g3", "-g")
    filteredCXXFLAGS = get.CXXFLAGS().replace("-g3", "-g")

    vars = {"PISILINUX_CC" :       get.CC() + (" -m32" if get.buildTYPE() == "emul32" else ""),
            "PISILINUX_CXX":       get.CXX() + (" -m32" if get.buildTYPE() == "emul32" else ""),
            "PISILINUX_CFLAGS":    filteredCFLAGS + (" -m32" if get.buildTYPE() == "emul32" else ""),
            "PISILINUX_LDFLAGS":   get.LDFLAGS() + (" -m32" if get.buildTYPE() == "emul32" else "")}

    for k, v in vars.items():
        pisitools.dosed("mkspecs/common/g++-base.conf", k, v)
        #pisitools.dosed("mkspecs/common/g++-unix.conf", k, v)

    shelltools.export("CFLAGS", filteredCFLAGS)
    shelltools.export("CXXFLAGS", filteredCXXFLAGS)
    #check that dosed commands without releated patches
    pisitools.dosed("mkspecs/common/gcc-base-unix.conf", "\-Wl,\-rpath,")
    pisitools.dosed("mkspecs/common/gcc-base.conf", "\-O2", filteredCFLAGS)
    pisitools.dosed("mkspecs/common/gcc-base.conf", "^(QMAKE_LFLAGS\s+\+=)", r"\1 %s" % get.LDFLAGS())

    shelltools.system('sed -i "s|-O2|${CXXFLAGS}|" mkspecs/common/{g++,gcc}-base.conf')
    shelltools.system('sed -i "/^QMAKE_LFLAGS_RPATH/s| -Wl,-rpath,||g" mkspecs/common/gcc-base-unix.conf')
    shelltools.system('sed -i "/^QMAKE_LFLAGS\s/s|+=|+= ${LDFLAGS}|g" mkspecs/common/gcc-base.conf')

    pisitools.dosed("mkspecs/linux-g++-64/qmake.conf", "-m64", "-m32")
    shelltools.export("LDFLAGS", "-m32 %s" % get.LDFLAGS())
    autotools.rawConfigure("-v \
                   -confirm-license \
                   -opensource \
                   -no-pch \
                   -prefix /usr \
                   -datadir /usr/share/qt5 \
                   -libdir /usr/lib32/ \
                   -plugindir /usr/lib32/qt5/plugins \
                   -importdir /usr/lib32/qt5/imports \
                   -qt-zlib \
                   -qt-libjpeg \
                   -qt-libpng \
                   -qt-harfbuzz \
                   -system-sqlite \
                   -nomake tests \
                   -openssl-linked \
                   -nomake examples \
                   -nomake tools \
                   -optimized-qmake \
                   -no-rpath \
                   -no-strip \
                   -dbus-linked \
                   -no-openvg \
                   -no-sse2 \
                   -reduce-relocations \
                   -no-warnings-are-errors \
                   -no-use-gold-linker")
def build():
    #shelltools.export("LD_LIBRARY_PATH", "%s/lib:%s" % (get.curDIR(), get.ENV("LD_LIBRARY_PATH")))
    shelltools.export("LD_LIBRARY_PATH", "/lib:{LD_LIBRARY_PATH}")
    autotools.make()
    # Fix docs build when qt is not installed
    shelltools.system('sed -i "s|/usr/lib/qt/bin/qdoc|${QTDIR}/qtbase/bin/qdoc|g" qmake/Makefile.qmake-docs')
    #shelltools.system("find -name Makefile -exec sed -i "s|/usr/lib/qt/bin/qdoc|${QTDIR}/qtbase/bin/qdoc|g" {} +")
    shelltools.system('sed -i "s|/usr/lib/qt/bin/qhelpgenerator|${QTDIR}/qttools/bin/qhelpgenerator|g" qmake/Makefile.qmake-docs')
    #shelltools.system("find -name Makefile -exec sed -i "s|/usr/lib/qt/bin/qhelpgenerator|${QTDIR}/qttools/bin/qhelpgenerator|g" {} +")

def install():
    if get.buildTYPE() == "emul32":
        qt5.install("INSTALL_ROOT=%s32" % get.installDIR())
        shelltools.move("%s32/usr/lib32" % get.installDIR(), "%s/usr" % get.installDIR())

    # Drop QMAKE_PRL_BUILD_DIR because reference the build dir
    #pisitools.remove("/usr/lib/*.prl")

    # Fix wrong qmake path in pri file
    #shelltools.system('sed -i "s|${srcdir}/${_pkgfqn}/qtbase|/usr|" /usr/lib/qt5/mkspecs/modules/qt_lib_bootstrap_private.pri')

    mkspecPath = "%s/mkspecs" %  qt5.archdatadir

    for root, dirs, files in os.walk("%s%s" % (get.installDIR(),  qt5.archdatadir)):
        # Remove unnecessary spec files..
        if root.endswith(mkspecPath):
            for dir in dirs:
                if not dir.startswith("linux") and dir not in ["common","qws","features","default"]:
                    pisitools.removeDir(os.path.join(mkspecPath,dir))
        for name in files:
            if name.endswith(".prl"):
                pisitools.dosed(os.path.join(root, name), "^QMAKE_PRL_BUILD_DIR.*", "")

    pisitools.dodoc("LGPL_EXCEPTION.txt", "LICENSE.*")
