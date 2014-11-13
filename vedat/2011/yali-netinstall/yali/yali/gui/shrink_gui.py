#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali.context as ctx
from yali.gui import storageGuiHelpers
from yali.gui.Ui.partitionshrink import Ui_ShrinkPartitionWidget
from yali.gui.YaliDialog import Dialog
from yali.storage.operations import OperationResizeDevice, OperationResizeFormat
from yali.storage.formats.filesystem import FilesystemError

class ShrinkEditor:
    def __init__(self, parent, storage):
        self.storage = storage
        self.intf = parent.intf
        self.parent = parent
        self.dialog = Dialog(_("Partitions to Shrink"), closeButton=False)
        self.dialog.addWidget(ShrinkWidget(self))
        self.dialog.resize(QSize(0,0))

    def run(self):
        if self.dialog is None:
            return []

        while 1:
            rc = self.dialog.exec_()
            operations = []

            if not rc:
                self.destroy()
                return (rc, operations)

            widget = self.dialog.content

            request = widget.partitions.itemData(widget.partitions.currentIndex()).toPyObject()
            newsize = widget.sizeSpin.value()

            try:
                operations.append(OperationResizeFormat(request, newsize))
            except ValueError as e:
                self.intf.messageWindow(_("Resize FileSystem Error"),
                                        _("%(device)s: %(msg)s") %
                                        {'device': request.format.device, 'msg': e.message},
                                        type="error")
                continue

            try:
                operations.append(OperationResizeDevice(request, newsize))
            except ValueError as e:
                self.intf.messageWindow(_("Resize Device Error"),
                                              _("%(name)s: %(msg)s") %
                                               {'name': request.name, 'msg': e.message},
                                               type="warning")
                continue

            # everything ok, fall out of loop
            break

        self.dialog.destroy()

        return (rc, operations)

    def destroy(self):
        if self.dialog:
            self.dialog = None


class ShrinkWidget(QtGui.QWidget, Ui_ShrinkPartitionWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent.parent)
        self.setupUi(self)
        self.parent = parent
        self.operations = []
        self.storage = parent.storage

        storageGuiHelpers.fillResizablePartitions(self.partitions, self.storage)
        QObject.connect(self.partitions, SIGNAL("currentIndexChanged(int)"), self.updateSpin)
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.parent.dialog.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.parent.dialog.reject)

        #Force to show max, min values
        #self.partitions.setCurrentIndex(0)
        self.updateSpin(0)

    def updateSpin(self, index):
        request = self.partitions.itemData(index).toPyObject()
        try:
            requestlower = 1
            requestupper = request.maxSize
            if request.format.exists:
                requestlower = request.minSize
            if request.type == "partition":
                geomsize = request.partedPartition.geometry.getSize(unit="MB")
                if (geomsize != 0) and (requestupper > geomsize):
                    requestupper = geomsize
        except FilesystemError, msg:
            ctx.logger.error("Shrink Widget update spin gives error:%s" % msg)
        else:
            self.sizeSpin.setRange(max(1, requestlower), requestupper)
            self.sizeSpin.setValue(requestlower)
            self.sizeSlider.setRange(max(1, requestlower), requestupper)
            self.sizeSlider.setValue(requestlower)
