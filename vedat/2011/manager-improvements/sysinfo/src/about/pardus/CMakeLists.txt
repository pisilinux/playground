install( FILES
    images/background.png
    images/dirs.png
    images/hdd.png
    images/inner-bcg.png
    images/network.png
    images/cpu.png
    images/display.png
    images/hdds.png
    images/launch.png
    images/mem.png
    images/sysinfo.png

    DESTINATION ${DATA_INSTALL_DIR}/sysinfo/about/images
)

install (FILES
   index.html
   style.css
   DESTINATION ${DATA_INSTALL_DIR}/sysinfo/about
)
