#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import scons
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/MyPaint/work/ and:
# WorkDir="MyPaint-"+ get.srcVERSION() +"/sub_project_dir/"


def build():
    scons.make()

def install():
    scons.install()


# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("MyPaint")

# You can use these as variables, they will replace GUI values before build.
# Package Name : MyPaint
# Version : 1.1.0
# Summary : MyPaint is a fast and easy open-source graphics application for digital painters

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
