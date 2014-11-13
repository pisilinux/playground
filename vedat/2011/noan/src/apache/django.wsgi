import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'packages_pardus.settings'

sys.path.append("/home/pars/packages_pardus")
sys.path.append("/home/pars")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

