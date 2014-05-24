#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/qtkeychain/work/ and:
# WorkDir="qtkeychain-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=release \
                          -DBUILD_WITH_QT4=on \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DCMAKE_INSTALL_LIBDIR=/usr/lib")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("qtkeychain")

# You can use these as variables, they will replace GUI values before build.
# Package Name : qtkeychain
# Version : 0.3.0
# Summary : Platform-independent Qt API for storing passwords securely.

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
