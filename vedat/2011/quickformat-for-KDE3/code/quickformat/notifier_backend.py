#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# GUI Module ~ gui.py

# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Python Libraries
import copy

# Qt Libraries
from PyQt4 import QtGui
from PyQt4 import QtCore

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize

from PyQt4.QtGui import QColor
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPalette


# PREDEFINED POSITIONS
# --------------------
(TOPLEFT, TOPCENTER, TOPRIGHT, \
 MIDLEFT, MIDCENTER, MIDRIGHT, \
 BOTLEFT, BOTCENTER, BOTRIGHT,
 CURRENT) = range(10)
# --------------------
FORWARD = QtCore.QTimeLine.Forward
BACKWARD = QtCore.QTimeLine.Backward
# --------------------
(IN, OUT, FINISHED) = range(3)
# --------------------

class PAbstractBox(QtGui.QWidget):
    def __init__(self, parent):

        # Overlay widget, it should be initialized at first
        self.__overlay = QtGui.QWidget(parent)
        self.__overlay.hide()
        self.__overlay_enabled = False
        self.__overlay_animated = False
        self.__overlay_styled = False

        # Main widget initializing on parent widget
        QtGui.QWidget.__init__(self, parent)
        self.hide()

        # Pre-defined states
        self.__last_direction = OUT
        self.__last_move_direction = FORWARD
        self.__last_start = TOPCENTER
        self.__last_stop = BOTCENTER
        self.__overlay_duration = 1400
        self.__overlay_opacity = 200
        self._duration = 2000
        self._disable_parent_in_shown = False

        # Parent Widget
        self.__parent = parent
        self._updateParentResizeEvent()

        # Initialize Timelines
        self._initializeTimeLines()

        # Animation, QEasingCurve.Type
        self._animation = 38

        # Callback functions for using at pre-defined statements
        self.__call_back_functions = {IN:[], OUT:[], FINISHED:[]}

        # Resize functions for using with resize event
        self.__resize_functions = []
        self.registerResizeFunction(self._updatePositionWhenResized)

        # Update Parent widgets resize events when animation finished
        self.registerFunction(FINISHED, self._updateParentResizeEvent)

    def _disable_parent(self):
        if self._disable_parent_in_shown:
            for item in self.__parent.children():
                if not item == self and not item.inherits("QLayout"):
                    try:
                        item.setEnabled(not self.__last_direction == IN)
                    except:
                        pass

    def _isVisible(self):
        return self.__last_direction == IN

    def _updateParentResizeEvent(self):
        # Override parents resize-event
        self.__parent.resizeEvent = self._resizeCallBacks

    def _resizeCallBacks(self, event):
        # Run aldready registered resize functions
        for func in self.__resize_functions:
            func(event)

    def _updatePositionWhenResized(self, event):
        if self.__overlay_enabled:
            self.__overlay.resize(self.__parent.size())
        if self.isVisible() or self.__last_direction == IN:
            self._animate(self.__last_direction,
                          self.__last_move_direction,
                          CURRENT,
                          self.__last_stop,
                          self._duration,
                          True)

    def _initializeTimeLines(self):
        # Timeline for X coordinate
        self.__sceneX = QtCore.QTimeLine()

        # Timeline for Y coordinate
        self.__sceneY = QtCore.QTimeLine()

        # Timeline for fade-effect of overlay
        self.__sceneF = QtCore.QTimeLine()

        # Set overlay animation
        if self.__overlay_enabled:
            self.enableOverlay(self.__overlay_animated, self.__overlay_styled)

    def enableShadow(self, offset = 3, radius = 9, color = 'black'):
        # Enable shadow for mainwidget with given features
        self.__effect = QtGui.QGraphicsDropShadowEffect(self)
        self.__effect.setBlurRadius(radius)
        self.__effect.setOffset(offset)
        self.__effect.setColor(QtGui.QColor(color))
        self.setGraphicsEffect(self.__effect)

    def enableOverlay(self, animated = False, use_style = True):
        # Resize the overlay with parent's size
        self.__overlay.resize(self.__parent.size())
        self.__overlay_enabled = True
        self.__overlay_animated = animated
        self.__overlay_styled = use_style
        self.__sceneF.setUpdateInterval(20)

        # When animation finished, overlay animation should be stop
        self.registerFunction(IN,  self.__sceneF.stop)

        if self.__overlay_styled:
            if animated:
                # Register animation range for overlay fade-in/out effect
                self.__sceneF.setFrameRange(0, 200)
                self.__sceneF.frameChanged.connect(lambda x: self.__overlay.setStyleSheet('background-color: rgba(0,0,0,%s)' % x))
                self.registerFunction(IN,  lambda: self.__sceneF.setFrameRange(0, 200))
                self.registerFunction(OUT, lambda: self.__sceneF.setFrameRange(200, 0))
            else:
                # Set overlay opacity
                self.__overlay.setStyleSheet('background-color: rgba(0,0,0,%s)' % self.__overlay_opacity)
        else:
            self.__overlay.setAutoFillBackground(True)

    def disableOverlay(self):
        self.__overlay_enabled = False

    def animate(self, direction = IN, move_direction = FORWARD, start = TOPCENTER, stop = BOTCENTER, start_after = None, duration = 0, dont_animate = False):

        if start_after:
            if start_after.state() == QtCore.QTimeLine.Running:
                # If there is an animation started before this one, we can easily start it when the old one finishes
                start_after.finished.connect(lambda: self._animate(direction, move_direction, start, stop, duration))
                return

        # Otherwise, run the animation directly and return the timeline obj for using as a reference for later animations
        return self._animate(direction, move_direction, start, stop, duration, dont_animate = dont_animate)

    def _animate(self, direction, move_direction, start, stop, duration, just_resize = False, dont_animate = False):

        # Stop all running animations
        for timeline in (self.__sceneX, self.__sceneY, self.__sceneF):
            timeline.stop()

        # Re-initialize Timelines
        self._initializeTimeLines()

        # Use given duration time or use the default one
        duration = duration if duration > 0 else self._duration

        # Set last used animations with given values
        self.__last_stop           = stop
        self.__last_start          = start
        self.__last_move_direction = move_direction
        self.__last_direction      = direction

        # Set X coordinate timeline settings
        self.__sceneX.setDirection(move_direction)
        self.__sceneX.setEasingCurve(QtCore.QEasingCurve(self._animation))
        self.__sceneX.setDuration(duration)
        self.__sceneX.setUpdateInterval(20)

        # Set Y coordinate timeline settings
        self.__sceneY.setDirection(move_direction)
        self.__sceneY.setEasingCurve(QtCore.QEasingCurve(self._animation))
        self.__sceneY.setDuration(duration)
        self.__sceneY.setUpdateInterval(20)

        # Update duration for overlay fade effect
        self.__sceneF.setDuration(self.__overlay_duration)

        # Get current sizes
        p_width  = self.__parent.width()
        p_height = self.__parent.height()
        width  = self.width()
        height = self.height()

        # Calculate new positions for given points
        limits = {TOPLEFT   : [0, 0],
                  TOPCENTER : [p_width/2 - width/2, 0],
                  TOPRIGHT  : [p_width - width, 0],
                  MIDLEFT   : [0, p_height/2 - height/2],
                  MIDCENTER : [p_width/2 - width/2, p_height/2 - height/2],
                  MIDRIGHT  : [p_width - width, p_height/2 - height/2],
                  BOTLEFT   : [0, p_height - height],
                  BOTCENTER : [p_width/2 - width/2, p_height - height],
                  BOTRIGHT  : [p_width - width, p_height - height],
                  CURRENT   : [self.x(), self.y()]}

        # Get start and stop positions
        # I used deepcopy in case of selecting same positions for start and stop
        start_pos = copy.deepcopy(limits[start])
        stop_pos  = copy.deepcopy(limits[stop])

        # Poor developer's debug mechanism.
        # print start_pos, stop_pos, width, height

        # Update start and stop positions for given direction
        if direction == IN:
            self.show()
            if start in (TOPLEFT, MIDLEFT, BOTLEFT):
                start_pos[0] -= width
            elif start in (TOPRIGHT, MIDRIGHT, BOTRIGHT):
                start_pos[0] += width
            elif start == TOPCENTER:
                start_pos[1] -= height
            elif start == BOTCENTER:
                start_pos[1] += height
        elif direction == OUT:
            if stop in (TOPLEFT, MIDLEFT, BOTLEFT):
                stop_pos[0] -= width
            elif stop in (TOPRIGHT, MIDRIGHT, BOTRIGHT):
                stop_pos[0] += width
            elif stop == TOPCENTER:
                stop_pos[1] -= height
            elif stop == BOTCENTER:
                stop_pos[1] += height

        # Move the widget to calculated start position
        self.move(start_pos[0], start_pos[1])

        # Set calculated start and stop positions
        self.__sceneX.setFrameRange(start_pos[0], stop_pos[0])
        self.__sceneX.frameChanged.connect(lambda x: self.move(x, self.y()))
        self.__sceneY.setFrameRange(start_pos[1], stop_pos[1])
        self.__sceneY.frameChanged.connect(lambda y: self.move(self.x(), y))

        # Run predefined callback functions for given direction
        self.runCallBacks(direction)
        self._disable_parent()

        # Hide widget when direction is OUT
        self.__sceneX.finished.connect(lambda: self.setHidden(direction == OUT))

        # Run finish callbacks
        self.__sceneX.finished.connect(lambda: self.runCallBacks(FINISHED))

        # Show/hide overlay if overlay enabled
        if self.__overlay_enabled:
            self.__overlay.show()
            self.__sceneX.finished.connect(lambda: self.__overlay.setHidden(direction == OUT))
        else:
            self.__overlay.hide()

        if dont_animate:
            self.__overlay.setHidden(direction == OUT)
            self.setHidden(direction == OUT)
            self.runCallBacks(FINISHED)
        else:
            # Start the animation !
            if self.__sceneX.state() == QtCore.QTimeLine.NotRunning:
                self.__sceneX.start()
                self.__sceneY.start()
                if not just_resize:
                    # The animation will just work for repositioning the widget,
                    # so we dont need overlay fade animation
                    self.__sceneF.start()

        # Return the X coordinate timeline obj to use as reference for next animation
        return self.__sceneX

    def flushCallBacks(self, direction, approve = False):
        # Reset given direction's call backs
        self.__call_back_functions[direction] = []

    def registerResizeFunction(self, func):
        # Add function to resize functions list
        if not func in self.__resize_functions:
            self.__resize_functions.append(func)

    def registerFunction(self, direction, func):
        # Add function to given direction's list
        if not func in self.__call_back_functions[direction]:
            self.__call_back_functions[direction].append(func)

    def runCallBacks(self, direction):
        # Run all functions for given direction
        for func in self.__call_back_functions[direction]:
            func()

    def setOverlayClickMethod(self, method):
        self.__overlay.mousePressEvent = method

    def setOverlayOpacity(self, opacity = 200):
        self.__overlay_opacity = opacity


class QProgressIndicator(QWidget):

    def __init__(self, parent, color = None):
        QWidget.__init__(self, parent)

        self.angle = 0
        self.timerId = -1
        self.delay = 80
        self.displayedWhenStopped = False
        self.color = self.palette().color(QPalette.Text) if not color else QColor(color)

    def busy(self):
        self.startAnimation()
        self.show()

    def isAnimated(self):
        return not self.timerId == -1

    def setDisplayedWhenStopped(self, state):
        self.displayedWhenStopped = state
        self.update()

    def isDisplayedWhenStopped(self):
        return self.displayedWhenStopped

    def startAnimation(self):
        self.angle = 0
        if self.timerId == -1:
            self.timerId = self.startTimer(self.delay)

    def stopAnimation(self):
        if not self.timerId == -1:
            self.killTimer(self.timerId)
        self.timerId = -1
        self.update()

    def setAnimationDelay(self, delay):
        if not self.timerId == -1:
            self.killTimer(self.timerId)
        self.delay = delay
        if self.timerId == -1:
            self.timerId = self.startTime(self.delay)

    def setColor(self, color):
        self.color = color
        self.update()

    def sizeHint(self):
        return QSize(20,20)

    def heightForWidth(self, width):
        return width

    def timerEvent(self, event):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        if not self.displayedWhenStopped and not self.isAnimated():
            return

        width = min(self.width(), self.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width-1) * 0.5
        innerRadius = (width-1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth  = capsuleHeight * 0.23 if width > 32 else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(12):
            color = QColor(self.color)
            color.setAlphaF(float(1.0 - float(i / 12.0)))
            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self.angle - float(i * 30.0))
            p.drawRoundedRect(-capsuleWidth * 0.5,\
                              -(innerRadius + capsuleHeight),\
                              capsuleWidth,\
                              capsuleHeight,\
                              capsuleRadius,\
                              capsuleRadius)
            p.restore()

