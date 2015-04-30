#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt 


from pisi.actionsapi import pisitools


def install():
    pisitools.dosed("lib/pkgconfig/libspotify.pc", "PKG_PREFIX", "/usr")
  
    pisitools.insinto("/usr/lib", "lib/*")
    pisitools.insinto("/usr/include", "include/*")
    pisitools.insinto("/usr/share/doc", "share/doc/*")
    pisitools.insinto("/usr/share/man/man3", "share/man3/*")
    
    

    pisitools.dodoc("ChangeLog", "LICENSE", "README")

