#!/usr/bin/python

# Created For PisiLinux

from pisi.actionsapi import shelltools, get, pisitools

WorkDir = "."

def install():
    shelltools.system("rpm2targz megasync-openSUSE_13.1.x86_64.rpm")
    shelltools.system("tar -zxvf megasync-openSUSE_13.1.x86_64.tar.gz")
    pisitools.insinto("/", "usr")
    shelltools.system("rm -rf *")
