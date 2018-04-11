import argparse
import csv
import pacparser
import sys

def main():
    # Commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pacfile', metavar='PACFILE', type=str,
            default='proxy.pac',
            help="Path to PAC file to test")
    parser.add_argument('-f', '--testfile', metavar='FILE', type=str,
            default='test-data.csv',
            help="Path to CSV test data file.")
    args = parser.parse_args()

    testpassed = 0

    print("Testing PAC file: {}".format(args.pacfile.lstrip()))

    # Initialise pacparser
    pacparser.init()
    pacparser.parse_pac(args.pacfile.lstrip())

    with open(args.testfile.lstrip(), 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            host = line[0]
            expected = line[1]

            #print("read line: {} {}".format(host, expected))

            result = pacparser.find_proxy(
                "http://{}".format(host),
                host
            )

            #print("result: {}".format(result))

            # Compare result and output
            if(result == expected):
                print("OK   - {}".format(host))
            else:
                testpassed = 1
                print("FAIL - {}".format(host))

    # Cleanup pacparser
    pacparser.cleanup()

    if(testpassed):
        print("Test Failed")
    else:
        print("Test Passed")

    # Set exit code based on test output
    sys.exit(testpassed)

if __name__ == '__main__':
    main()
