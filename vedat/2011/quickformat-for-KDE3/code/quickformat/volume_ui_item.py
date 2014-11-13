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

from PyQt4 import QtGui
from ui_volumeitem import Ui_VolumeItem

class VolumeUiItem(Ui_VolumeItem, QtGui.QWidget):

    def __init__(self, volume, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.device.hide()

        self.name.setText(volume.device_name)
        self.device.setText(volume.device_path)

        if volume.name == "":
            volume.name = "Volume (%s)" % volume.file_system 
            self.label.setText(volume.name)
        else:
            self.label.setText(volume.name)
        self.path.setText(volume.path)

        size_human = self.size_to_human(volume.size)

        self.size.setText(size_human)
        self.format.setText("(%s)" % volume.file_system)
        self.icon.setPixmap(volume.icon)

    def size_to_human(self, size):
        size = size / 1024.0 ** 2

        if size >= 1000 and size < 100000:
            size = str("%.2f" % (size / 1024.0)) + " GB"
        elif size > 100000:
            size = str(int(size / 1024)) + " GB"
        else:
            size = str(int(size)) + " MB"

        return size
