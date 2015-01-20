#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QPixmap, Qt, QListWidgetItem, QSize, QTimeLine, QTimer

import yali.util
import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.collectionswidget import Ui_CollectionsWidget
from yali.gui.Ui.collectionitem import Ui_CollectionItem

CLOSED_SIZE = 36
ANIMATE_TIME = 400
EXPANDED_SIZE = 146

class Widget(Ui_CollectionsWidget, QWidget, ScreenWidget):
    name = "collectionSelection"

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.collections = None
        self.current_item = None
        self.last_item = None
        self.collectionList.itemClicked.connect(self.openItem)
        self.collectionList.currentItemChanged.connect(self.itemChanged)

    def fillCollections(self):
        self.collectionList.clear()
        selected = None
        for index, collection in enumerate(self.collections):
            self.addItem(collection)
            if ctx.installData.autoCollection  == collection:
                selected = index

        if not selected:
            selected = 0

        self.current_item = self.collectionList.item(selected)
        self.last_item = self.current_item
        self.collectionList.setCurrentRow(selected)

    def shown(self):
        self.collections = ctx.collections
        self.fillCollections()
        ctx.mainScreen.disableNext()
        if self.current_item:
            self.openItem(self.current_item)
        else:
            self.openItem(self.collectionList.item(0))
        self.check()

    def execute(self):
        ctx.installData.autoCollection = self.collectionList.itemWidget(self.current_item).collection
        return True

    def check(self):
        if self.current_item:
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()

    def itemChanged(self, current, previous):
        self.current_item = current
        self.check()

    def addItem(self, collection):
        item = QListWidgetItem(self.collectionList)
        item.setSizeHint(QSize(36, CLOSED_SIZE))
        self.collectionList.addItem(item)
        self.collectionList.setItemWidget(item, CollectionItem(self, collection, item))

    def openItem(self, item):
        if item == self.last_item:
            return

        if self.last_item:
            self.closeItem(self.last_item)

        self.animation = QTimeLine(ANIMATE_TIME, self)
        self.animation.setFrameRange(36, EXPANDED_SIZE)
        self.animation.frameChanged.connect(lambda x: item.setSizeHint(QSize(32, x)))
        self.animation.start()
        self.last_item = item
        self.animation.finished.connect(lambda: self.collectionList.setCurrentItem(item))

    def closeItem(self, item):
        animation = QTimeLine(ANIMATE_TIME, self)
        animation.setFrameRange(146, CLOSED_SIZE)
        animation.frameChanged.connect(lambda x: item.setSizeHint(QSize(32, x)))
        animation.start()

class CollectionItem(Ui_CollectionItem, QWidget):
    def __init__(self, parent, collection, item):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.item = item
        self.collection = collection
        self.header.setText(collection.title)
        self.description.setText(collection.description)
        icon = QPixmap(":/gui/pics/%s" % collection.icon)
        if icon.isNull():
            icon = QPixmap(":/gui/pics/systemsettings.png")
        self.icon.setPixmap(icon)
