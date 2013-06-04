#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def build():
    autotools.make()
    pisitools.dosed("primusrun", "LIB/libGL.so.1", "LIB/primus/libGL.so.1")

def install():
    pisitools.insinto("/usr/lib/primus", "lib/libGL.so.1")
    pisitools.insinto("etc/bash_completion.d", "primus.bash-completion", "primusrun")
    pisitools.dobin("primusrun")
    pisitools.doman("primusrun.1")

    pisitools.dodoc("LICENSE.txt")