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

    testpassed = 0

    with open(args.testfile.lstrip(), 'rt') as f:
        # Create csv reader, filtering out rows starting with '#'
        reader = csv.DictReader(filter(lambda row: row[0]!='#', f), delimiter=',')

        for row in reader:
            v_print(1, "read row: {} {}".format(row['url'], row['expected']))

            try:
                result = get_http_status_code(row['url'], get_proxy(row['expected']))
            except:
                v_print(2, "Error connecting to URL")
                result = 'error'

            v_print(1, "result: {}".format(result))
            
            # Compare result and output
            if(result == requests.codes.ok):
                v_print(2, "OK   - {}".format(row['url']))
            else:
                testpassed = 1
                v_print(2, "FAIL - {}".format(row['url']))

            v_print(1, "")

    if(testpassed):
        v_print(3, "Test Failed")
    else:
        v_print(3, "Test Passed")

    # Set exit code based on test output
    sys.exit(testpassed)

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

def get_http_status_code(url, proxy):
    """Retreives the status code of a url by requesting HEAD data"""

    proxies = {}
    if(proxy):
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    r = requests.get(url, proxies=proxies)
    return r.status_code

if __name__ == '__main__':
    main()
