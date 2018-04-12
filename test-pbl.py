import argparse
import csv
import pblparser
import sys

def main():
    # Commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxybypasss', metavar='FILE', type=str,
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

    testpassed = 0

    v_print(3, "Testing Proxy Bypass List: {}".format(args.proxybypasss.lstrip()))

    # Initialise pblparser
    pblparser.set_proxy(args.proxystring.lstrip())
    pblparser.parse_pbl(args.proxybypasss.lstrip())

    v_print(1, pblparser.get_pbl())
    v_print(1, "")

    with open(args.testfile.lstrip(), 'rt') as f:
        # Create csv reader, filtering out rows starting with '#'
        reader = csv.DictReader(filter(lambda row: row[0]!='#', f), delimiter=',')

        for row in reader:
            v_print(1, "read row: {} {}".format(row['url'], row['expected']))

            result = pblparser.find_proxy(row['url'])

            v_print(1, "result: {}".format(result))
            
            # Compare result and output
            if(result == row['expected']):
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

if __name__ == '__main__':
    main()
