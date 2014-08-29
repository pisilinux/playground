#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

# if pisi can't find source directory, see /var/pisi/freemind/work/ and:
# WorkDir="freemind-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    shelltools.system("chmod +x check_for_duplicate_resources.sh")

def build():
    shelltools.export("JAVA_HOME","/opt/sun-jdk")
    shelltools.system("ant")

def install():
    shelltools.cd("..")
    shelltools.move("bin","freemind-"+ get.srcVERSION())
    pisitools.dodir("/opt")
    pisitools.insinto("/opt","freemind-"+ get.srcVERSION())
    

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("freemind")

# You can use these as variables, they will replace GUI values before build.
# Package Name : freemind
# Version : 1.0.0
# Summary : Mind Mapping tool

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
