SUBDIRS = . about

INCLUDES = $(all_includes) `pkg-config --cflags hal`

kde_module_LTLIBRARIES = kio_sysinfo.la libksysinfopart.la

kio_sysinfo_la_SOURCES = sysinfo.cpp
kio_sysinfo_la_LIBADD = $(LIB_KIO) -lhd -lGL
kio_sysinfo_la_LDFLAGS = -module -avoid-version $(all_libraries) $(KDE_PLUGIN) $$(pkg-config --libs hal)

kde_services_DATA = sysinfo.protocol ksysinfopart.desktop

libksysinfopart_la_SOURCES = ksysinfopart.cpp
libksysinfopart_la_LIBADD = -lkhtml $(LIB_KPARTS)
libksysinfopart_la_LDFLAGS = $(all_libraries) $(KDE_PLUGIN)

xdg_apps_DATA = kfmclient_sysinfo.desktop

messages:
	$(XGETTEXT) *.cpp -o $(podir)/kio_sysinfo.pot

METASOURCES = AUTO

apps_DATA = x-sysinfo.desktop
appsdir = $(kde_mimedir)/application

