#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/libdbi-drivers/work/ and:
#WorkDir="libdbi-drivers-"+ get.srcVERSION()+ libdbi-drivers-0.9.0

def setup():
    
    shelltools.system("tar zxvf %s/libdbi-drivers-0.9.0.tar.gz" % get.workDIR())
    shelltools.cd("%s/libdbi-drivers-0.9.0/" % get.workDIR()) 
    autotools.configure()
    shelltools.system("sh ./autogen.sh --prefix=/usr")
    #autotools.autoreconf("-vfi")
    
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("libdbi-drivers")

# You can use these as variables, they will replace GUI values before build.
# Package Name : libdbi-drivers
# Version : 0.9.0
# Summary : libdbi implements a database-independent abstraction layer in C, similar to the DBI/DBD layer in Perl.

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
