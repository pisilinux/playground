#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pythonmodules

pisitools.flags.sub("-O[\ds]+", "-O3")
WorkDir="mplayer-checkout-2014-10-26"
def setup():
#    for f in ["configure", "libmpdemux/demux_rtp.cpp", "libmpdemux/demux_rtp_internal.h"]:
#        pisitools.dosed(f, "([\"<])(liveMedia|BasicUsageEnvironment)(\.hh)([\">])", "\\1\\2/\\2\\3\\4")
#    pisitools.dosed("libmpdemux/demux_rtp.cpp", "GroupsockHelper.hh", "groupsock/GroupsockHelper.hh")
    shelltools.copytree("../ffmpeg-2.4.2", "ffmpeg")
    autotools.rawConfigure(' \
                            --prefix=/usr \
                            --enable-runtime-cpudetection \
                            --enable-gui \
                            --disable-arts \
                            --disable-liblzo \
                            --disable-speex \
                            --disable-openal \
                            --disable-libdv \
                            --disable-musepack \
                            --disable-esd \
                            --disable-mga \
                            --disable-ass-internal \
                            --disable-cdparanoia \
                            --enable-xvmc \
                            --enable-radio \
                            --enable-radio-capture \
                            --enable-smb \
                            --language=all \
                            --enable-ffmpeg_a \
                            --confdir=/etc/mplayer \
                            ')

                            # stuff that fail hede=yes check, but working with hede=auto
                            # do not use: autodetect is fine  --enable-cdparanoia and --enable-libcdio 
                            #  --enable-directfb \
                            #
                            #  not ready 
                            # --enable-live \
                            #
                            #   Maybe used
                            # --disable-ffmpeg_so \

def build():
    autotools.make()

def install():
    autotools.install("prefix=%(D)s/usr \
                       BINDIR=%(D)s/usr/bin \
                       LIBDIR=%(D)s/usr/lib \
                       CONFDIR=%(D)s/usr/share/mplayer \
                       DATADIR=%(D)s/usr/share/mplayer \
                       MANDIR=%(D)s/usr/share/man" % {"D": get.installDIR()})

    # set the default skin for gui
    shelltools.copytree("default_skin", "%s/usr/share/mplayer/skins/default" % get.installDIR())

    # codecs conf, not something user will interact with
    pisitools.insinto("/usr/share/mplayer", "etc/codecs.conf")

    # example dvb conf
    pisitools.insinto("/usr/share/mplayer", "etc/dvb-menu.conf")

    # just for fast access to conf
    pisitools.dosym("/etc/mplayer.conf", "/usr/share/mplayer/mplayer.conf")
    pisitools.dosym("/etc/mencoder.conf", "/usr/share/mplayer/mencoder.conf")

    # install docs, tools, examples
    pisitools.dodoc("AUTHORS", "Changelog", "README", "LICENSE")
    pisitools.insinto("/%s/%s/" % (get.docDIR(), get.srcNAME()), "TOOLS")
    pisitools.insinto("/%s/%s/" % (get.docDIR(), get.srcNAME()), "DOCS/tech")
    pythonmodules.fixCompiledPy("/usr/share/doc")
