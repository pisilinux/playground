#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 Aerva, Inc
# Copyright 2010 Gavin Bisesi
# Copyright 2010 Mark Renouf
# Copyright 2011 Gökmen Göksel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Enum(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.__class__._values[value] = self
        self.__class__._names[name] = self

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(%d, \"%s\")" % (self.__class__.__name__, self.value, self.name)

    @classmethod
    def from_value(cls, value):
        return cls._values[value]

def new(name, **values):
    ENUM = type(name, (Enum, object, ), dict(_values={},_names={}))
    for (name, value) in values.iteritems():
        setattr(ENUM, name, ENUM(name, value))
    return ENUM

