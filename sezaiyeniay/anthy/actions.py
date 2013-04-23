# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/old-licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools


def setup():
    autotools.configure("--prefix=/usr --sysconfdir=/etc --disable-static")
    
def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("COPYING","INSTALL","README","doc/*")
