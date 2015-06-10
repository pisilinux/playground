#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

#pisitools.dosed("%s/calamares-master/src/modules/partition/tests/PartitionJobTests.cpp" % get.workDIR(), "Xfs", "Ext4" )

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Debug \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DWITH_PARTITIONMANAGER=1 \
                          -DCMAKE_INSTALL_LIBDIR=lib")
   

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
