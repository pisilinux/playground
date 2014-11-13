#!/bin/bash

PYLINT="pylint --rcfile=yali.lint -d C0111 -d C0301"

for module in $(find $1 -name "*.py"); do
    $PYLINT $module 2>/dev/null > `echo $module | cut -d "." -f1`.pylint
done
