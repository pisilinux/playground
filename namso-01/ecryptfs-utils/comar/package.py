#!/usr/bin/python

import os, re

OUR_ID = 640
OUR_NAME = "ecryptfs"
OUR_DESC = "MDM"


for dirs in ("/usr/share/pixmaps/ecryptfs-mount-private.desktop", "/usr/share/pixmaps/ecryptfs-setup-private.desktop"):
    os.system("/bin/chmod -R 755 %s" % dirs)
    os.system("/bin/chmod +s 755 /usr/bin/mount.ecryptfs_private")
    os.system("/sbin/ldconfig authconfig --enableecryptfs --update")

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    try:
        os.system ("groupadd -r -f %s" % (OUR_ID, OUR_NAME))
        #os.system ("useradd -m -d /var/lib/mdm -r -s /bin/false -u %d -g %d %s -c %s" % (OUR_ID, OUR_ID, OUR_NAME, OUR_DESC))
    except:
        pass

def postRemove():
    try:
        #os.system ("userdel %s" % OUR_NAME)
        os.system ("groupdel %s" % OUR_NAME)
    except:
        pass