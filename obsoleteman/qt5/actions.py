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

WorkDir = "qt-everywhere-opensource-src-%s" % get.srcVERSION().replace('_','-').replace('pre1', 'tp')

qtbase = qt5.prefix
absoluteWorkDir = "%s/%s" % (get.workDIR(), WorkDir)

def setup():
    #pisitools.flags.add("-I/usr/include/gtk-2.0/gdk")
    #make sure we don't use them
    
    
    #for d in ('libjpeg', 'freetype', 'libpng', 'zlib', "xcb", "sqlite"):
        #shelltools.unlinkDir("qtbase/src/3rdparty/%s" % d)

    filteredCFLAGS = get.CFLAGS().replace("-g3", "-g")
    filteredCXXFLAGS = get.CXXFLAGS().replace("-g3", "-g")

    vars = {"PISILINUX_CC" :       get.CC() + (" -m32" if get.buildTYPE() == "emul32" else ""),
            "PISILINUX_CXX":       get.CXX() + (" -m32" if get.buildTYPE() == "emul32" else ""),
            "PISILINUX_CFLAGS":    filteredCFLAGS + (" -m32" if get.buildTYPE() == "emul32" else ""),
            "PISILINUX_LDFLAGS":   get.LDFLAGS() + (" -m32" if get.buildTYPE() == "emul32" else "")}

    for k, v in vars.items():
        pisitools.dosed("qtbase/mkspecs/common/g++-base.conf", k, v)
        pisitools.dosed("qtbase/mkspecs/common/g++-unix.conf", k, v)

    shelltools.export("CFLAGS", filteredCFLAGS)
    shelltools.export("CXXFLAGS", filteredCXXFLAGS)
    #check that dosed commands without releated patches
    pisitools.dosed("qtbase/mkspecs/common/gcc-base-unix.conf", "\-Wl,\-rpath,")
    pisitools.dosed("qtbase/mkspecs/common/gcc-base.conf", "\-O2", filteredCFLAGS)
    pisitools.dosed("qtbase/mkspecs/common/gcc-base.conf", "^(QMAKE_LFLAGS\s+\+=)", r"\1 %s" % get.LDFLAGS())

    if not get.buildTYPE() == "emul32":
        #-no-pch makes build ccache-friendly
        options = "-v \
                   -no-pch \
                   -confirm-license \
                   -opensource \
                   -optimized-qmake \
                   -nomake tests \
                   -no-rpath \
                   -release \
                   -shared \
                   -accessibility \
                   -dbus-linked \
                   -fontconfig \
                   -glib \
                   -gtkstyle \
                   -icu \
                   -c++11 \
                   -system-harfbuzz \
                   -openssl-linked \
                   -system-libjpeg \
                   -system-libpng \
                   -system-sqlite \
                   -system-zlib \
                   -plugin-sql-sqlite \
                   -plugin-sql-odbc \
                   -plugin-sql-psql \
                   -plugin-sql-ibase \
                   -no-sql-tds \
                   -I/usr/include/firebird/ \
                   -I/usr/include/postgresql/server/ \
                   -no-separate-debug-info \
                   -no-strip \
                   -prefix %s \
                   -bindir %s \
                   -archdatadir %s\
                   -libdir %s \
                   -docdir %s \
                   -examplesdir %s \
                   -plugindir %s \
                   -translationdir %s \
                   -sysconfdir %s \
                   -datadir %s \
                   -importdir %s \
                   -headerdir %s \
                   -reduce-relocations" % (qt5.prefix, qt5.bindir, qt5.archdatadir, qt5.libdir, qt5.docdir, qt5.examplesdir, qt5.plugindir, qt5.translationdir, qt5.sysconfdir, qt5.datadir, qt5.importdir, qt5.headerdir)
    else:
        pisitools.dosed("qtbase/mkspecs/linux-g++-64/qmake.conf", "-m64", "-m32")
        shelltools.export("LDFLAGS", "-m32 %s" % get.LDFLAGS())
        options = "-no-pch \
                   -v \
                   -prefix /usr \
                   -libdir /usr/lib32 \
                   -plugindir /usr/lib32/qt5/plugins \
                   -importdir /usr/lib32/qt5/imports \
                   -datadir /usr/share/qt5 \
                   -translationdir /usr/share/qt5/translations \
                   -sysconfdir /etc \
                   -system-sqlite \
                   -c++11 \
                   -openssl-linked \
                   -nomake examples \
                   -nomake tools \
                   -optimized-qmake \
                   -no-rpath \
                   -no-strip \
                   -dbus-linked \
                   -no-sse2 \
                   -no-openvg \
                   -confirm-license \
                   -reduce-relocations  \
                   -opensource "

    autotools.rawConfigure(options)

def build():
    shelltools.export("LD_LIBRARY_PATH", "%s/lib:%s" % (get.curDIR(), get.ENV("LD_LIBRARY_PATH")))
    autotools.make()

def install():
    if get.buildTYPE() == "emul32":
        qt5.install("INSTALL_ROOT=%s32" % get.installDIR())
        shelltools.move("%s32/usr/lib32" % get.installDIR(), "%s/usr" % get.installDIR())
        return
    
    qt5.install("INSTALL_ROOT=%s" % get.installDIR())


    ##Remove phonon, we use KDE's phonon but we have to build Qt with Phonon support for webkit and some other stuff
    #pisitools.remove("%s/libphonon*" % qt5.libdir)
    #pisitools.removeDir("%s/phonon" % qt5.includedir)
    #if shelltools.isDirectory("%s/%s/phonon_backend" % (get.installDIR(), qt5.plugindir)):
        #pisitools.removeDir("%s/phonon_backend" % qt5.plugindir)
    #pisitools.remove("%s/pkgconfig/phonon*" % qt5.libdir)
    ## Phonon 4.5 provides libphononwidgets.so file
    #pisitools.remove("%s/designer/libphononwidgets.so" % qt5.plugindir)

    ##Remove lost /usr/tests directory
    #pisitools.removeDir("usr/tests")

    # Turkish translations
    #shelltools.export("LD_LIBRARY_PATH", "%s%s" % (get.installDIR(), qt5.libdir))
    #shelltools.system("%s%s/lrelease l10n-tr/*.ts" % (get.installDIR(), qt5.bindir))
    #pisitools.insinto(qt5.translationdir, "l10n-tr/*.qm")

    # Fix all occurances of WorkDir in pc files
    pisitools.dosed("%s%s/pkgconfig/*.pc" % (get.installDIR(), qt5.libdir), "%s/qt-x11-opensource-src-%s" % (get.workDIR(), get.srcVERSION()), qt5.prefix)

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

    ## Remove useless image directory, images of HTML docs are in doc/html/images
    #pisitools.removeDir("%s/src" % qt5.docdir)
    pisitools.dodoc("LGPL_EXCEPTION.txt", "LICENSE.*")
