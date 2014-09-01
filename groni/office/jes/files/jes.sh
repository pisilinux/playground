#!/bin/sh
#
# Startscript for Jes on Pardus GNU/Linux
#

echo "Starting jes ..."

export GDK_NATIVE_WINDOWS=true

exec java -jar /usr/share/jes/jes.jar

exit 0 
