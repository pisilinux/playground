#!/bin/bash

LOCAL_DIR="$HOME"/.eagle
LOCAL_DIR1="$HOME"
mkdir -p "$LOCAL_DIR"
cp -aru /opt/eagle-6.5.0/* "$LOCAL_DIR"
cp -aru /opt/eagle-6.5.0/bin/freeware.key "$LOCAL_DIR1"
exec "$LOCAL_DIR"/bin/eagle "$@"
