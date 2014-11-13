#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python Libs
import os
import shutil

# DistUtils
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.sdist import sdist
from distutils.command.install import install
from distutils.sysconfig import get_python_lib

PROJECT = 'appinfo'

def plp():
    return os.path.join(get_python_lib(), PROJECT)

class Clean(clean):
    def run(self):
        print 'Cleaning ...'
        os.system('find -name *.pyc|xargs rm -rf')
        for dirs in ('build', 'dist'):
            if os.path.exists(dirs):
                print ' removing: ', dirs
                shutil.rmtree(dirs)
        clean.run(self)

class Dist(sdist):
    def run(self):
        os.system('python setup.py build')
        sdist.run(self)

class Uninstall(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print 'Uninstalling ...'
        project_dir = plp()
        if os.path.exists(project_dir):
            print ' removing: ', project_dir
            shutil.rmtree(project_dir)

class Install(install):
    def run(self):
        install.run(self)
        root_dir = '/usr/bin'
        if self.root:
            root_dir = "%s/usr/bin" % self.root
        shutil.move('%s/%s.py' % (root_dir, PROJECT), '%s/%s' % (root_dir, PROJECT))


setup(name=PROJECT,
      version='0.2',
      description='Appinfo: Metadata information for packages',
      long_description='Package Management System indepented, package metadata'\
                       'information management system.',
      license='GNU GPL2',
      author='Gökmen Göksel',
      author_email='gokmen@pardus.org.tr',
      url='http://developer.pardus.org.tr',
      packages=[PROJECT, '%s.backends' % PROJECT],
      data_files = [(plp(), ['AUTHORS', 'ChangeLog', 'README', 'COPYING', 'HELP'])],
      scripts = ['appinfo.py'],
      cmdclass = {
                  'install': Install,
                  'uninstall':Uninstall,
                  'clean'    :Clean,
                 }
     )
