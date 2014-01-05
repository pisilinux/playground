#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

#shelltools.export("JOBS", get.makeJOBS().replace("-j", ""))
shelltools.export("ALT_PARALLEL_COMPILE_JOBS", "-j")
shelltools.export("HOTSPOT_BUILD_JOBS", "-j")
shelltools.export("LC_ALL", "C")

def setup():
    shelltools.system("./configure \
                       --disable-tests \
                       --disable-Werror \
                       --disable-downloading \
                       --with-parallel-jobs=-j \
                       --with-jdk-home=/opt/sun-jdk \
                       --enable-pulse-java \
                       --enable-nss \
                       --with-rhino \
                       --disable-bootstrap \
                       --with-jdk-src-zip=7958751eb9ef.tar.gz \
                       --with-jaxp-src-zip=8f220f7b51c7.tar.gz \
                       --with-corba-src-zip=8ed5df839fbc.tar.gz \
                       --with-jaxws-src-zip=652eb396f959.tar.gz  \
                       --with-openjdk-src-zip=e2f5917da3c1.tar.gz \
                       --with-hotspot-src-zip=b59e02d9e72b.tar.gz  \
                       --with-langtools-src-zip=3c8eb52a32ea.tar.gz \
                       --with-abs-install-dir=/usr/lib/jvm/java-7-openjdk \
                       --with-pkgversion='PisiLinux build 7.u45_2.4.3-1' ")

def build():
    autotools.make()
    
def check():
    autotools.check()

def install():
    autotools.rawInstall('DESTDIR=%s' % get.installDIR())

    pisitools.dodoc("AUTHORS", "THANKS", "COPYING", "README", "NEWS", "TODO")
