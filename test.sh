#!/bin/sh
set -e

python3 src/test-pbl.py
python3 src/test-pac.py
python3 src/test-web.py
