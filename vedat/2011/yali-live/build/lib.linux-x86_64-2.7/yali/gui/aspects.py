# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from pyaspects.meta import MetaAspect
import yali.context as ctx

##
# Disables navigation buttons before method.
class DisableNavButtonsAspect:

    __metaclass__ = MetaAspect
    name = "disableNavButtons"

    def before(self, wobj, data, *args, **kwargs):
        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

    def after(self, wobj, data, *args, **kwargs):
        pass

disableNavButtonsAspect = DisableNavButtonsAspect()

##
# Enable navigation buttons before method.
class EnableNavButtonsAspect:

    __metaclass__ = MetaAspect
    name = "enableNavButtons"

    def before(self, wobj, data, *args, **kwargs):
        ctx.mainScreen.enableNext()
        ctx.mainScreen.enableBack()

    def after(self, wobj, data, *args, **kwargs):
        pass

enableNavButtonsAspect = EnableNavButtonsAspect()

class LoggerAspect:
    __metaclass__ = MetaAspect
    name = "LoggerAspect"

    def __init__(self, logger ):
        self.logger = logger

    def before(self, wobj, data, *args, **kwargs):
        met_name = data['original_method_name']
        class_ = str(data['__class__'])[8:-2]
        fun_str = "%s%s from %s" % (met_name, args, class_)
        self.logger.debug("call, %s" % fun_str,1,+1)

    def after(self, wobj, data, *args, **kwargs):
        met_name = data['original_method_name']
        fun_str = "%s%s" % (met_name, args)
        self.logger.debug("left, %s" % fun_str,1,-1)

loggerAspect = LoggerAspect(ctx.logger)
