#!/bin/sh
set -e

python3 ./test-pbl.py
python3 ./test-pac.py
python3 ./test-web.py
