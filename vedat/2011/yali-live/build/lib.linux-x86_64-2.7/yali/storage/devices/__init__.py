#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from yali.storage import StorageError

class NotImplementedError(StorageError):
    pass

class AbstractDeviceError(StorageError):
    pass

class AbstractDevice(object):
    _id = 0
    _type = "abstract"

    def __init__(self, name, parents):
        self._name = name
        if parents is None:
            parents = []
        elif not isinstance(parents, list):
            raise ValueError("parents must be a list of AbstractDevice instances")
        self.parents = parents
        self.kids = 0
        self._id = AbstractDevice._id
        AbstractDevice._id += 1

        for parent in self.parents:
            parent.addChild()

    def __deepcopy__(self, memo):
        """ Create a deep copy of a Device instance.

            We can't do copy.deepcopy on parted objects, which is okay.
            For these parted objects, we just do a shallow copy.
        """
        new = self.__class__.__new__(self.__class__)
        memo[id(self)] = new
        dont_copy_attrs = ('_raidSet',)
        shallow_copy_attrs = ('_partedDevice', '_partedPartition')
        for (attr, value) in self.__dict__.items():
            if attr in dont_copy_attrs:
                setattr(new, attr, value)
            elif attr in shallow_copy_attrs:
                setattr(new, attr, copy.copy(value))
            else:
                setattr(new, attr, copy.deepcopy(value, memo))

        return new

    def __str__(self):
        s = ("%(type)s instance (%(id)s) --\n"
             "  name = %(name)s  status = %(status)s"
             "  parents = %(parents)s\n"
             "  kids = %(kids)s\n"
             "  id = %(dev_id)s\n" %
             {"type": self.__class__.__name__, "id": "%#x" % id(self),
              "name": self.name, "parents": [parent.name for parent in self.parents], "kids": self.kids,
              "status": self.status, "dev_id": self.id})
        return s

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        """ This device's name. """
        return self._name

    @property
    def isleaf(self):
        """ True if this device has no children. """
        return self.kids == 0

    @property
    def type(self):
        """ Device type. """
        return self._type

    def addChild(self):
        self.kids += 1

    def removeChild(self):
        self.kids -= 1

    def create(self, intf=None):
        """ Open, or set up, a device. """
        raise NotImplementedError("create method not implemented in AbstactDevice class.")

    def destroy(self):
        """ Close, or tear down, a device. """
        raise NotImplementedError("destroy method not implemented in AbstactDevice class.")

    def setup(self, intf=None):
        """ Open, or set up, a device. """
        raise NotImplementedError("setup method not implemented in AbstactDevice class.")

    def teardown(self):
        """ Close, or tear down, a device. """
        raise NotImplementedError("tearDown method not implemented in AbstactDevice class.")

    def createParents(self):
        """ Run create method of all parent devices. """
        for parent in self.parents:
            if not parent.exists:
                raise AbstractDeviceError("parent device does not exist", self.name)

    def setupParents(self, orig=False):
        """ Open, or set up, a device. """
        for parent in self.parents:
            parent.setup(orig=orig)

    def teardownParents(self, recursive=False):
        """ Close, or tear down, a device. """
        for parent in self.parents:
            parent.teardownParents(recursive)

    def dependsOn(self, dep):
        if dep in self.parents:
            return True

        for parent in self.parents:
            if parent.dependsOn(dep):
                return True

        return False

    @property
    def status(self):
        """ This device's status.

            For now, this should return a boolean:
                True    the device is open and ready for use
                False   the device is not open
        """
        return False

    @property
    def mediaPresent(self):
        return True
