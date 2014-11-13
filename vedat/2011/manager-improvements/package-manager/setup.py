#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import glob
import shutil
import tempfile

from src import about

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.install import install

PROJECT = about.appName

def makeDirs(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

def remove(path):
    if os.path.exists(path):
        print ' removing: ', path
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

def update_messages():
    files = tempfile.mkstemp()[1]

    # Collect UI files
    filelist = []
    for filename in glob.glob1("ui", "*.ui"):
        os.system("pyuic4 -o ui/ui_%s.py ui/%s -g %s" % (filename.split(".")[0], filename, PROJECT))

    # Collect headers for desktop files
    for filename in glob.glob("data/*.desktop.in"):
        os.system("intltool-extract --type=gettext/ini %s" % filename)

    filelist = os.popen("find data src ui -name '*.h' -o -name '*.py'").read().strip().split("\n")
    filelist.sort()
    with open(files, "w") as _files:
        _files.write("\n".join(filelist))

    # Generate POT file
    os.system("xgettext --default-domain=%s \
                        --keyword=_ \
                        --keyword=N_ \
                        --keyword=i18n \
                        --keyword=ki18n \
                        --kde \
                        -ci18n -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 -ktr2i18n:1 \
                        -kI18N_NOOP:1 -kI18N_NOOP2:1c,2 -kaliasLocale -kki18n:1 -kki18nc:1c,2 \
                        -kki18np:1,2 -kki18ncp:1c,2,3 \
                        --files-from=%s \
                        -o po/%s.pot" % (PROJECT, files, PROJECT))

    # Update PO files
    for item in glob.glob1("po", "*.po"):
        print "Updating .. ", item
        os.system("msgmerge --update --no-wrap --sort-by-file po/%s po/%s.pot" % (item, PROJECT))

    # Cleanup
    os.unlink(files)
    for f in [_f for _f in filelist if _f.startswith("ui/") or _f.endswith(".h")]:
        try:
            os.unlink(f)
        except OSError:
            pass


class Build(build):
    def run(self):

        # Clear all
        os.system("rm -rf build")

        # Copy codes
        print "Copying PYs..."
        os.system("cp -R src/ build/")

        # Copy icons
        print "Copying Images..."
        os.system("cp -R data/ build/")

        print "Generating .desktop files..."
        for filename in glob.glob("data/*.desktop.in"):
            os.system("intltool-merge -d po %s %s" % (filename, filename[:-3]))

        print "Generating UIs..."
        for filename in glob.glob1("ui", "*.ui"):
            os.system("pyuic4 -o build/ui_%s.py ui/%s -g %s" % (filename.split(".")[0], filename, PROJECT))

        print "Generating RCs..."
        for filename in glob.glob1("data", "*.qrc"):
            os.system("pyrcc4 data/%s -o build/%s_rc.py" % (filename, filename.split(".")[0]))

class Install(install):
    def run(self):
        install.run(self)
        def rst2doc(lang):
            if os.path.exists(os.path.join('help', lang)):
                for doc in ('main_help', 'preferences_help'):
                    if os.path.exists(os.path.join('help', lang,'%s.rst' % doc)):
                        os.system("rst2html --stylesheet help/help.css help/%s/%s.rst > help/%s/%s.html" % (lang, doc, lang, doc))

        if self.root:
            root_dir = "%s/usr/share" % self.root
            bin_dir = os.path.join(self.root, "usr/bin")
        else:
            root_dir = "/usr/share"
            bin_dir = "/usr/bin"

        mime_icons_dir = os.path.join(root_dir, "icons/hicolor")
        icon_dir = os.path.join(root_dir, "icons/hicolor/128x128/apps")
        mime_dir = os.path.join(root_dir, "mime/packages")
        locale_dir = os.path.join(root_dir, "locale")
        apps_dir = os.path.join(root_dir, "applications")
        project_dir = os.path.join(root_dir, PROJECT)

        # Make directories
        print "Making directories..."
        makeDirs(mime_icons_dir)
        makeDirs(icon_dir)
        makeDirs(mime_dir)
        makeDirs(bin_dir)
        makeDirs(locale_dir)
        makeDirs(apps_dir)
        makeDirs(project_dir)

        # Install desktop files
        print "Installing desktop files..."

        for filename in glob.glob("data/*.desktop"):
            shutil.copy(filename, apps_dir)

        shutil.copy("data/%s.png" % PROJECT, icon_dir)
        shutil.copy("data/%s.xml" % PROJECT, mime_dir)

        # Install icons
        for size in ["16x16", "32x32", "48x48", "64x64"]:
            mime_size_dir = "%s/%s/mimetypes/" % (mime_icons_dir, size)
            makeDirs(mime_size_dir)
            shutil.copy("data/%s-%s.png" % (PROJECT, size), "%s/application-x-pisi.png" % mime_size_dir)

        # Install codes
        print "Installing codes..."
        os.system("cp -R build/* %s/" % project_dir)

        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            rst2doc(lang)
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            makeDirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % PROJECT))
        rst2doc('en')
        if os.path.exists('help'):
            print "Installing help files..."
            os.system("cp -R help %s/" % project_dir)

        # Rename
        print "Renaming application.py..."
        shutil.move(os.path.join(project_dir, "main.py"), os.path.join(project_dir, "%s.py" % PROJECT))

        # Modes
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.py" % PROJECT), 0755)
        os.chmod(os.path.join(project_dir, "pm-install.py"), 0755)

        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % PROJECT), os.path.join(bin_dir, PROJECT))
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "pm-install.py"), os.path.join(bin_dir, "pm-install"))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % PROJECT), os.path.join(bin_dir, PROJECT))
                os.symlink(os.path.join(project_dir, "pm-install.py"), os.path.join(bin_dir, "pm-install"))
        except OSError:
            pass


class Uninstall(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        root_dir = "/usr/share"
        bin_dir = "/usr/bin"

        locale_dir = os.path.join(root_dir, "locale")
        apps_dir = os.path.join(root_dir, "applications")
        project_dir = os.path.join(root_dir, PROJECT)

        print 'Uninstalling ...'
        remove(project_dir)
        remove(apps_dir +"/%s.desktop" % PROJECT)
        for filename in glob.glob1('po', '*.po'):
            lang = filename.rsplit(".", 1)[0]
            remove(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % PROJECT))


class Clean(clean):
    def run(self):
        print 'Cleaning ...'
        os.system('find -name *.pyc|xargs rm -rf')
        os.system('find -name *.mo|xargs rm -rf')
        for dirs in ('build', 'dist'):
            if os.path.exists(dirs):
                print ' removing: ', dirs
                shutil.rmtree(dirs)
        clean.run(self)

if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
      name              = PROJECT,
      version           = about.version,
      description       = unicode(about.PACKAGE),
      license           = unicode('GPL'),
      author            = "Pardus Developers",
      author_email      = about.bugEmail,
      url               = about.homePage,
      data_files        = [('/usr/share/doc/%s' % PROJECT, ['AUTHORS', 'ChangeLog'])],
      cmdclass          = {
                            'build': Build,
                            'install': Install,
                            'uninstall':Uninstall,
                            'clean':Clean
                          }
)
