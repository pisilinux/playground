#!/usr/bin/env python
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
import os
import glob
import shutil
from PyQt4 import pyqtconfig
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.spawn import find_executable, spawn

I18N_DOMAIN = "yali"
I18N_LANGUAGES = ["tr", "nl", "it", "fr", "de", "pt_BR", "es", "pl", "ca", "sv", "hu", "ru"]

def qt_ui_files():
    ui_files = "yali/gui/Ui/*.ui"
    return glob.glob(ui_files)

def py_file_name(ui_file):
    return os.path.splitext(ui_file)[0] + '.py'

class YaliBuild(build):
    def changeQRCPath(self, ui_file):
        py_file = py_file_name(ui_file)
        lines = open(py_file, "r").readlines()
        replaced = open(py_file, "w")
        for line in lines:
            if line.find("data_rc") != -1:
                continue
            replaced.write(line)

    def compileUI(self, ui_file):
        pyqt_configuration = pyqtconfig.Configuration()
        pyuic_exe = find_executable('pyuic4', pyqt_configuration.default_bin_dir)
        if not pyuic_exe:
            pyuic_exe = find_executable('pyuic4')

        cmd = [pyuic_exe, ui_file, '-o']
        cmd.append(py_file_name(ui_file))
        cmd.append("-g \"yali\"")
        os.system(' '.join(cmd))

    def run(self):
        for ui_file in qt_ui_files():
            print ui_file
            self.compileUI(ui_file)
            self.changeQRCPath(ui_file)
        build.run(self)

class YaliClean(clean):

    def run(self):
        clean.run(self)

        for ui_file in qt_ui_files():
            ui_file = py_file_name(ui_file)
            if os.path.exists(ui_file):
                os.unlink(ui_file)

        if os.path.exists("build"):
            shutil.rmtree("build")

class YaliUninstall(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        yali_dir = os.path.join(get_python_lib(), "yali")
        if os.path.exists(yali_dir):
            print "removing: ", yali_dir
            shutil.rmtree(yali_dir)

        conf_dir = "/etc/yali"
        if os.path.exists(conf_dir):
            print "removing: ", conf_dir
            shutil.rmtree(conf_dir)
        os.unlink("/usr/bin/yali-bin")
        os.unlink("/usr/bin/start-yali")
        os.unlink("/usr/bin/bindYali")
        os.unlink("/lib/udev/rules.d/70-yali.rules")


class I18nInstall(install):
    def run(self):
        install.run(self)
        for lang in I18N_LANGUAGES:
            print "Installing '%s' translations..." % lang
            os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            if not self.root:
                self.root = "/"
            destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
            try:
                os.makedirs(destpath)
            except:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % I18N_DOMAIN))

setup(name="yali",
      version= "2.4.0",
      description="YALI (Yet Another Linux Installer)",
      long_description="Pardus System Installer.",
      license="GNU GPL2",
      author="Pardus Developers",
      author_email="yali@pardus.org.tr",
      url="http://www.pardus.org.tr/eng/yali/",
      packages = ['yali', 'yali.gui', 'yali.gui.Ui', 'yali.storage',\
                  'yali.storage.devices', 'yali.storage.formats', 'yali.storage.library'],
      data_files = [('/etc/yali', glob.glob("data/yali.conf")),
                    ('/lib/udev/rules.d', ["data/70-yali.rules"])],
      scripts = ['yali-bin', 'start-yali', 'scripts/bindYali'],
      ext_modules = [Extension('yali._sysutils',
                               sources = ['yali/_sysutils.c'],
                               libraries = ["ext2fs"],
                               extra_compile_args = ['-Wall'])],
      cmdclass = {
        'build' : YaliBuild,
        'clean' : YaliClean,
        'install': I18nInstall,
        'uninstall': YaliUninstall
        }
    )
