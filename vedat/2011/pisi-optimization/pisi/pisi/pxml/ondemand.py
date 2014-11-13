# -*- coding: utf-8 -*-

import pisi

class OnDemandError(pisi.Error):
    pass

class OnDemandNode(object):
    def __init__(self, decode, node, where):
        self.decode_function = decode
        self.node = node
        self.error_function = None
        self.where = where

    def decode(self):
        # print "decoding", self.where # debuginfo
        errs = []

        r = self.decode_function(self.node, errs, self.where, True)

        if self.error_function:
            # print "checking", self.where # debuginfo
            if r:
                errs.extend(self.error_function(r, self.where))

        if errs:
            raise OnDemandError(*errs)

        return r

    def decodeAll(self):
        pass

class OnDemandList(list):

    def __init__(self):
        super(OnDemandList, self).__init__()
        self.undecoded_count = 0
        self.errors_item_function = None

    def __getitem__(self, y):
        item = super(OnDemandList, self).__getitem__(y)

        if isinstance(item, OnDemandNode):
            item.error_function = self.errors_item_function
            item = item.decode()
            super(OnDemandList, self).__setitem__(y, item)
            self.undecoded_count -= 1

        return item

    def decodeall_run_f(self, y, f):
        self.decodeAll()
        if isinstance(y, OnDemandList):
            y.decodeAll()

        function = getattr(super(OnDemandList, self), f)
        return function(y)

    def append(self, y):
        if isinstance(y, OnDemandNode):
            self.undecoded_count += 1
        return super(OnDemandList, self).append(y)

    def count(self, y):
        self.decodeAll()
        return super(OnDemandList, self).count(y)

    def extend(self, i):
        if isinstance(i, OnDemandList):
            self.undecoded_count += i.undecoded_count
        else:
            for x in i:
                if isinstance(x, OnDemandNode):
                    self.undecoded_count += 1

        return super(OnDemandList, self).extend(i)

    def index(self, value, start = 0, stop = -1):
        self.decodeAll()
        return super(OnDemandList, self).index(value, start, stop)

    def insert(self, index, o):
        if isinstance(y, OnDemandNode):
            self.undecoded_count += 1
        return super(OnDemandList, self).insert(index, o)

    def pop(self, index = -1):
        a = super(OnDemandList, self).pop(index)
        if isinstance(a, OnDemandNode):
            a = a.decode()
        return a

    def remove(self, value):
        self.decodeAll()
        return super(OnDemandList, self).remove(value)

    def sort(self, cmp = None, key=None, reverse=False):
        self.decodeAll()
        return super(OnDemandList, self).sort(cmp, key, reverse)

    def __add__(self, y):
        return self.decodeall_run_f(y, '__add__')

    def __contains__(self, y):
        if self.undecoded_count > 0:
            self.decodeAll()
        return super(OnDemandList, self).__contains__(y)

    def __delitem__(self, y):
        # print "delitem", y
        if not self.isDecoded(y):
            self.undecoded_count -= 1
        return super(OnDemandList, self).__delitem__(y)

    def __delslice__(self, i, j):
        # print "delslice", i, j
        if j > len(self):
            j = len(self)

        for x in xrange(i, j):
            if not self.isDecoded(x):
                self.undecoded_count -= 1

        return super(OnDemandList, self).__delslice__(i, j)

    def __eq__(self, y):
        if isinstance(y, list):
            # print "__eq__" # debuginfo
            return self.decodeall_run_f(y, '__eq__')

        return False

    def __ge__(self, y):
        # print "__ge__" # debuginfo
        return self.decodeall_run_f(y, '__ge__')

    def __getslice__(self, i, j):
        if j > len(self):
            j = len(self)

        # Decode slice
        for x in xrange(i, j):
            self.__getitem__(x)

        return super(OnDemandList, self).__getslice__(i, j)

    def __gt__(self, y):
        # print "__gt__" # debuginfo
        return self.decodeall_run_f(y, '__gt__')

    def __iadd__(self, y):
        # print "__iadd__" # debuginfo
        return self.decodeall_run_f(y, '__iadd__')

    def __imul__(self, y):
        # print "__imul__" # debuginfo
        return self.decodeall_run_f(y, '__imul__')

    def __iter__(self):
        for i in xrange(len(self)):
            yield self.__getitem__(i)

    def __le__(self, y):
        # print "__le__" # debuginfo
        return self.decodeall_run_f(y, '__le__')

    def __lt__(self, y):
        # print "__lt__" # debuginfo
        return self.decodeall_run_f(y, '__lt__')

    def __mul__(self, y):
        # print "__mul__" # debuginfo
        return self.decodeall_run_f(y, '__mul__')

    def __ne__(self, y):
        if isinstance(y, list):
            # print "__ne__" # debuginfo
            return self.decodeall_run_f(y, '__ne__')

        return True

    def __reduce__(self):
        # print "reduce"
        self.decodeAll()
        if hasattr(self, 'errors_item_function'):
            delattr(self, 'errors_item_function')
        return super(OnDemandList, self).__reduce__()

    def __reduce_ex__(self, protocol):
        # print "reduce_ex"
        self.decodeAll()
        if hasattr(self, 'errors_item_function'):
            delattr(self, 'errors_item_function')
        return super(OnDemandList, self).__reduce_ex__(protocol)

    # __repr__(self)

    def __reversed__(self):
        for i in xrange(len(self)-1, -1, -1):
            yield self.__getitem__(i)

    def __rmul__(self, y):
        # print "__rmul__" # debuginfo
        return self.decodeall_run_f(y, '__rmul')

    def __setitem__(self, i, y):
        if not self.isDecoded(i):
            self.undecoded_count -= 1

        if isinstance(y, OnDemandNode):
            self.undecoded_count += 1

        return super(OnDemandList, self).__setitem__(i, y)

    def isDecoded(self, y):
        item = super(OnDemandList, self).__getitem__(y)
        return not isinstance(item, OnDemandNode)

    def safeIter(self):
        class iterator(object):
            def __init__(self, obj):
                self.obj = obj
                self.index = -1

            def __iter__(self):
                return self

            def next(self):
                self.index+=1
                if self.index >= len(self.obj):
                    raise StopIteration
                # print len(self.obj), self.index #

                while not self.obj.isDecoded(self.index):
                    self.index += 1
                    if self.index >= len(self.obj):
                        raise StopIteration

                return self.obj[self.index]

        return iterator(self)

    def decodeAll(self):
        if self.undecoded_count > 0:
            for x in xrange(len(self)):
                i = self.__getitem__(x)
                if hasattr(i, 'decodeAll'):
                    i.decodeAll()
