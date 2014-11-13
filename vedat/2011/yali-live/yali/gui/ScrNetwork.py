#!/usr/bin/python
# -*- coding: utf-8 -*-

import pds.container
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QGridLayout
import yali.context as ctx
from yali.gui import ScreenWidget

class Widget(QWidget, ScreenWidget):
    name = "network"

    def __init__(self):
        QWidget.__init__(self)
        self.layout = QGridLayout(self)
        self.networkConnector = pds.container.PNetworkManager(self)
        self.layout.addWidget(self.networkConnector)

    def shown(self):
        self.networkConnector.startNetworkManager()

    def execute(self):
        self.networkConnector._proc.terminate()
        ctx.mainScreen.disableBack()
        return True


