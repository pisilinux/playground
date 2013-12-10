from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

WorkDir = "HotShots-2.0.0-src"

def setup():
    shelltools.cd("%s/HotShots-2.0.0-src/build" % get.workDIR())
    cmaketools.configure("-DCMAKE_BUILD_TYPE=release", installPrefix="/usr")

def build():
    shelltools.cd("%s/HotShots-2.0.0-src/build" % get.workDIR())
    cmaketools.make()

def install():
    shelltools.cd("%s/HotShots-2.0.0-src/build" % get.workDIR())
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())


# By PiSiDo 2.0.0
