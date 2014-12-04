#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
import os
# if pisi can't find source directory, see /var/pisi/ipython3/work/ and:
# WorkDir="ipython3-"+ get.srcVERSION() +"/sub_project_dir/"

def build():
    pythonmodules.compile(pyVer="3")

def install():
    pythonmodules.install(pyVer="3")
    print os.getcwd()
    pisitools.remove("/usr/bin/ipython")
    
# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("ipython3")

# You can use these as variables, they will replace GUI values before build.
# Package Name : ipython3
# Version : 2.3.1
# Summary : An enhanced interactive Python3 shell

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
