.. Disk Manager documentation master file, created by
   sphinx-quickstart on Wed May 11 10:05:33 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Disk Manager
~~~~~~~~~~~~

:Author: Mehmet Özdemir

Disk Manager is a Pardus GUI application used for managing automatic mount 
operations for your disks. It provides an easy interface to configure. You 
do configure how your disk partitions will be initialized at system startup. 
Disks are integrated into system's file system with this configuration. So 
that you do not have to mount your disks manually again and again. Disk 
Manager also allows you to mount or unmount your disk partitions.


API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api/index.rst


Features
--------

* Add an entry. (entry = a line which is used for to describe partition initialization information)
   - Adding an entry includes a mount operation if that entry is not already mounted.
* Remove an entry
* Mount a partition
* Unmount a partition

Source Code
-----------

You can `browse <http://svn.pardus.org.tr/uludag/branches/kde/disk-manager/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/branches/kde/disk-manager/

Requirements
------------

* PyQt3
* PyKDE3
* kdelibs
* dbus-python


Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Disk%20Y%C3%B6neticisi%20%2F%20Disk%20Manager>`_
* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Disk%20Y%C3%B6neticisi%20%2F%20Disk%20Manager>`_
* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Disk%20Y%C3%B6neticisi%20%2F%20Disk%20Manager>`_

Tasks
-----

* `Open Tasks <http://proje.pardus.org.tr:50030/projects/disk-manager/issues?set_filter=1&tracker_id=4>`_

Developed by
------------

* Gökmen GÖKSEL <gokmen [at] pardus.org.tr>
* İşbaran AKÇAYIR <isbaran [at] gmail.com>

Fstab Module Authors:

* A.Murat EREN <meren [at] pardus.org.tr>

* Onur KÜÇÜK <onur [at] pardus.org.tr>

License
-------

Disk Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.


API
---

_Api

.. _Pisi: http://developer.pardus.org.tr/pisi
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr/uludag/trunk/kde/disk-manager/
.. _Api: http://developer.pardus.org.tr/projects/disk-manager/api/index.html


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

