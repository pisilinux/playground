#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2011 TUBITAK/BILGEM
#  Renan Çakırerk <renan at pardus.org.tr>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#  (See COPYING)

import os
import glob
import shutil
import sys
import re

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

from code.quickformat import about

PROJECT = about.appName

def tr2i18n(filename):
    """Converts QT's translate methods with gettext's i18n method which
    declared in i18n.py module"""

    template = '%s.set%s(i18n("%s"))'
    old_file = open(filename)
    new_file = open(filename, "a")
    p = re.compile(r"(.*?)\.set(.*?)\(QtGui.QApplication.translate\(\".*?\", \"(.*?)\"")

    for line in old_file.readlines():
        ma = p.match(line)
        if ma == None:
            new_file.write(line)
        else:
            new_file.write(template % (ma.group(1), ma.group(2), ma.group(3))+"\n")
    new_file.write("from quickformat.i18n import i18n")

def update_messages():
    # Create empty directory
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("ui", "*.ui"):
        os.system("pyuic4 -o .tmp/ui_%s.py ui/%s" % (filename.split(".")[0], filename))
    # Collect Python files
    os.system("cp -R code/* .tmp/")
    os.system("cp -R code/quickformat/* .tmp/")
    # Generate POT file
    os.system("find .tmp -name '*.py' | xargs xgettext \
                    --default-domain=%s --keyword=i18n -o po/%s.pot" % (about.catalog, about.catalog))

    # Collect desktop files
    os.system("cp -R data/*.desktop.in .tmp/")

    # Generate headers for desktop files
    for filename in glob.glob(".tmp/*.desktop.in"):
        os.system("intltool-extract --type=gettext/ini %s" % filename)

    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge -q -o .tmp/temp.po po/%s po/%s.pot" % (item, about.catalog))
            os.system("cp .tmp/temp.po po/%s" % item)
    # Remove temporary directory
    #os.system("rm -rf .tmp")

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
        os.system("cp -R code/ build/")
        # Copy compiled UIs and RCs
        print "Generating UIs..."
        for filename in glob.glob1("ui", "*.ui"):
            os.system("pyuic4 -o build/%s/ui_%s.py ui/%s" % (about.appName, filename.split(".")[0], filename))
            tr2i18n("build/%s/ui_%s.py" % (about.appName, filename.split(".")[0]))
        #print "Generating RCs..."
        for filename in glob.glob1("data", "*.qrc"):
            os.system("/usr/bin/pyrcc4 data/%s -o build/%s_rc.py" % (filename, filename.split(".")[0]))

class Install(install):
    def run(self):
        os.system("./setup.py build")
        if self.root:
            z_dir = "%s/usr" % self.root
        else:
            kde_dir = "/usr"
        bin_dir = os.path.join(kde_dir, "bin")
        locale_dir = os.path.join(kde_dir, "share/locale")
        apps_dir = os.path.join(kde_dir, "share/applications")
        project_dir = os.path.join(kde_dir, "share", about.appName)

        # Make directories
        print "Making directories..."
        makeDirs(bin_dir)
        makeDirs(locale_dir)
        makeDirs(apps_dir)
        makeDirs(project_dir)

        # Install desktop files
        print "Installing desktop files..."

        for filename in glob.glob("data/*.desktop.in"):
            os.system("intltool-merge -d po %s %s" % (filename, filename[:-3]))

        # Install desktop files
        print "Installing desktop files..."
        shutil.copy("data/%s.desktop" % PROJECT, apps_dir)

        print "Installing icon file..."
        shutil.copy("data/images/draw-eraser-icon.png", "/usr/share/pixmaps")

        # Install codes
        print "Installing codes..."
        os.system("cp -R build/* %s/" % project_dir)

        # Install rc file
        print "Installing resource file"
        os.system("pyrcc4 data/images.qrc > %s/data_rc.py" % project_dir)

        # Install pics
        print "Installing pics..."
        os.system("cp -R data/images %s" % project_dir)
        #os.system("cp -R resources/icons %s" % project_dir)

        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % about.catalog))

        # Rename
        #print "Renaming application.py..."
        #shutil.move(os.path.join(project_dir, "application.py"), os.path.join(project_dir, "%s.py" % about.appName))

        # Modes
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.py" % about.appName), 0755)
        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
        except OSError:
            pass


if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
      name              = about.appName,
      version           = about.version,
      description       = unicode(about.description),
      license           = unicode(about.license),
      author            = "",
      author_email      = about.bugEmail,
      url               = about.homePage,
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'build': Build,
                            'install': Install,
                          }
)
