#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

# if pisi can't find source directory, see /var/pisi/flickrnet/work/ and:
# WorkDir="flickrnet-"+ get.srcVERSION() +"/sub_project_dir/"



def install():
        shelltools.cd("..")  
        pisitools.dodir("/usr")
        pisitools.insinto("/usr/lib","usr/lib/mono")
        pisitools.insinto("/usr/lib","usr/lib/pkgconfig")

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("flickrnet")

# You can use these as variables, they will replace GUI values before build.
# Package Name : flickrnet
# Version : 3.7.0
# Summary : The Flickr.Net API Library is a .Net Library for accessing the Flickr API.

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
