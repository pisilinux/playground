#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import traceback
from time import time

time_counter = 0
start_time = time()
last_time = time()

def _time():
    global last_time, time_counter
    trace = list(traceback.extract_stack())
    diff = time() - start_time
    print ('%s ::: %s:%s' % (time_counter,
                             trace[-2][0].split('/')[-1],
                             trace[-2][1])), diff, diff - last_time
    last_time = diff
    time_counter += 1

