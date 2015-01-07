#!/usr/bin/python 

import os

def postInstall():
    if not os.path.isfile("/usr/lib/libudev.so.0"):
        os.mkdir("/usr/lib/opera/lib",0755)
        os.symlink("/usr/lib/libudev.so","/usr/lib/opera/lib/libudev.so.0")