#!/usr/bin/python

# Created For PisiLinux

from pisi.actionsapi import shelltools, get, pisitools

WorkDir = "."


def install():
    shelltools.system("rpm2targz brdcp7030lpr-2.0.2-1.i386.rpm")
    shelltools.system("tar -zxvf brdcp7030lpr-2.0.2-1.i386.tar.gz")
    pisitools.insinto("/", "usr")
    shelltools.system("rm -rf *")
