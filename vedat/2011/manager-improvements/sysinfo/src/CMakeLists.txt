#add_subdirectory(about/pardus)
#add_subdirectory(about/2009)
add_subdirectory(about/2011)

set(kio_sysinfo_SRCS
   sysinfo.cpp
)

kde4_add_plugin(kio_sysinfo ${kio_sysinfo_SRCS})
target_link_libraries(kio_sysinfo ${KDE4_KIO_LIBS} ${KDE4_SOLID_LIBS} GL ${X11_LIBRARIES})
if (HAVE_HD_H)
   target_link_libraries(kio_sysinfo hd)
endif (HAVE_HD_H)

install(TARGETS kio_sysinfo DESTINATION ${PLUGIN_INSTALL_DIR})

set(libksysinfopart_SRCS
   ksysinfopart.cpp
)

kde4_add_plugin(libksysinfopart ${libksysinfopart_SRCS})
target_link_libraries(libksysinfopart ${KDE4_KHTML_LIBS} ${KDE4_KPART_LIBS} ${KDE4_SOLID_LIBS})
install(TARGETS libksysinfopart DESTINATION ${PLUGIN_INSTALL_DIR})

install( FILES sysinfo.protocol ksysinfopart.desktop DESTINATION  ${SERVICES_INSTALL_DIR} )
install( FILES kfmclient_sysinfo.desktop DESTINATION ${XDG_APPS_INSTALL_DIR} )
install( FILES sysinfo.desktop DESTINATION ${XDG_APPS_INSTALL_DIR} )

find_package(SharedMimeInfo REQUIRED)
install(FILES x-sysinfo.xml DESTINATION ${XDG_MIME_INSTALL_DIR})
update_xdg_mimetypes(${XDG_MIME_INSTALL_DIR})
