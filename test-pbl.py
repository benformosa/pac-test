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
    args = parser.parse_args()

    testpassed = 0

    print("Testing Proxy Bypass List: {}".format(args.proxybypasss.lstrip()))

    # Initialise pblparser
    pblparser.set_proxy(args.proxystring.lstrip())
    pblparser.parse_pbl(args.proxybypasss.lstrip())

    # VERBOSE
    # print(pblparser.get_pbl())
    # print("")

    with open(args.testfile.lstrip(), 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            host = line[0]
            expected = line[1]

            # VERBOSE
            # print("read line: {} {}".format(host, expected))

            result = pblparser.find_proxy(host)

            # VERBOSE
            # print("result: {}".format(result))
            
            # Compare result and output
            if(result == expected):
                print("OK   - {}".format(host))
            else:
                testpassed = 1
                print("FAIL - {}".format(host))

            # VERBOSE
            # print("")

    if(testpassed):
        print("Test Failed")
    else:
        print("Test Passed")

    # Set exit code based on test output
    sys.exit(testpassed)

if __name__ == '__main__':
    main()
