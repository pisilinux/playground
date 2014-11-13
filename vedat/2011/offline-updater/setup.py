#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

appName = "offline-updater"


def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass

class Build(build):
    def run(self):
        # Clear all
        os.system("rm -rf build")
        # Copy codes
        print "Copying PYs..."
        os.system("cp -R src/ build/")
        # Copy compiled UIs and RCs
        print "Generating UIs..."
        for filename in glob.glob1("ui", "*.ui"):
            os.system("pyuic4 -o build/ui_%s.py ui/%s" % (filename.split(".")[0], filename))


class Install(install):
    def run(self):
        os.system("./setup.py build")
        if self.root:
            usr_dir = "%s/usr" % self.root
        else:
            usr_dir = "/usr"
        bin_dir = os.path.join(usr_dir, "bin")
        apps_dir = os.path.join(usr_dir, "share", appName)

        # Make directories
        print "Making directories..."
        makeDirs(bin_dir)
        makeDirs(apps_dir)

        # Install codes
        print "Installing codes..."
        os.system("cp -R build/* %s/" % apps_dir)


        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(apps_dir.replace(self.root, ""), "offline_mode.py"), os.path.join(bin_dir, "offline_mode"))
                os.symlink(os.path.join(apps_dir.replace(self.root, ""), "online_mode.py"), os.path.join(bin_dir, "online_mode"))
        except OSError:
            pass


setup(
      name              = "offline-updater",
      version           = "0.1",
      description       = "bisiler",
      author            = u"Cem Türker",
      author_email      = "cemturker@gmail.com",
      url               = "http://www.cemturker.net",
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'build': Build,
                            'install': Install,
                          }
)
