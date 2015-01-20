#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, QTreeWidgetItem, SIGNAL, QObject, QSize

import yali.context as ctx
from yali.gui.YaliDialog import Dialog
from yali.gui import storageGuiHelpers
from yali.gui.Ui.volumegroup import Ui_VolumeGroupWidget
from yali.gui.Ui.logicalvolume import Ui_LogicalVolumeWidget
from yali.storage import formats
from yali.storage.operations import OperationCreateDevice, OperationDestroyDevice, OperationResizeDevice, OperationMigrateFormat, OperationResizeFormat, OperationCreateFormat, OperationDestroyFormat
from yali.storage.library import lvm
from yali.storage.devices.device import Device
from yali.storage.devices.volumegroup import VolumeGroup
from yali.storage.devices.logicalvolume import LogicalVolume
from yali.storage.storageBackendHelpers import queryNoFormatPreExisting, sanityCheckMountPoint, sanityCheckVolumeGroupName, sanityCheckLogicalVolumeName

class LVMEditor(object):
    def __init__(self, parent, request, isNew=False):
        self.parent = parent
        self.storage = parent.storage
        self.origrequest = request
        self.peSize = request.peSize
        self.pvs = request.pvs[:]
        self.isNew = isNew
        self.intf = parent.intf
        self.operations = []
        self.dialog = None
        self.lvs = {}

        for lv in self.origrequest.lvs:
            self.lvs[lv.lvname] = {"name": lv.lvname,
                                   "size": lv.size,
                                   "format": copy.copy(lv.format),
                                   "originalFormat": lv.originalFormat,
                                   "stripes": lv.stripes,
                                   "logSize": lv.logSize,
                                   "snapshotSpace": lv.snapshotSpace,
                                   "exists": lv.exists}

        self.availlvmparts = self.storage.unusedPVS(vg=request)
        # if no PV exist, raise an error message and return
        if len(self.availlvmparts) < 1:
            self.intf.messageWindow(_("Not enough physical volumes"),
                                    _("At least one unused physical "
                                      "volume partition is "
                                      "needed to\ncreate an LVM Volume Group.\n"
                                      "Create a partition or RAID array "
                                      "of type \"physical volume\n(LVM)\" and then "
                                      "select the \"LVM\" option again."),
                                    type="warning")
            self.dialog = None
            return

        if isNew:
            title = _("Make LVM Volume Group")
        else:
            try:
                title = _("Edit LVM Volume Group: %s") % (request.name,)
            except AttributeError:
                title = _("Edit LVM Volume Group")

        self.dialog = Dialog(title, closeButton=False)
        self.dialog.addWidget(VolumeGroupWidget(self, self.origrequest, isNew=isNew))
        self.dialog.resize(QSize(450, 200))

    def run(self):
        if self.dialog is None:
            return []

        while 1:
            rc = self.dialog.exec_()
            operations = []
            if not rc:
                if self.isNew:
                    if self.lvs.has_key(self.origrequest.name):
                        del self.lvs[self.origrequest.name]
                self.destroy()
                return []

            widget = self.dialog.content

            name =  str(widget.name.text())
            pvs = widget.selectedPhysicalVolumes
            msg = sanityCheckVolumeGroupName(name)
            if msg:
                self.intf.messageWindow(_("Invalid Volume Group Name"),
                                        msg, type="warning")
                continue

            origname = self.origrequest.name
            if origname != name:
                if name in [vg.name for vg in self.storage.vgs]:
                    self.intf.messageWindow(_("Name in use"),
                                            _("The volume group name \"%s\" is "
                                              "already in use. Please pick another.")
                                              % (name,), type="warning")
                    continue

            peSize = widget.physicalExtends.itemData(widget.physicalExtends.currentIndex()).toInt()[0] / 1024.0

            origlvs = self.origrequest.lvs
            if not self.origrequest.exists:
                ctx.logger.debug("non-existing vg -- setting up lvs, pvs, name, peSize")
                for lv in self.origrequest.lvs:
                    self.origrequest._removeLogicalVolume(lv)

                for pv in self.origrequest.pvs:
                    if pv not in self.pvs:
                        self.origrequest._removePhysicalVolume(pv)

                for pv in self.pvs:
                    if pv not in self.origrequest.pvs:
                        self.origrequest._addPhysicalVolume(pv)

                self.origrequest.name = name
                self.origrequest.peSize = peSize

                if self.isNew:
                    operations = [OperationCreateDevice(self.origrequest)]

            for lv in origlvs:
                ctx.logger.debug("old lv %s..." % lv.lvname)
                if not lv.exists or lv.lvname not in self.lvs or \
                   (not self.lvs[lv.lvname]['exists'] and lv.exists):
                    ctx.logger.debug("removing lv %s" % lv.lvname)
                    if lv.format.type:
                        operations.append(OperationDestroyFormat(lv))

                    if lv in self.origrequest.lvs:
                        self.origrequest._removeLogicalVolume(lv)

                    operations.append(OperationDestroyDevice(lv))

            # schedule creation of all new lvs, their formats, luks devices, &c
            tempvg = widget.tmpVolumeGroup
            for lv in tempvg.lvs:
                ctx.logger.debug("new lv %s" % lv)
                if not lv.exists:
                    ctx.logger.debug("creating lv %s" % lv.lvname)
                    logicalvolume = LogicalVolume(lv.lvname, self.origrequest, size=lv.size)
                    operations.append(OperationCreateDevice(logicalvolume))

                    # create the format
                    mountpoint = getattr(lv.format, "mountpoint", None)
                    format = formats.getFormat(lv.format.type,
                                               mountpoint=mountpoint,
                                               device=logicalvolume.path)
                    operations.append(OperationCreateFormat(logicalvolume, format))
                else:
                    ctx.logger.debug("lv %s already exists" % lv.lvname)
                    origlv = widget.getLogicalVolumeByName(lv.lvname)
                    if lv.resizable and lv.targetSize != origlv.size:
                        operations.append(OperationResizeDevice(origlv, lv.targetSize))

                    if lv.format.exists:
                        ctx.logger.debug("format already exists")
                        usedev = origlv
                        format = lv.format
                        if format == usedev.originalFormat:
                            cancel = []
                            cancel.extend(self.parent.storage.devicetree.findOperations(type="create",
                                                                                        object="format",
                                                                                        devid=origlv.id))
                            cancel.extend(self.parent.storage.devicetree.findOperations(type="destroy",
                                                                                        object="format",
                                                                                        devid=origlv.id))
                            for operation in cancel:
                                self.storage.devicetree.cancelOperation(operation)

                        if hasattr(format, "mountpoint"):
                            usedev.format.mountpoint = format.mountpoint

                        if format.migratable and format.migrate and \
                           not usedev.format.migrate:
                            usedev.format.migrate = format.migrate
                            operations.append(OperationMigrateFormat(usedev))

                        if format.resizable and lv.format.resizable and \
                                lv.targetSize != format.targetSize and \
                                lv.targetSize != lv.currentSize and \
                                usedev.format.exists:
                            ctx.logger.debug("resizing format on %s to %d" % (usedev.lvname, lv.targetSize))
                            operations.append(OperationResizeFormat(usedev, lv.targetSize))
                    elif lv.format.type:
                        ctx.logger.debug("new format: %s" % lv.format.type)
                        if origlv.format.type:
                            operations.append(OperationDestroyFormat(origlv))

                        mountpoint = getattr(lv.format, "mountpoint", None)
                        format = formats.getFormat(lv.format.type,
                                                   mountpoint=mountpoint,
                                                   device=origlv.path)
                        operations.append(OperationCreateFormat(origlv, format))
                    else:
                        ctx.logger.debug("no format!")
            break

        return operations

    def destroy(self):
        if self.dialog:
            self.dialog = None

class VolumeGroupWidget(QWidget, Ui_VolumeGroupWidget):
    def __init__(self, parent, request, isNew):
        QWidget.__init__(self, parent.parent)
        self.setupUi(self)
        self.origrequest = request
        self.parent = parent
        self.isNew = isNew

        if not self.origrequest.exists:
            if not self.isNew:
                self.name.setText(self.origrequest.name)
            else:
                self.name.setText(self.parent.storage.createSuggestedVolumeGroupName())
        else:
            self.name.setText(self.origrequest.name)
            self.name.setEnabled(False)

        storageGuiHelpers.fillPhysicalExtends(self.physicalExtends)
        self.connect(self.physicalExtends, SIGNAL("currentIndexChanged(int)"), self.physicalExtendsChanged)
        if self.origrequest.exists:
            self.physicalExtends.setEnabled(False)

        storageGuiHelpers.fillLvmPhysicals(self.physicals)
        if self.origrequest.exists:
            self.physicals.setEnabled(False)

        if self.origrequest.lvs:
            for lv in self.origrequest.lvs:
                LogicalVolumeItem(self.logicalVolumesTree, lv)


        self.connect(self.addButton, SIGNAL("clicked()"), self.add)
        self.connect(self.editButton, SIGNAL("clicked()"), self.edit)
        self.connect(self.deleteButton, SIGNAL("clicked()"), self.delete)
        self.connect(self.logicalVolumesTree, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.activateButtons)
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.parent.dialog.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.parent.dialog.reject)

        # set free, used, total spaces to correct values
        self.updateSpaces()

    def activateButtons(self, item, column):
        if item and item.device is not None and isinstance(item.device, LogicalVolume):
            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
        else:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    @property
    def tmpVolumeGroup(self):
        pvs = [copy.deepcopy(pv) for pv in self.parent.pvs]
        vg = VolumeGroup('tmp-%s' % self.origrequest.name,
                         parents=pvs, peSize=self.parent.peSize)
        for lv in self.parent.lvs.values():
            logicalVolume = LogicalVolume(lv['name'], vg,
                               format=lv['format'], size=lv['size'],
                               exists=lv['exists'], stripes=lv['stripes'],
                               logSize=lv['logSize'], snapshotSpace=lv['snapshotSpace'])
            logicalVolume.originalFormat = lv['originalFormat']

        return vg

    def getLogicalVolumeByName(self, name, vg=None):
        if vg is None:
            vg = self.origrequest

        for lv in vg.lvs:
            if lv.lvname == name or lv.name == name:
                return lv
    @property
    def selectedPhysicalVolumes(self):
        pvs = []
        for index in range(self.physicals.count()):
            if self.physicals.item(index).widget.checkBox.isChecked():
                pvs.append(self.physicals.item(index).widget.pv)
        return pvs

    @property
    def smallestPhysicalVolumeSize(self):
        first = 1
        minpvsize = 1
        activePESize = self.physicalExtends.itemData(self.physicalExtends.currentIndex()).toFloat()[0]
        for pv in self.selectedPhysicalVolumes:
            try:
                peSize = activePESize / 1024.0
            except:
                peSize = self.origrequest.peSize

            pvsize = max(0, lvm.clampSize(pv.size, peSize) - peSize)
            if first:
                minpvsize = pvsize
                first = 0
            else:
                minpvsize = min(pvsize, minpvsize)

        return minpvsize

    def availableLogicalVolumes(self):
        return max(0, lvm.MAX_LV_SLOTS - len(self.parent.lvs))

    def computeSpace(self):
        vg = self.tmpVolumeGroup
        size = vg.size
        free = vg.freeSpace
        used = size - free
        return (size, used, free)

    def updateAllowedPhysicals(self):
        """ update sizes in pvs """
        for index, partition in enumerate(self.parent.availlvmparts):
            size = partition.size
            peSize = self.physicalExtends.itemData(self.physicalExtends.currentIndex()).toFloat()[0] / 1024.0
            size = lvm.clampSize(size, peSize)
            prettysize = "%10.2f MB"  % size
            self.physicals.item(index).widget.labelDrive.setText("%s (%s)" % (partition.name, prettysize))

    def updateLogicalVolumeTree(self):
        self.logicalVolumesTree.clear()
        for lv in self.parent.lvs.values():
            logicalVolume = self.getLogicalVolumeByName(lv["name"], vg=self.tmpVolumeGroup)
            LogicalVolumeItem(self.logicalVolumesTree, logicalVolume)

    def updateSpaces(self):
        (total, used, free) = self.computeSpace()

        self.totalSpace.setText("%10.2f MB" % total)
        self.usedSpace.setText("%10.2f MB" % used)

        if total > 0:
            usedpercent = (100.0 * used)/total
        else:
            usedpercent = 0.0
        self.usedSpace.setText("(%4.1f %%)" % usedpercent)

        self.freeSpace.setText("%10.2f MB" % free)
        if total > 0:
            freepercent = (100.0 * free)/total
        else:
            freepercent = 0.0
        self.freeSpace.setText("(%4.1f %%)" % freepercent)


    def physicalExtendsChanged(self, index):
        """ handle changes in the Physical Extent Option Menu """

        def getPhysicalVolumeWastedRatio(physicalextend):
            """ Given a new physicalExtend value, return percentage of smallest 
                Physical Volume wasted

                new - (int) new value of PE, in KB
            """
            pvs = self.selectedPhysicalVolumes

            waste = 0.0
            for pv in pvs:
                waste = max(waste, (long(pv.size*1024) % physicalextend)/(pv.size*1024.0))

            return waste

        def computeVolumeGroupSize(pvs, curpe):
            availSpace = 0L
            for pv in pvs:
                # have to clamp pvsize to multiple of PE
                # XXX why the suboperation? fudging metadata?
                size = lvm.clampSize(pv.size, curpe) - (curpe/1024)

                availSpace = availSpace + size

            ctx.logger.info("computeVolumeGroupSize: size is %s" % (availSpace,))
            return availSpace

        def reclampLogicalVolume(physicalextend):
            """ given a new physical extend value, set logical volume sizes accordingly

                physicalextend - (int) new value of Physical Extend, in MB
            """

            pvs = self.selectedPhysicalVolumes
            availableSpace = computeVolumeGroupSize(pvs, physicalextend)

            # see if total space is enough
            used = 0
            resize = False
            for lv in self.parent.lvs.values():
                # total space required by an lv may be greater than lv size.
                vgSpace = lv['size'] * lv['stripes'] + lv['logSize'] + lv['snapshotSpace']
                clampedVGSpace = lvm.clampSize(vgSpace, physicalextend, roundup=1)
                used += clampedVGSpace
                if lv['size'] != lvm.clampSize(lv['size'], physicalextend, roundup=1):
                    resize = True

            if used > availableSpace:
                self.parent.intf.messageWindow(_("Not enough space"),
                                               _("The physical extent size cannot be changed because\n"
                                                 "otherwise the space required by the currently defined\n"
                                                 "logical volumes will be increased to more than the\n"
                                                 "available space."),
                                               type="warning")
                return  0

            if resize:
                rc = self.parent.intf.messageWindow(_("Confirm Physical Extent Change"),
                                                   _("This change in the value of the physical extent will\n"
                                                     "require the sizes of the current logical volume requests\n"
                                                     "to be rounded up in size to an integer multiple of\n"
                                                     "the physical extent.\n\nThis change will take effect\n"
                                                     "immediately."),
                                                   type="custom", customIcon="question",
                                                   customButtons=[_("Cancel"), _("Continue")])
                if not rc:
                    return 0

            for lv in self.parent.lvs.values():
                lv['size'] = lvm.clampSize(lv['size'], physicalextend, roundup=1)

            return 1

        curpe = self.physicalExtends.itemData(index).toFloat()[0] / 1024.0
        currentValue = curpe
        lastValue = self.origrequest.peSize
        maximumPhysicalSize = self.smallestPhysicalVolumeSize
        if curpe > maximumPhysicalSize:
            self.parent.intf.messageWindow(_("Not enough space"),
                                           _("The physical extent size cannot be "
                                             "changed because\nthe value selected "
                                             "(%(curpe)10.2f MB) is larger than the\n"
                                             "smallest physical volume "
                                             "(%(maxpvsize)10.2f MB) in the volume "
                                             "group.") %
                                           {'curpe': curpe, 'maxpvsize': maximumPhysicalSize},
                                           type="warning")
            return 0

        # see if new PE will make any PV useless due to overhead
        if lvm.clampSize(maximumPhysicalSize, curpe) < curpe:
            self.parent.intf.messageWindow(_("Not enough space"),
                                           _("The physical extent size cannot be "
                                             "changed because the value selected "
                                             "(%(curpe)10.2f MB) is too large "
                                             "compared to the size of the "
                                             "smallest physical volume "
                                             "(%(maxpvsize)10.2f MB) in the "
                                             "volume group.")
                                           % {'curpe': curpe, 'maxpvsize': maximumPhysicalSize},
                                           type="warning")
            return 0

        if getPhysicalVolumeWastedRatio(curpe) > 0.10:
            rc = self.parent.intf.messageWindow(_("Too small"),
                                                _("This change in the value of the "
                                                  "physical extent will waste "
                                                  "substantial space on one or more "
                                                  "of the physical volumes in the "
                                                  "volume group."),
                                                 type="custom", customIcon="warning",
                                                 customButtons=[_("Cancel"), _("Continue")])
            if not rc:
                return 0

        # now see if we need to fixup effect PV and LV sizes based on PE
        if currentValue > lastValue:
            rc = reclampLogicalVolume(curpe)
            if not rc:
                return 0
            else:
                self.updateLogicalVolumeTree()
        else:
            maxlv = lvm.getMaxLVSize()
            for lv in self.parent.lvs.values():
                if lv['size'] > maxlv:
                    self.parent.intf.messageWindow(_("Not enough space"),
                                                   _("The physical extent size "
                                                     "cannot be changed because the "
                                                     "resulting maximum logical "
                                                     "volume size (%10.2f MB) is "
                                                     "smaller than one or more of their "
                                                     "currently defined logical "
                                                     "volumes.") % (maxlv,),
                                                   type="warning")
                    return 0

        # now actually set the VG's extent size
        self.peSize = curpe
        self.updateAllowedPhysicals()
        self.updateSpaces()


    def getCurrentLogicalVolume(self):
        return self.logicalVolumesTree.currentItem()

    def add(self):
        if self.availableLogicalVolumes < 1:
            self.parent.intf.messageWindow(_("No free slots"),
                                           _("You cannot create more than %d logical volume \n"
                                             "per volume group.") % (lvm.MAX_LV_SLOTS,),
                                           type="warning")
            return

        (total, used, free) = self.computeSpace()
        if free <= 0:
            self.parent.intf.messageWindow(_("No free space"),
                                           _("There is no room left in the volume group to create new\n"
                                             "logical volumes. To add a logical volume you must reduce\n"
                                             "the size of one or more of the currently existing logical\n"
                                             "volumes"),
                                           type="warning")
            return

        tempvg = self.tmpVolumeGroup
        name = self.parent.storage.createSuggestedLogicalVolumeName(tempvg)
        format = formats.getFormat(self.parent.storage.defaultFSType)
        self.parent.lvs[name] = {'name': name,
                          'size': free,
                          'format': format,
                          'originalFormat': format,
                          'stripes': 1,
                          'logSize': 0,
                          'snapshotSpace': 0,
                          'exists': False}
        tempvg = self.tmpVolumeGroup
        device =  self.getLogicalVolumeByName(name, vg=tempvg)
        self.editLogicalVolume(device, isNew=True)

    def edit(self):
        item = self.getCurrentLogicalVolume()
        if item is None:
            return

        self.editLogicalVolume(item.device)

    def delete(self):
        item = self.getCurrentLogicalVolume()
        if item is None:
            return

        if not item.device:
            return

        rc = self.parent.intf.messageWindow(_("Confirm Delete"),
                                            _("Are you sure you want to delete the \n"
                                              "logical volume \"%s\"?") % (item.device.lvname,),
                                            type="custom", customIcon="question",
                                            customButtons=[_("Delete"), _("Cancel")])
        if rc:
            return
        else:
            del self.parent.lvs[item.device.lvname]
            self.updateLogicalVolumeTree()
            self.updateSpaces()

    def editLogicalVolume(self, device, isNew=False):
        logicalVolumeEditor = LogicalVolumeEditor(self, device, isNew=isNew)
        while True:
            logicalvolume = logicalVolumeEditor.run()
            if logicalvolume:
                self.parent.lvs[logicalvolume["name"]] = logicalvolume
                self.updateLogicalVolumeTree()
                self.updateSpaces()
            break

        logicalVolumeEditor.destroy()


class LogicalVolumeEditor:
    def __init__(self, parent, request, isNew=False):
        self.parent = parent
        self.storage = parent.parent.storage
        self.intf = parent.parent.intf
        self.origrequest = request
        self.isNew = isNew

        if isNew:
            title = _("Make Logical Volume")
        else:
            title = _("Edit Logical Volume: %s") % request.lvname

        self.dialog = Dialog(title, closeButton=False)
        self.dialog.addWidget(LogicalVolumeWidget(self, request, isNew))
        self.dialog.resize(QSize(0, 0))

    def run(self):
        if self.dialog is None:
            return None

        while 1:
            rc = self.dialog.exec_()

            if not rc:
                if self.isNew:
                    if self.parent.parent.lvs.has_key(self.origrequest.lvname):
                        del self.parent.parent.lvs[self.origrequest.lvname]
                self.destroy()
                return None

            format = None
            widget = self.dialog.content

            format = self.origrequest.format

            mountpoint = unicode(widget.mountpointMenu.currentText())
            if mountpoint and widget.mountpointMenu.isEditable():
                msg = sanityCheckMountPoint(mountpoint)
                if msg:
                    self.intf.messageWindow(_("Mount Point Error"), msg,
                                            type="error")
                    continue

            if not self.origrequest.exists:
                format_type = str(widget.filesystemMenu.currentText())
            else:
                format_type = str(widget.formatCombo.currentText())

            format_class = formats.getFormat(format_type)
            if mountpoint and format_class.mountable:
                used = False

                current_mountpoint = getattr(format, "mountpoint", None)

                for lv in self.parent.parent.lvs.values():
                    format = lv["format"]
                    if not format.mountable or current_mountpoint and \
                        format.mountpoint == current_mountpoint:
                        continue

                    if format.mountpoint == mountpoint:
                        used = True
                        break

                for (mp, dev) in self.parent.parent.storage.mountpoints.iteritems():
                    if (dev.type != "lvmlv" or dev.vg.id != self.origrequest.vg.id) and mp == mountpoint:
                        used = True
                        break

                if used:
                    self.intf.messageWindow(_("Mount point in use"),
                                            _("The mount point \"%s\" is in "
                                              "use. Please pick another.") %
                                            (mountpoint,),
                                            type="warning")
                    continue


            name = str(widget.name.text())
            if not self.origrequest.exists:
                msg = sanityCheckLogicalVolumeName(name)
                if msg:
                    self.intf.messageWindow(_("Illegal Logical Volume Name"),
                                            msg, type="warning")
                    continue

            # check that the name is not already in use
            used = 0
            for lv in self.parent.parent.lvs.values():
                if self.origrequest.lvname != name and lv['name'] == name:
                    used = 1
                    break

            if used:
                self.intf.messageWindow(_("Illegal logical volume name"),
                                        _("The logical volume name \"%s\" is "
                                          "already in use. Please pick another.")
                                        % (name,), type="warning")
                continue


            if not self.origrequest.exists:
                badsize = 0
                try:
                    size = long(widget.sizeSpin.value())
                except:
                    size = 1

                if badsize or size <= 0:
                    self.intf.messageWindow(_("Illegal size"),
                                            _("The requested size as entered is "
                                              "not a valid number greater than 0."),
                                            type="warning")
                    continue
            else:
                size = self.origrequest.size

            # check that size specification is within limits
            peSize = self.parent.physicalExtends.itemData(self.parent.physicalExtends.currentIndex()).toInt()[0] / 1024
            size = lvm.clampSize(size, peSize, roundup=True)
            maximumVolumeSize = lvm.getMaxLVSize()
            if size > maximumVolumeSize:
                self.intf.messageWindow(_("Not enough space"),
                                        _("The current requested size "
                                          "(%(size)10.2f MB) is larger than "
                                          "the maximum logical volume size "
                                          "(%(maxlv)10.2f MB). "
                                          "To increase this limit you can "
                                          "create more Physical Volumes from "
                                          "unpartitioned disk space and "
                                          "add them to this Volume Group.")
                                          % {'size': size, 'maxlv': maximumVolumeSize},
                                        type="warning")
                continue

            # Get format
            origname = self.origrequest.lvname
            if not self.origrequest.exists:
                formatType = str(widget.filesystemMenu.currentText())
                format = formats.getFormat(formatType, mountpoint=mountpoint)
                self.origrequest._name = name
                try:
                    self.origrequest.size = size
                except ValueError, msg:
                    self.intf.messageWindow(_("Not enough space"),
                                            _("The size entered for this "
                                              "logical volume (%(size)d MB) "
                                              "combined with the size of the "
                                              "other logical volume(s) "
                                              "exceeds the size of the "
                                              "volume group (%(tmpvgsize)d "
                                              "MB). Please make the volume "
                                              "group larger or make the "
                                              "logical volume smaller.")
                                              % {'size': size, 'tmpvgsize': self.origrequest.vg.size},
                                            type="warning")
                    continue
                else:
                    self.origrequest.format = format
            else:
                if widget.formatRadio.isChecked():
                    formatType = str(widget.formatCombo.currentText())
                    format = formats.getFormat(formatType, mountpoint=mountpoint, device=self.origrequest.path)
                    self.origrequest.format = format
                else:
                    self.origrequest.format = self.origrequest.originalFormat

                if widget.migrateRadio.isChecked():
                    self.origrequest.format.migrate = True

                if widget.resizeRadio.isChecked():
                    self.origrequest.targetSize = widget.resizeSpin.value()

                if self.origrequest.format.mountable:
                    self.origrequest.format.mountpoint = mountpoint

                if self.origrequest.format.exists and \
                    self.origrequest.format.mountable and \
                    self.origrequest.format.mountpoint:
                    if self.storage.formatByDefault(self.origrequest) and \
                       not queryNoFormatPreExisting(self.intf):
                        continue

            # everything ok
            break

        if self.parent.parent.lvs.has_key(origname) and origname != self.origrequest.lvname:
            del self.parent.parent.lvs[origname]

        return {'name': self.origrequest.lvname,
                'size': self.origrequest.size,
                'format': self.origrequest.format,
                'originalFormat': self.origrequest.originalFormat,
                'stripes': self.origrequest.stripes,
                'logSize': self.origrequest.logSize,
                'snapshotSpace': self.origrequest.snapshotSpace,
                'exists': self.origrequest.exists}

    def destroy(self):
        if self.dialog:
            self.dialog = None

class LogicalVolumeWidget(QWidget, Ui_LogicalVolumeWidget):
    def __init__(self, parent, request, isNew=0):
        QWidget.__init__(self, parent.parent)
        self.setupUi(self)
        self.parent = parent
        self.origrequest = request
        self.isNew = isNew

        if not self.origrequest.exists:
            if self.origrequest.name:
                self.name.setText(self.origrequest.lvname)
            else:
                self.name.setText(self.parent.storage.createSuggestedVolumeGroupName(self.origrequest.vg))
        else:
            self.name.setText(self.origrequest.lvname)

        storageGuiHelpers.fillMountpointMenu(self.mountpointMenu, self.origrequest, excludes=["/boot"])
        QObject.connect(self.mountpointMenu, SIGNAL("currentIndexChanged(int)"), self.mountPointChanged)

        # This empty radioButton is hack about enabling autoExclusive formatRadio according to mountpoint.(#16446)
        self.radioButton.hide()

        # Partition Type
        if not self.origrequest.exists:
            storageGuiHelpers.fillFilesystemMenu(self.filesystemMenu, self.origrequest.format,
                                                 ignores=["mdmember", "efi", "lvmpv"])
            QObject.connect(self.filesystemMenu, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
            default_format = self.filesystemMenu.findText("ext4")
            self.filesystemMenu.setCurrentIndex(default_format)
            self.resizeRadio.hide()
            self.resizeSlider.hide()
            self.resizeSpin.hide()
            self.formatRadio.hide()
            self.formatCombo.hide()
            self.migrateRadio.hide()
            self.migrateCombo.hide()
        else:
            self.filesystemLabel.hide()
            self.filesystemMenu.hide()
            if self.origrequest.format.formattable or not self.origrequest.format.type:
                storageGuiHelpers.fillFilesystemMenu(self.formatCombo, self.origrequest.format,
                                                     ignores= ["mdmember", "lvmpv", "vfat"])
                self.formatRadio.setChecked(self.origrequest.format.formattable and not self.origrequest.format.exists)
                QObject.connect(self.formatRadio, SIGNAL("toggled(bool)"), self.formatRadioToggled)
                QObject.connect(self.formatCombo, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
            else:
                self.formatRadio.hide()
                self.formatCombo.hide()

            if self.origrequest.format.migratable and self.origrequest.format.exists:
                storageGuiHelpers.fillFilesystemMenu(self.migrateCombo, self.origrequest.format,
                                                     availables=[self.origrequest.format.migrationTarget])
                self.migrateRadio.setChecked(self.origrequest.format.migrate and not self.formatRadio.isChecked())
                QObject.connect(self.migrateCombo, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
            else:
                self.migrateRadio.hide()
                self.migrateCombo.hide()

            if self.origrequest.resizable and self.origrequest.format.exists:
                if self.origrequest.targetSize is not None:
                    value = self.origrequest.targetSize
                else:
                    value = self.origrequest.size

                reqlower = 1
                requpper = self.origrequest.maxSize
                if self.origrequest.format.exists:
                    reqlower = self.origrequest.minSize

                    if self.origrequest.type == "partition":
                        geomsize = self.origrequest.partedPartition.geometry.getSize(unit="MB")
                        if (geomsize != 0) and (requpper > geomsize):
                            requpper = geomsize

                self.resizeSpin.setMinimum(reqlower)
                self.resizeSpin.setMaximum(requpper)
                self.resizeSpin.setValue(value)
                self.resizeSlider.setMinimum(reqlower)
                self.resizeSlider.setMaximum(requpper)
                self.resizeSlider.setValue(value)
            else:
                self.resizeRadio.hide()
                self.resizeSpin.hide()
                self.resizeSlider.hide()

        #Size and maximum size
        if not self.origrequest.exists:
             maximumGrow = self.origrequest.vg.freeSpace / self.origrequest.stripes
             self.sizeSpin.setMaximum(min(lvm.getMaxLVSize(), self.origrequest.size + maximumGrow))
             self.sizeSpin.setValue(self.origrequest.size)
             self.sizeSlider.setMaximum(min(lvm.getMaxLVSize(), self.origrequest.size + maximumGrow))
             self.sizeSlider.setValue(self.origrequest.size)
        else:
            self.sizeLabel.hide()
            self.sizeSlider.hide()
            self.sizeSpin.hide()


        self.connect(self.buttonBox, SIGNAL("accepted()"), self.parent.dialog.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.parent.dialog.reject)

    def enableMountpoint(self, format):
        if format.mountable:
            self.mountpointMenu.setEnabled(True)
        else:
            self.mountpointMenu.setEnabled(False)
            self.mountpointMenu.setCurrentIndex(0)

    def formatRadioToggled(self, checked):
        if checked:
            format  = formats.getFormat(str(self.formatCombo.currentText()))
            self.enableMountpoint(format)

    def formatTypeChanged(self, index):
        format  = formats.getFormat(str(self.sender().itemText(index)))
        self.enableMountpoint(format)

    def mountPointChanged(self, index):
        if self.formatRadio.isVisible():
            self.radioButton.setChecked(True)
            self.formatRadio.setChecked(self.mountpointMenu.itemData(index).toBool())

class LogicalVolumeItem(QTreeWidgetItem):
    def __init__(self, parent, device):
        QTreeWidgetItem.__init__(self, parent)
        self._device = device
        self.setText(0, device.lvname)
        mountpoint = getattr(device.format, "mountpoint", "")
        if not mountpoint:
            mountpoint = ""
        elif not (device.format and device.format.mountable):
            mountpoint = "N/A"
        self.setText(1, mountpoint)
        self.setText(2, "%Ld" % device.size)

    @property
    def device(self):
        return self._device


