#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

DEFAULT_HEIGHT = 52
MAX_HEIGHT = DEFAULT_HEIGHT * 3
(UP, DOWN) = range(2)

class HoverLinkFilter(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        self._init_values()

    def _init_values(self):
        self.link_rect = QRect()
        self.button_rect = QRect()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove and self.parent.direction == UP:
            if self.link_rect.contains(event.pos()):
                obj.setCursor(Qt.PointingHandCursor)
            else:
                obj.unsetCursor()
            return True
        return QObject.eventFilter(self, obj, event)

class RowAnimator(object):
    def __init__(self, updater=None):
        self.height = DEFAULT_HEIGHT
        self.max_height = DEFAULT_HEIGHT * 3
        self.direction = DOWN
        self.row = None
        self.lastrow = None
        self.t_view = updater
        self.initTimeLine()
        self.hoverLinkFilter = HoverLinkFilter(self)
        self.t_view.installEventFilter(self.hoverLinkFilter)

    def initTimeLine(self):
        self.timeLine = QTimeLine(300)
        QObject.connect(self.timeLine, SIGNAL("frameChanged(int)"), self.updateSize)
        QObject.connect(self.timeLine, SIGNAL("finished()"), self.finished)
        self.timeLine.setDirection(QTimeLine.Backward)

    def animate(self, row, reverseOld = False):
        if self.timeLine.state() == QTimeLine.Running:
            return
        if self.row >= 0:
            if not self.row == row:
                self.timeLine.setFrameRange(DEFAULT_HEIGHT, self.max_height)
                self.timeLine.start()
                QObject.connect(self.timeLine, SIGNAL("finished()"), lambda: self.animate(row, True))
                if not reverseOld:
                    return

        self.initTimeLine()
        self.setRow(row)
        self.timeLine.setFrameRange(DEFAULT_HEIGHT, self.max_height)
        self.timeLine.start()

    def reset(self, row=None):
        self.timeLine.setDirection(QTimeLine.Forward)
        self.height = DEFAULT_HEIGHT
        if self.row >= 0:
            self.t_view.setRowHeight(self.row, self.height)
        self.direction = DOWN
        self.row = row

    def finished(self):
        if self.direction == DOWN:
            self.direction = UP
            self.height = self.max_height
            self.timeLine.setDirection(QTimeLine.Backward)
            self.hoverLinkFilter._init_values()
        else:
            self.direction = DOWN
            self.height = DEFAULT_HEIGHT
            self.timeLine.setDirection(QTimeLine.Forward)
        self.t_view.setRowHeight(self.row, self.height)
        self.row = None if self.direction == DOWN else self.row

    def size(self):
        return QSize(0, self.height)

    def setRow(self, row):
        if not self.row == row:
            self.reset(row)

    def currentRow(self):
        return self.row

    def running(self):
        return self.timeLine.state() == QTimeLine.Running

    def updateSize(self, size):
        if self.direction == DOWN:
            self.height = size
            if self.height > self.max_height:
                self.height = self.max_height
        else:
            self.height = size
            if self.height < DEFAULT_HEIGHT:
                self.height = DEFAULT_HEIGHT
        self.timeLine.setFrameRange(DEFAULT_HEIGHT, self.max_height)
        self.t_view.setRowHeight(self.row, self.height)

