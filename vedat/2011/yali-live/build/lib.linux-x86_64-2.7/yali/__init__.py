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
import os
import logging
import logging.handlers
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

import yali.context as ctx

class Error(Exception):
    pass

def init_logging():
    log_dir = os.path.join(ctx.consts.log_dir, ctx.consts.log_file)
    if os.access(ctx.consts.log_dir, os.W_OK):
        handler = logging.handlers.RotatingFileHandler(log_dir)
        formatter = logging.Formatter('%(asctime)-12s: %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        ctx.logger = logging.getLogger('yali')
        ctx.logger.addHandler(handler)
        ctx.loghandler = handler
        ctx.logger.setLevel(logging.DEBUG)


init_logging()
