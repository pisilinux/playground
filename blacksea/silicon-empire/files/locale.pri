# This is an edited locale.pri of the minitunes projects
# This voodoo comes from the Arora project
INCLUDEPATH += $$PWD
DEPENDPATH += $$PWD

# ls -1 *.ts | tr '\n' ' '
TRANSLATIONS = lang-en.ts lang-fa.ts lang-es.ts lang-de.ts lang-zh_TW.ts lang-tr.ts

isEmpty(QMAKE_LRELEASE) { 
    win32:QMAKE_LRELEASE = $$[QT_INSTALL_BINS]\lrelease.exe
    else:QMAKE_LRELEASE = $$[QT_INSTALL_BINS]/lrelease
}
updateqm.input = TRANSLATIONS

unix:!macx {
    updateqm.output = ../../build-linux/share/silicon/languages/${QMAKE_FILE_BASE}.qm
    updateqm.commands = $$QMAKE_LRELEASE \
        ${QMAKE_FILE_IN} \
        -qm \
        ../../build-linux/share/silicon/languages/${QMAKE_FILE_BASE}.qm
}

macx {
    updateqm.output = ../../build-osx/share/silicon/languages/${QMAKE_FILE_BASE}.qm
    updateqm.commands = $$QMAKE_LRELEASE \
        ${QMAKE_FILE_IN} \
        -qm \
        ../../build-osx/share/silicon/languages/${QMAKE_FILE_BASE}.qm
}

win32 {
    updateqm.output = ../../build-windows/share/silicon/languages/${QMAKE_FILE_BASE}.qm
    updateqm.commands = $$QMAKE_LRELEASE \
        ${QMAKE_FILE_IN} \
        -qm \
        ../../build-windows/share/silicon/languages/${QMAKE_FILE_BASE}.qm
}

updateqm.CONFIG += no_link \
    target_predeps
QMAKE_EXTRA_COMPILERS += updateqm

