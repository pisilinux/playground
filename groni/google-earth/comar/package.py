#!/usr/bin/python

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    # If this driver-X86_64 in use is nvidia-current then set driver-32 after installation.
    if os.readlink("/etc/alternatives/libGL") == "/usr/lib/nvidia-current/libGL.so.1.2":
        os.system("/usr/sbin/alternatives --set libGL-32bit /usr/lib32/nvidia-current/libGL.so.1.2")
        os.system("/sbin/ldconfig -X")

    # If this driver-X86_64 in use is fglrx then set driver-32 after installation.
    if os.readlink("/etc/alternatives/libGL") == "/usr/lib/fglrx/libGL.so.1.2":
        os.system("/usr/sbin/alternatives --set libGL-32bit /usr/lib32/fglrx/libGL.so.1.2")
        os.system("/sbin/ldconfig -X")
