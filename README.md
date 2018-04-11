# pac-test

pac-test is a set of tools for testing [proxy PAC files](https://en.wikipedia.org/wiki/Proxy_auto-config) and [Proxy Bypass Lists](https://technet.microsoft.com/en-us/library/cc939852.aspx#EBAA).

## Getting Started

Clone this project and replace the files `proxy.pac` and `proxy-bypass-list.txt` with your own proxy PAC file and Proxy Bypass list.

Replace the file `test-data.csv` with your test data.

## Test data file format

The test data is a CSV with two columns

| Column     | Detail |
|------------|--------|
| `url`      | URL to test |
| `expected` | Expected output, in the format returned by a PAC file's `FindProxyForURL(url,host)` function.

```csv
url,expected
http://example.com,DIRECT
# example.net should use proxy
http://example.net,PROXY proxy:8080
```

## Running

Run `test.sh` to run both tests.

### Running with Docker

To build and run with Docker:

```sh
docker build -t pac-test .
docker run --rm pac-test
```

## Prerequisites

Requires Python and the [pacparser](https://github.com/manugarg/pacparser) Python module.

Install pacparser with `pip install pacparser`, or on Debian with `apt-get install python-pacparser`

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
