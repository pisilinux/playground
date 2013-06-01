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
    pisitools.flags("-fstack-protector -fasynchronous-unwind-tables -O.")
    shelltools.system("./autogen.sh")
    shelltools.makedirs("../grub-efi")
    shelltools.system("cp -ar ./* %s/grub-efi/" % get.workDIR())
    autotools.configure("--disable-werror \
                         --with-grubdir=grub2 \
                         --program-transform-name='s,grub,grub2,'\
                         --program-prefix='' \
                         --htmldir='/usr/share/doc/${PF}/html' \
                         --enable-mm-debug \
                         --enable-nls \
                         --enable-device-mapper \
                         --enable-cache-stats \
                         --enable-grub-mkfont \
                         --enable-grub-mount \
                         --%sable-efiemu" % "en" if get.ARCH() == "x86_64" else "dis")
    shelltools.cd("../grub-efi")
    autotools.configure("--with-platform='efi' \
                         --target='i386' \
                         --disable-efiemu \
                         --disable-werror \
                         --with-grubdir=grub2 \
                         --program-transform-name='s,grub,grub2,'\
                         --program-prefix='' \
                         --enable-mm-debug \
                         --enable-nls \
                         --enable-device-mapper \
                         --enable-cache-stats \
                         --enable-grub-mkfont \
                         --enable-grub-mount \
                         --htmldir='/usr/share/doc/${PF}/html' ")

def build():
    autotools.make()

    shelltools.cd("../grub-efi")
    autotools.make()

def install():
    # Install unicode.pf2 using downloaded font source. 
    shelltools.system("./grub-mkfont -o unicode.pf2 unifont.pcf.gz")

    # Create directory for grub.cfg file
    pisitools.dodir("/boot/grub2")
    pisitools.insinto("/boot/grub2", "unicode.pf2")

    # Insall our theme
    pisitools.insinto("/usr/share/grub/themes/","themes/pisilinux")

    #remove -r 0x0-0x7F entries to fix ugly fonts or find a suitable range parameter -r ***
    shelltools.system("./grub-mkfont -o DejaVuSans-10.pf2 -r 0x0-0x7F -s 10 /usr/share/fonts/dejavu/DejaVuSans.ttf")
    shelltools.system("./grub-mkfont -o DejaVuSans-12.pf2 -r 0x0-0x7F -s 12 /usr/share/fonts/dejavu/DejaVuSans.ttf")
    shelltools.system("./grub-mkfont -o DejaVuSans-14.pf2 -r 0x0-0x7F -s 14 /usr/share/fonts/dejavu/DejaVuSans.ttf")
    shelltools.system("./grub-mkfont -o DejaVuSans-16.pf2 -r 0x0-0x7F -s 16 /usr/share/fonts/dejavu/DejaVuSans.ttf")
    shelltools.system("./grub-mkfont -o DejaVuSans-Bold-14.pf2 -r 0x0-0x7F -s 14 /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf")
    shelltools.system("./grub-mkfont -o DejaVuSans-Mono-14.pf2 -r 0x0-0x7F -s 14 /usr/share/fonts/dejavu/DejaVuSansMono.ttf")
    shelltools.copy("ascii.pf2","%s/usr/share/grub/themes/pisilinux" % get.installDIR())

    # Do not install auto generated dejavu* fonts
    fonts=["DejaVuSans-10.pf2" , "DejaVuSans-12.pf2" , "DejaVuSans-14.pf2" , "DejaVuSans-16.pf2" , "DejaVuSans-Mono-14.pf2", "DejaVuSans-Bold-14.pf2"]
    for font in fonts:
        shelltools.copy(font,"%s/usr/share/grub/themes/pisilinux" % get.installDIR())

    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    #Remove default starfiled theme.
    pisitools.removeDir("/usr/share/grub/themes/starfield")

    pisitools.dodoc("ABOUT-NLS", "AUTHORS", "BUGS", "ChangeLog", "COPYING", "TODO", "README")

    shelltools.cd("../grub-efi")
    autotools.rawInstall("DESTDIR=%s-efi" % get.installDIR())
    for i in ["*.module", "*.image", "kernel.exec", "gdb_grub", "gmodule.pl"]:
        shelltools.system("rm -f %s-efi/usr/lib/grub/i386-efi/%s" % (get.installDIR(), i))
    shelltools.move("%s-efi/usr/lib/grub/i386-efi" % get.installDIR(), "%s/usr/lib/grub/i386-efi" % get.installDIR())
