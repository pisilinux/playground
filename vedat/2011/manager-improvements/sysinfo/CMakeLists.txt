project(kio_sysinfo)

# search packages used by KDE
find_package(KDE4 REQUIRED)
include (UsePkgConfig)
include (KDE4Defaults)
include (MacroLibrary)
include(MacroOptionalAddSubdirectory)

PKGCONFIG(dbus-1 DBUS_INCLUDE_DIR DBUS_LINK_DIR DBUS_LINK_FLAGS DBUS_CFLAGS)
add_definitions(${DBUS_CFLAGS})

add_definitions (${QT_DEFINITIONS} ${QT_QTDBUS_DEFINITIONS} ${KDE4_DEFINITIONS})
include_directories (${QDBUS_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR} ${KDE4_INCLUDES})

add_subdirectory(src)

#process and install translations
find_package(Gettext REQUIRED)
file(GLOB po_files po/*.po)
set(_gmoFiles)
foreach (_current_PO_FILE ${po_files})
   get_filename_component(_basename ${_current_PO_FILE} NAME_WE)
   set(_lang ${_basename})
   set(_gmoFile ${CMAKE_CURRENT_BINARY_DIR}/${_basename}.gmo)
   add_custom_command(OUTPUT ${_gmoFile}
      COMMAND ${GETTEXT_MSGFMT_EXECUTABLE} -o ${_gmoFile} ${_current_PO_FILE}
      WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
      DEPENDS ${_current_PO_FILE}
   )
   list(APPEND _gmoFiles ${_gmoFile})
   install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${_basename}.gmo DESTINATION ${LOCALE_INSTALL_DIR}/${_lang}/LC_MESSAGES/ RENAME kio_sysinfo.mo)
endforeach (_current_PO_FILE ${po_files})
add_custom_target(pofiles ALL DEPENDS ${_gmoFiles})
