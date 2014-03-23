#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
import platform
import os
import re

OUR_ID = 1000
OUR_NAME = "realtime"


def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    try:
        os.system ("groupadd -g %d %s" % (OUR_ID, OUR_NAME))
    except:
        pass
    
    fileassociations = open("/etc/security/limits.conf","a")
    fileassociations.write("*               -       rtprio          0;\n")
    fileassociations.write("*               -       nice            0;\n")
    fileassociations.write("@audio          -       rtprio          65;\n")
    fileassociations.write("@audio          -       nice           -10;\n")
    fileassociations.write("@audio          -       memlock         40000;\n")
    fileassociations.close()
    
    fileassociations = open("/etc/security/limits.d/99-jack.conf","a")
    fileassociations.write("@audio      - rtprio        99;\n")
    fileassociations.write("@audio      - memlock       unlimited;\n")
    fileassociations.close()
    

def postRemove():
    try:
        os.system ("groupdel %s" % OUR_NAME)
    except:
        pass

    



