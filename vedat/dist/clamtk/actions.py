#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

import os
import fnmatch
from pisi.actionsapi import pisitools
from pisi.actionsapi import get


def setup():
    pisitools.dosed("clamtk", "use ClamTk::Prefs", "use lib \"/usr/lib/\";\nuse ClamTk::Prefs")
    pisitools.dosed("clamtk", "use ClamTk::GUI", "use lib \"/usr/lib/\";\nuse ClamTk::GUI")
    pisitools.dosed("clamtk", "use ClamTk::Analysis", "use lib \"/usr/lib/\";\nuse ClamTk::Analysis")

def install():
    pisitools.dobin("clamtk")
    pisitools.dolib("lib/*", "/usr/lib/perl5/vendor_perl/"+ get.curPERL()+ "/ClamTk")
    pisitools.doman("clamtk.1.gz")
    
    pisitools.dosym("/usr/share/icons/oxygen/16x16/places/network-workgroup.png", "/usr/share/icons/oxygen/16x16/places/gtk-network.png")
    pisitools.dosym("/usr/share/icons/oxygen/22x22/places/network-workgroup.png", "/usr/share/icons/oxygen/22x22/places/gtk-network.png")
    pisitools.dosym("/usr/share/icons/oxygen/32x32/places/network-workgroup.png", "/usr/share/icons/oxygen/32x32/places/gtk-network.png")
    pisitools.dosym("/usr/share/icons/oxygen/48x48/places/network-workgroup.png", "/usr/share/icons/oxygen/48x48/places/gtk-network.png")
    pisitools.dosym("/usr/share/icons/oxygen/64x64/places/network-workgroup.png", "/usr/share/icons/oxygen/64x64/places/gtk-network.png")
    pisitools.dosym("/usr/share/icons/oxygen/128x128/places/network-workgroup.png", "/usr/share/icons/oxygen/128x128/places/gtk-network.png")
    pisitools.dosym("/usr/share/icons/oxygen/256x256/places/network-workgroup.png", "/usr/share/icons/oxygen/256x256/places/gtk-network.png")

    
    
    pisitools.dosym("/usr/share/icons/gnome/16x16/actions/gtk-new.png", "/usr/share/icons/oxygen/16x16/places/gtk-new.png")
    pisitools.dosym("/usr/share/icons/gnome/22x22/actions/gtk-new.png", "/usr/share/icons/oxygen/22x22/places/gtk-new.png")
    pisitools.dosym("/usr/share/icons/gnome/32x32/actions/gtk-new.png", "/usr/share/icons/oxygen/32x32/places/gtk-new.png")
    pisitools.dosym("/usr/share/icons/gnome/48x48/actions/gtk-new.png", "/usr/share/icons/oxygen/48x48/places/gtk-new.png")
    pisitools.dosym("/usr/share/icons/gnome/256x256/actions/gtk-new.png", "/usr/share/icons/oxygen/256x256/places/gtk-new.png")
    
    pisitools.insinto("/usr/share/applications", "clamtk.desktop")
    #pisitools.insinto("/usr/share/pixmaps", "clamtk.png")
    pisitools.dodoc("CHANGES", "DISCLAIMER", "LICENSE", "README")

    #Locales
    for i in os.listdir("po"):
        if fnmatch.fnmatch(i, '*.po'):
            pisitools.domo("po/" + i, i.replace(".po", ""), "clamtk.mo")
