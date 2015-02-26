#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools

def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    shelltools.cd("..")
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                   -DCMAKE_INSTALL_PREFIX=/usr \
                   -DCMAKE_SKIP_RPATH=ON \
                   -DCMAKE_INSTALL_LIBDIR=lib \
                   -DPHONON_BUILD_PHONON4QT5=ON")

def build():    
    cmaketools.make()

def install():
    cmaketools.install()

    #Also add symlink for qt-only applications
    #pisitools.dosym("%s/plugins/phonon_backend/phonon_vlc.so" % kde4.modulesdir, "%s/phonon_backend/libphonon_vlc.so" % qt4.plugindir)

    pisitools.dodoc("AUTHORS", "COPYING*")
