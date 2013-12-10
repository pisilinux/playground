#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/Rstudio/work/ and:
# WorkDir="Rstudio-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=release \
                          -DRSTUDIO_TARGET=Desktop \
                          -DQT_QMAKE_EXECUTABLE=/usr/lib/qt4/bin/qmake \
                          -DCMAKE_INSTALL_PREFIX=/usr/lib/rstudio",  installPrefix="/usr")
def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# By PiSiDo 2.0.0
