import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    os.system("udevadm control --reload-rules")
