#!/bin/bash

LANGUAGES=`ls po/*.po`
TEMP=`mktemp`
set -x

xgettext -L "python" --keyword=__tr --keyword=_ --keyword=i18n network -o po/python-networkmanager.pot
for lang in $LANGUAGES
do
    #msgcat --use-first -o $TEMP $lang po/python-networkmanager.pot
    msgmerge -q -o $TEMP $lang po/python-networkmanager.pot
    cat $TEMP > $lang
done
rm -f $TEMP
