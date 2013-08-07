#!/usr/bin/python

import os
def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    perm_fixes = (
                ("/usr/lib/go/pkg/tool", 0755),
    )

    for path, mode in perm_fixes:
        if os.path.exists(path):
            os.chmod(path, mode)
    # If the go tool sees a package file timestamped older than a dependancy it
    # will rebuild that file. So, in order to stop go from rebuilding lots of
    # packages for every build we need to fix the timestamps. The compiler and
    # linker are also checked - so we need to fix them too.
    TREF = "/usr/lib/go/pkg/*/runtime.a"
    os.system("/usr/bin/find /usr/lib/go -type f -exec touch -r %s {} \;" % TREF)

