#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools

def setup():
    
    #shelltools.system("sed -i 's/KF5Prison_DIR:PATH=KF5Prison_DIR-NOTFOUND/KF5Prison_DIR:PATH=\/usr\/lib\/cmake\/Prison/g' %s/kdepimlibs/akonadi-contact/CMakeLists.txt" % get.workDIR())
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
		          -DCMAKE_INSTALL_PREFIX=/usr \
		          -DCMAKE_SKIP_RPATH=ON \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
		          -DLIB_INSTALL_DIR=lib")
def build():
    cmaketools.make()

def install():
    cmaketools.install()

    pisitools.dodoc("README", "COPYING")
