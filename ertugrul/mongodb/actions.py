#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import scons
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

##NoStrip= "/"

def build():
    pisitools.ldflags.add("-lstdc++")

    scons.make("all \
                --use-system-boost \
                --use-system-pcre \
                --use-system-tcmalloc \
                --ssl \
                --sharedclient \
                --prefix=/usr \
                 DESTDIR=%s" % get.installDIR())

def install():
    scons.install("install \
                  --full --sharedclient \
                  --prefix=%s/usr" % get.installDIR())

    # remove static library
    pisitools.remove("/usr/lib64/libmongoclient.a")

    # needed directory
    pisitools.dodir("/var/lib/mongodb")
    pisitools.dodir("/var/log/mongodb")
    pisitools.dodir("/var/run/mongodb")

    # add man and documents
    pisitools.doman("debian/mongo*.1")
    pisitools.dodoc("README","docs/index.md","docs/building.md")
