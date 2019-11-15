#!/usr/bin/python

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    os.system("/usr/sbin/alternatives \
               --install /usr/lib/libGL.so.1.2.0 libGL /usr/lib/mesa/libGL.so.1.2.0 80 \
               --slave /usr/lib/xorg/modules/volatile xorg-modules-volatile /var/empty")

    os.system("/usr/sbin/alternatives \
               --install /usr/lib/libEGL.so.1.0.0 libEGL /usr/lib/mesa/libEGL.so.1.0.0 80 \
               --slave /usr/lib/xorg/modules/volatile xorg-modules-volatile /var/empty")

    if not os.path.lexists("/usr/lib/libGL.so.1"):
        os.symlink("libGL.so.1.2.0", "/usr/lib/libGL.so.1")
        
    if not os.path.lexists("/usr/lib/libGL.so.1.2"):
        os.symlink("libGL.so.1.2.0", "/usr/lib/libGL.so.1.2")
        
	if not os.path.lexists("/usr/lib/libEGL.so.1.1.0"):
		os.symlink("libEGL.so.1.0.0", "/usr/lib/libEGL.so.1.1.0")
		
	if not os.path.lexists("/usr/lib/libEGL.so.1"):
		os.symlink("libEGL.so.1.0.0", "/usr/lib/libEGL.so.1")	
	
	if not os.path.lexists("/usr/lib/libEGL.so"):
		os.symlink("libEGL.so.1.0.0", "/usr/lib/libEGL.so")

def preRemove():
    # FIXME This is not needed when upgrading package; but pisi does not
    #       provide a way to learn operation type.
    #os.system("/usr/sbin/alternatives --remove libGL /usr/lib/mesa/libGL.so.1.2")
    pass

