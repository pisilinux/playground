#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from guppy import hpy

h = hpy()

l = []
for i in range(1000):
    l.append(random.randint(0, 1000))

print h.heap()
raw_input()
