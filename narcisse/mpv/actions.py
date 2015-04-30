#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pythonmodules
from pisi.actionsapi import get

shelltools.export("JOBS", get.makeJOBS().replace("-j", ""))

mjobs=get.makeJOBS().replace("-j", "")

def setup():       
    
    shelltools.system("./bootstrap.py")

    shelltools.system('./waf configure \
                       --prefix=/usr \
                       --confdir=/usr/share/mpv \
                       --datadir=/usr/share/mpv \
                       --libdir=/usr/lib \
                       --enable-libmpv-shared \
                       --disable-pdf-build \
                       --disable-test \
                       --disable-libguess \
                       --enable-lua \
                       --enable-encoding \
                       --enable-sdl2 \
                       --enable-pulse \
                       --enable-jack \
                       --enable-openal \
                       --enable-alsa \
                       --enable-wayland \
                       --enable-x11 \
                       --enable-xext \
                       --enable-xv \
                       --enable-xinerama \
                       --enable-gl-x11 \
                       --enable-egl-x11 \
                       --enable-gl-wayland \
                       --enable-gl \
                       --enable-vdpau \
                       --enable-vdpau-gl-x11 \
                       --enable-vaapi \
                       --enable-vaapi-glx \
                       --enable-jpeg \
                       --enable-vaapi-hwaccel \
                       --enable-vdpau-hwaccel \
                       ')


def build():
    shelltools.system("./waf build --jobs=%s" %mjobs)

def install():
    
    shelltools.system("./waf install --destdir=%s" %get.installDIR())

    pisitools.insinto("/etc/mpv", "etc/encoding-profiles.conf")
    
    pisitools.domove("/usr/share/mpv/*", "/usr/share")
    pisitools.removeDir("/usr/share/mpv")
    pisitools.remove("/usr/share/encoding-profiles.conf")

    # install docs, tools, examples
    pisitools.dodoc("Copyright", "LICENSE", "README.md")
    
