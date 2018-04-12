#!/bin/sh
set -e

python3 ./test-pbl.py -p proxy-bypass-list.txt -f test-data.csv
python3 ./test-pac.py -p proxy.pac -f test-data.csv
python3 ./test-web.py -f test-data.csv -vvv
