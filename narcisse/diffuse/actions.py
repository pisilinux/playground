#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.



from pisi.actionsapi import shelltools
from pisi.actionsapi import get


  
def install():
    
    shelltools.system("python install.py --prefix=/usr --destdir=%s" % get.installDIR())
    
   
    
   