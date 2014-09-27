#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get


def install():
    #shelltools.echo("/etc/bash/bashrc" , "screenfetch-dev")
    pisitools.insinto("/usr/bin","screenfetch-dev.sh","screenfetch-dev")
