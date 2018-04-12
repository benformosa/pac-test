#!/bin/sh
set -e

python ./test-pbl.py -p proxy-bypass-list.txt -f test-data.csv
python ./test-pac.py -p proxy.pac -f test-data.csv
