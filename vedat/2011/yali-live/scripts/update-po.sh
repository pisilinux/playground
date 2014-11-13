#!/bin/bash

LANGUAGES=`ls po/*.po`
TEMP=`mktemp`
set -x

xgettext -L "python" --keyword=__tr --keyword=_ --keyword=i18n yali/gui/Ui/*.py yali/gui/*.py yali/storage/*.py yali/storage/devices/*.py yali/storage/library/*.py yali/storage/formats/*.py yali/*.py -o po/yali.pot
for lang in $LANGUAGES
do
    #msgcat --use-first -o $TEMP $lang po/yali.pot
    msgmerge -q -o $TEMP $lang po/yali.pot
    cat $TEMP > $lang
done
rm -f $TEMP
