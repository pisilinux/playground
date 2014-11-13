# -*- coding: utf-8 -*-
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
import yali.flags
import yali.constants
import yali.installdata

flags = yali.flags.Flags()
consts = yali.constants.Constants()
installData = yali.installdata.InstallData()

STEP_DEFAULT, STEP_BASE, STEP_FIRST_BOOT, STEP_RESCUE, STEP_OEM_INSTALL = xrange(5)

STEP_TYPE_STRINGS = {STEP_DEFAULT:"Default",
                     STEP_BASE:"Base System Installation",
                     STEP_OEM_INSTALL:"OEM Installation",
                     STEP_FIRST_BOOT:"First Boot mode",
                     STEP_RESCUE:"System Rescue mode"}

RESCUE_GRUB, RESCUE_PASSWORD, RESCUE_PISI = xrange(3)

# Auto Installation Methods
methodInstallAutomatic, methodInstallManual = range(2)

# Auto Selected Kernels
defaultKernel, paeKernel, rtKernel = range(3)

kernels = {defaultKernel:"kernel.default",
           paeKernel:"kernel.pae",
           rtKernel:"kernel.rt"}

stdout = None

stderr = None

logger = None

storage = None

bootloader = None

interface = None

mainScreen = None

storageInitialized = False

blacklistedKernelModules = []

packagesToInstall = []

socket = None

link = None

mountCount = {}

collections = None
