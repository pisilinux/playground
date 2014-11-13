from django.conf.urls.defaults import patterns, url, include
from packages.views import details, search, files

package_patterns = patterns('packages.views',
    url(r'^$', details),
    url(r'^files/$', files),
)
urlpatterns = patterns('',
        url(r'^$', search),
        url(r'^(?P<page>\d+)/$', search),
        url(r'^(?P<dist>[A-z0-9\-.]+)/(?P<arch>[A-z0-9]+)/(?P<name>[A-z0-9\-+.]+)/',
            include(package_patterns)),
)
