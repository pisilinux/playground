#!/bin/sh
cd "/usr/bin/"
./xdg-open http://admin@localhost:8080/gui/ $*
exit $?

