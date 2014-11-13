#!/bin/bash

LANGS='ca de es fr it nl pl pt_BR sv tr'

xgettext src/*.cpp -o po/sysinfo.pot -ki18n -ktr2i18n -kI18N_NOOP -ktranslate -kaliasLocale

for lang in $LANGS
do
    echo "updating $lang"
    msgmerge -U po/$lang.po po/sysinfo.pot
done

