#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    pisitools.dosed("include/dos_inc.h","e DOSBOX_DOS_INC_H","e DOSBOX_DOS_INC_H\n#include <stddef.h>")
    autotools.configure()

def build():
    autotools.make()
    
def install():
    pisitools.dodoc("README","THANKS","NEWS","COPYING","ChangeLog","AUTHORS","docs/README.video","docs/PORTING")
    pisitools.doman("docs/dosbox.1")
    pisitools.doexe("src/dosbox","/usr/bin")