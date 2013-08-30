#!/bin/bash

LOCAL_DIR="$HOME"/.eagle
mkdir -p "$LOCAL_DIR"
cp -aru /opt/eagle-6.5.0/* "$LOCAL_DIR"
exec "$LOCAL_DIR"/bin/eagle "$@"
