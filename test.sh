#!/bin/sh

python ./test-pel.py -p proxy-exception-list.txt -f test-data.csv
python ./test-pac.py -p proxy.pac -f test-data.csv
