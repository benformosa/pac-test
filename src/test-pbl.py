#!/usr/bin/env python3
"""Test output of pblparser against test data"""

import argparse
import csv
import sys

import pblparser

def main():
    # Commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxybypass', metavar='FILE', type=str,
            default='proxy-bypass-list.txt',
            help="Path to proxy bypass list to test")
    parser.add_argument('-f', '--testfile', metavar='FILE', type=str,
            default='test-data.csv',
            help="Path to CSV test data file.")
    parser.add_argument('-s', '--proxystring', metavar='STRING', type=str,
            default='PROXY proxy:8080',
            help="String to return when proxy is set")
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

    testfailed = test_pbl(args.proxybypass.lstrip(), args.testfile.lstrip(), args.proxystring.lstrip())

    # Set exit code based on test output
    sys.exit(testfailed)

def test_pbl(proxybypass, testfile, proxystring):
    """Test Proxy Bypass list against test data using pblparser.
    
    Returns 0 if all tests pass, 1 if any fail"""

    # Stores the script's exit code
    testfailed = 0

    v_print(3, "Testing Proxy Bypass List: {}".format(proxybypass))

    # Initialise pblparser
    pblparser.set_proxy(proxystring)
    pblparser.parse_pbl(proxybypass)

    v_print(1, pblparser.get_pbl())
    v_print(1, "")

    with open(testfile, 'rt') as f:
        # Create csv reader, filtering out rows starting with '#'
        reader = csv.DictReader(filter(lambda row: row[0]!='#', f), delimiter=',')

        # Iterate over test data
        for row in reader:
            v_print(1, "\nread row: {} {}".format(row['url'], row['expected']))
            testfailed = test_url(row['url'], row['expected'])

    if(testfailed):
        print("Proxy Bypass list Test Failed", file=sys.stderr)
    else:
        v_print(3, "Proxy Bypass list Test Passed")

    return testfailed

def test_url(url,expected):
    """Test a URL against the Proxy Bypass list.
    
    Returns 0 if the test passes, 1 if it fails"""
    # Find the proxy defined by the PBL for the URL
    result = pblparser.find_proxy(url)

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
