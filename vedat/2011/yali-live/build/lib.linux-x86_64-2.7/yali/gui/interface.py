#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from yali.gui.YaliDialog import MessageWindow, InformationWindow, ProgressWindow, ExceptionWindow

class Interface(object):
    def __init__(self):
        self._informationWindow = None
        self._warnedUnusedRaidMembers = []

    @property
    def informationWindow(self):
        if not self._informationWindow:
            self._informationWindow = InformationWindow()
        return self._informationWindow

    def exceptionWindow(self, error, traceback):
        return ExceptionWindow(error, traceback).rc

    def progressWindow(self, message):
        return ProgressWindow(message)

    def messageWindow(self, title, text, type="ok", default=None, customButtons=None, customIcon=None):
        return MessageWindow(title, text, type, default, customButtons, customIcon, run=True).rc

    def detailedMessageWindow(self, title, text, longText, type="ok", default=None, customButtons=None, customIcon=None):
        return MessageWindow(title, text, type, default, customButtons, customIcon, run=True, detailed=True, longText=longText).rc
