#!/usr/bin/env python3
"""Test connection to each URL in test data"""

from urllib.parse import urlparse
import argparse
import csv
import requests
import sys

def main():
    # Commandline arguments
    parser = argparse.ArgumentParser()
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

    testfailed = test_web(args.testfile.lstrip())

    # Set exit code based on test output
    sys.exit(testfailed)

def test_web(testfile):
    """Test web connections against test data

    Returns 0 if all tests pass, 1 if any fail"""

    # Stores the script's exit code
    testfailed = 0

    v_print(3, "Testing web connections")

    with open(testfile, 'rt') as f:
        # Create csv reader, filtering out rows starting with '#'
        reader = csv.DictReader(filter(lambda row: row[0]!='#', f), delimiter=',')

        for row in reader:
            v_print(1, "\nread row: {} {}".format(row['url'], row['expected']))
            testfailed = test_url(row['url'], row['expected'])

    if(testfailed):
        print("Web Test Failed", file=sys.stderr)
    else:
        v_print(3, "Web Test Passed")

    return testfailed

def test_url(url, proxystring):
    """Connect to a URL

    Returns 0 if the test passes, 1 if it fails"""

    # Attempt to connect to the URL
    try:
        result = get_http_status_code(url, get_proxy(proxystring))
    except Exception as e:
        v_print(1, "Error connecting to URL: {}".format(e))
        result = 'error'

    v_print(1, "result: {}".format(result))
    
    # Compare result
    if(result == requests.codes.ok):
        v_print(2, "OK   - {}".format(url))
        return 0
    else:
        v_print(2, "FAIL - {}".format(url))
        return 1

def get_proxy(proxystring):
    """Convert a proxy string back into a host:port string"""

    proxyprefix = "PROXY "
    if(proxystring.startswith(proxyprefix)):
        # Remove the prefix, any whitespace, and return the first proxy
        return proxystring.replace(proxyprefix, '').replace(' ', '').partition(';')[0]
    elif(proxystring.startswith("DIRECT")):
        # Explicit is better than implicit
        return ''
    else:
        return ''

def get_http_status_code(url, proxy=''):
    """Retreives the status code of a url by requesting HEAD data. Uses the proxy if set."""

    proxies = {}
    if(proxy):
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    r = requests.get(url, proxies=proxies, timeout=2)
    return r.status_code

if __name__ == '__main__':
    main()
