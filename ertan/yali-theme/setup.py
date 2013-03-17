#!/usr/bin/env python
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install

THEME_DIR = "usr/share/yali/theme/pardus"

class Build(build):
    def run(self):
        build.run(self)

        self.mkpath(self.build_base)
        self.spawn(["rcc", "-binary", "data.qrc", "-o", "%s/data.rcc" % self.build_base])


class Install(install):
    def run(self):
        install.run(self)

        self.copy_file("build/data.rcc", os.path.join(self.root or "/", THEME_DIR))


setup(name="yali-theme-pardus",
      version= "2011.0.8",
      description="Pardus theme for YALI (Yet Another Linux Installer)",
      license="GNU GPL2",
      author="Pardus Developers",
      author_email="yali@pardus.org.tr",
      url="http://www.pardus.org.tr/eng/yali/",
      data_files=[("/%s" % THEME_DIR, ["style.qss"])],
      cmdclass = {'build': Build,
                  'install': Install})
