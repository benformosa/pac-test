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

    testfailed = test_pac(args.pacfile.lstrip(), args.testfile.lstrip())

    # Set exit code based on test output
    sys.exit(testfailed)

def test_pac(pacfile, testfile):
    """Test PAC file against test data using pacparser

    Returns 0 if all tests pass, 1 if any fail"""

    # Stores the script's exit code
    testfailed = 0

    v_print(3, "Testing PAC file: {}".format(pacfile))

    # Initialise pacparser
    pacparser.init()
    pacparser.parse_pac(pacfile)

    with open(testfile, 'rt') as f:
        # Create csv reader, filtering out rows starting with '#'
        reader = csv.DictReader(filter(lambda row: row[0]!='#', f), delimiter=',')

        # Iterate over test data
        for row in reader:
            v_print(1, "\nread row: {} {}".format(row['url'], row['expected']))
            testfailed = test_url(row['url'], row['expected'])

    # Cleanup pacparser
    pacparser.cleanup()

    if(testfailed):
        print("PAC file Test Failed", file=sys.stderr)
    else:
        v_print(3, "PAC file Test Passed")

    return testfailed

def test_url(url, expected):
    """Test a URL against the PAC file.
    
    Returns 0 if the test passes, 1 if it fails"""
    # Find the proxy defined by the PAC file for the URL
    result = pacparser.find_proxy(
        url,
        urlparse(url).hostname
    )

    v_print(1, "result: {}".format(result))

    # Compare result
    if(result == expected):
        v_print(2, "OK   - {}".format(url))
        return 0
    else:
        v_print(2, "FAIL - {}".format(url))
        return 1

if __name__ == '__main__':
    main()
