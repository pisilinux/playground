#!/bin/bash

LANGUAGES=`ls po/*.po`

for lang in $LANGUAGES
do
    echo -en $lang "\t"
    msgfmt -cv $lang
done
rm messages.mo

