#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/qutiM/work/ and:
# WorkDir="qutiM-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
            -DQRCICONS=0 \
            -DQMLCHAT:BOOL=0 \
            -DKINETICPOPUPS:BOOL=0 \
            -DASTRAL:BOOL=0 \
            -DPLUGMAN:BOOL=0 \
            -DSCRIPTAPI:BOOL=0 \
            -DSTACKEDCHATFORM:BOOL=0 \
            -DMOBILEABOUT:BOOL=0 \
            -DKINETICSCROLLER:BOOL=0 \
            -DWEBKITSTYLE/MAEMO:BOOL=0 \
            -DMOBILECONTACTINFO:BOOL=0 \
            -DMOBILESETTINGSDIALOG:BOOL=0 \
            -DDECLARATIVE_UI:BOOL=0 \
            -DSYMBIANINTEGRATION:BOOL=0 \
            -DMACINTEGRATION:BOOL=0 \
            -DMAEMO5INTEGRATION:BOOL=0 \
            -DMEEGOINTEGRATION:BOOL=0 \
            -DMULTIMEDIABACKEND:BOOL=0 \
            -DANTIBOSS:BOOL=0 \
            -DWININTEGRATION:BOOL=0 \
            -DVIDROBACKEND:BOOL=0 \
	    	-DSYSTEM_JREEN:BOOL=1 \
            -DCMAKE_INSTALL_PREFIX=/usr", installPrefix="/usr")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("qutiM")

# You can use these as variables, they will replace GUI values before build.
# Package Name : qutiM
# Version : 0.3.1
# Summary : qutIM is free and open-source multiprotocol instant messenger

# For more information, you can look at the Actions API
# from the Help menu and toolbar.

# By PiSiDo 2.0.0
