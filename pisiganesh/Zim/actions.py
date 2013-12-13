#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

# if pisi can't find source directory, see /var/pisi/Zim/work/ and:
# WorkDir="Zim-"+ get.srcVERSION() +"/sub_project_dir/"

shelltools.export("XDG_DATA_HOME", get.workDIR())
shelltools.export("XDG_CONFIG_HOME", get.workDIR())
shelltools.export("XDG_DATA_DIRS", get.workDIR())

def build():
    pythonmodules.compile()

def install():
    pythonmodules.install()

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("Zim")

# You can use these as variables, they will replace GUI values before build.
# Package Name : Zim
# Version : 0.60
# Summary : Zim is a graphical text editor used to maintain a collection of wiki pages

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
