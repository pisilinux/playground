#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools

def build():
    pythonmodules.compile()

def install():
    pythonmodules.install()

    pisitools.dodoc("AUTHORS", "LICENSE")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("kivy")

# You can use these as variables, they will replace GUI values before build.
# Package Name : kivy
# Version : 1.8.0
# Summary : A software library for rapid development of hardware-accelerated multitouch applications.

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
