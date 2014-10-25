#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import qt4
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools

maindir = "Heimdall-1.4.1"

def setup():
	for i in ["libpit","heimdall"]:
		shelltools.cd("%s/%s/%s" % (get.workDIR(),maindir,i))
		autotools.configure()
	shelltools.cd("%s/%s/heimdall-frontend" % (get.workDIR(),maindir))
	qt4.configure(parameters='OUTPUTDIR=%s/usr/bin' % get.installDIR())
	
def build():
	for i in ["libpit","heimdall","heimdall-frontend"]:
		shelltools.cd("%s/%s/%s" % (get.workDIR(),maindir,i))
		autotools.make()
	
def install():
    for i in ["heimdall","heimdall-frontend"]:
	    shelltools.cd("%s/%s/%s" % (get.workDIR(),maindir,i))
	    autotools.install()
    pisitools.domove("/usr/lib/udev/rules.d/60-heimdall.rules","/lib/udev/rules.d")
    pisitools.removeDir("/usr/lib")
