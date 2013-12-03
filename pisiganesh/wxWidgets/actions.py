#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

# if pisi can't find source directory, see /var/pisi/wxWidgets/work/ and:
# WorkDir="wxWidgets-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    shelltools.export("CFLAGS", "%s -fPIC" % get.CFLAGS()) 
    shelltools.export("CXXFLAGS", "%s -fPIC" % get.CFLAGS())

    autotools.configure("--enable-unicode")  

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("wxWidgets")

# You can use these as variables, they will replace GUI values before build.
# Package Name : wxWidgets
# Version : 3.0.0
# Summary : Cross Platform GUI library

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
