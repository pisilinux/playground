# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools

def install():
    pythonmodules.install("--optimize=1",pyVer="3")

    #Use versioned binary to avoid python2 version.
    pisitools.remove("/usr/bin/easy_install")

