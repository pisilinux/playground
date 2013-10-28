#!/bin/sh
cd "/opt/utorrent-server-v3_0/"
./utserver -settingspath /opt/utorrent-server-v3_0/ $*
exit $?

