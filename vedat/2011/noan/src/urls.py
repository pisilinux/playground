from django.conf.urls.defaults import patterns, include, url
from packages.views import LastUpdatedPackages

from feeds import PackageFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
import os.path

feeds_patterns = patterns('',
    #(r'^$',          'public.views.feeds', {}, 'feeds-list'),  # feed list
    (r'^packages/$', PackageFeed()),
    #(r'^packages/(?P<arch>[A-z0-9]+)/$',
        #PackageFeed()),
    #(r'^packages/(?P<arch>[A-z0-9]+)/(?P<repo>[A-z0-9\-]+)/$',
        #PackageFeed()),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^packages/', include('packages.urls')),
    url(r'^feeds/', include(feeds_patterns)),
    url(r'^feeds/packages/$', LastUpdatedPackages()),
)

if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve',{'document_root':
                                               os.path.join(settings.DEPLOY_PATH, 'media')}),
                            (r'^jsi18n/$',   'django.views.i18n.null_javascript_catalog'), )
