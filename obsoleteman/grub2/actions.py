#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

def setup():
    shelltools.copy("../unifont*.pcf.gz", "./unifont.pcf.gz")
    shelltools.export("GRUB_CONTRIB", "%s/grub-%s/grub-extras" % (get.workDIR(), get.srcVERSION()))
    CFLAGS = get.CFLAGS().replace(" -fstack-protector","").replace(" -fasynchronous-unwind-tables","").replace(" -O2", "")
    shelltools.export("CFLAGS", CFLAGS)
    shelltools.system("./autogen.sh")
    autotools.configure("--disable-werror \
                         --with-grubdir=grub2 \
                         --program-transform-name='s,grub,grub2,'\
                         --program-prefix= \
                         --htmldir='/usr/share/doc/${PF}/html' ")

def build():
    autotools.make("dist")
    autotools.make()
    

def install():
    # Install unicode.pf2 using downloaded font source. 
    shelltools.system("./grub-mkfont -o unicode.pf2 unifont.pcf.gz")
     
    # Create directory for grub.cfg file
    pisitools.dodir("/boot/grub2")
    
    # Insall our theme
    pisitools.insinto("/usr/share/grub/themes/","themes/pisilinux")
    
    shelltools.system("./grub-mkfont -o %s/usr/share/grub/themes/pisilinux/DejaVuSans-10.pf2  -s 10 /usr/share/fonts/dejavu/DejaVuSans.ttf" % get.installDIR()) 
    shelltools.system("./grub-mkfont -o %s/usr/share/grub/themes/pisilinux/DejaVuSans-12.pf2  -s 12 /usr/share/fonts/dejavu/DejaVuSans.ttf" % get.installDIR()) 
    shelltools.system("./grub-mkfont -o %s/usr/share/grub/themes/pisilinux/DejaVuSans-14.pf2  -s 14 /usr/share/fonts/dejavu/DejaVuSans.ttf" % get.installDIR())
    shelltools.system("./grub-mkfont -o %s/usr/share/grub/themes/pisilinux/DejaVuSans-16.pf2  -s 16 /usr/share/fonts/dejavu/DejaVuSans.ttf" % get.installDIR()) 
    shelltools.system("./grub-mkfont -o %s/usr/share/grub/themes/pisilinux/DejaVuSans-Bold-14.pf2   -s 14 /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf" % get.installDIR()) 
    shelltools.copy("ascii.pf2","%s/usr/share/grub/themes/pisilinux" % get.installDIR())

    #TODO
    # Try to install Dejavu fonts also into /usr/share/grub/fonts to use in another themes
    # Do not install auto generated dejavu* fonts
    #fonts=["DejaVuSans-10.pf2" , "DejaVuSans-12.pf2" , "DejaVuSans-14.pf2" , "DejaVuSans-16.pf2" , "DejaVuSans-Bold-14.pf2"]
    
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    #Remove default starfiled theme.
    pisitools.removeDir("/usr/share/grub/themes/starfield")
    
    pisitools.dodoc("ABOUT-NLS", "AUTHORS", "BUGS", "ChangeLog", "COPYING", "TODO", "README")

