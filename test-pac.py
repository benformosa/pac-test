#!/usr/bin/env python3
"""Test output of pacparser against test data"""

import argparse
import csv
import pacparser
import sys
from urllib.parse import urlparse

def main():
    # Commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pacfile', metavar='PACFILE', type=str,
            default='proxy.pac',
            help="Path to PAC file to test")
    parser.add_argument('-f', '--testfile', metavar='FILE', type=str,
            default='test-data.csv',
            help="Path to CSV test data file.")
    parser.add_argument('-v', '--verbosity', action="count",
            help="increase output verbosity")
    args = parser.parse_args()

    # Set up v_print function for verbose output
    if args.verbosity:
        def _v_print(*verb_args):
            if verb_args[0] > (3 - args.verbosity):
                print(verb_args[1])
    else:
        _v_print = lambda *a: None  # do-nothing function

    global v_print
    v_print = _v_print

    testfailed = 0

    v_print(3, "Testing PAC file: {}".format(args.pacfile.lstrip()))

    # Initialise pacparser
    pacparser.init()
    pacparser.parse_pac(args.pacfile.lstrip())

    with open(args.testfile.lstrip(), 'rt') as f:
        # Create csv reader, filtering out rows starting with '#'
        reader = csv.DictReader(filter(lambda row: row[0]!='#', f), delimiter=',')

        for row in reader:
            v_print(1, "read row: {} {}".format(row['url'], row['expected']))

            result = pacparser.find_proxy(
                row['url'],
                urlparse(row['url']).hostname
            )

            v_print(1, "result: {}".format(result))

            # Compare result and output
            if(result == row['expected']):
                v_print(2, "OK   - {}".format(row['url']))
            else:
                testfailed = 1
                v_print(2, "FAIL - {}".format(row['url']))

            v_print(1, "")

    # Cleanup pacparser
    pacparser.cleanup()

    if(testfailed):
        print("PAC file Test Failed", file=sys.stderr)
    else:
        v_print(3, "PAC file Test Passed")

    # Set exit code based on test output
    sys.exit(testfailed)

if __name__ == '__main__':
    main()
