#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

WorkDir = "eigen-eigen-6e7488e20373"

def setup():
    shelltools.makedirs("%s/%s/build_dir" % (get.workDIR(),WorkDir))
    shelltools.cd("%s/%s/build_dir" % (get.workDIR(),WorkDir))
    cmaketools.configure(sourceDir = "..")

def install():
    shelltools.cd("%s/%s/build_dir" % (get.workDIR(),WorkDir))
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.remove("/usr/include/eigen3/Eigen/src/Sparse/SparseAssign.h")
