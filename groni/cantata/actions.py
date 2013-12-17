#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/cantata/work/ and:
# WorkDir="cantata-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    cmaketools.configure("--DCMAKE_INSTALL_PREFIX=`kde4-config --prefix` -DCMAKE_BUILD_TYPE=Release")

def build():
    cmaketools.make()

def install():
    cmaketools.install()

# Take a look at the source folder for these file as documentation.
    pisitools.dodoc("AUTHORS", "LICENSE", "ChangeLog", "TODO", "INSTALL", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("cantata")

# You can use these as variables, they will replace GUI values before build.
# Package Name : cantata
# Version : 1.2.0
# Summary : A KDE client for the music player daemon (MPD)

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
