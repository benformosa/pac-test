# pac-test

pac-test is a set of tools for testing [proxy PAC files](https://en.wikipedia.org/wiki/Proxy_auto-config) and [Proxy Bypass Lists](https://technet.microsoft.com/en-us/library/cc939852.aspx#EBAA).

## Getting Started

Clone this project and replace the files `proxy.pac` and `proxy-bypass-list.txt` with your own proxy PAC file and Proxy Bypass list.  
Replace the file `test-data.csv` with your test data. See [Test data file format](#test-data-file-format)

Run `test.sh` to run all tests.

To build and run with Docker:

```sh
docker build -t pac-test .
docker run --rm pac-test
```

## Running

Each test can be run individually.

| Test | Script |
|------|--------|
| PAC file | `src/test-pac.py` |
| Proxy Bypass list | `src/test-pbl.py` |
| Web connectivity | `src/test-web.py` |

Use the `-h` argument on each script to see available command line options.

## Requirements

Requires Python 3 with [pacparser](http://pacparser.manugarg.com/) and [requests](http://docs.python-requests.org/en/master/) modules.

To install requirements with pip: `pip install -r requirements.txt`  
To install requirements with apt on Debian: `apt-get install python3-pacparser python3-requests`

## Test data file format

The test data is a CSV with two columns. The first row should be headers. Lines beginning with `#` are treated as comments.

Note that Proxy Bypass lists do not specify which proxy to use, just whether it should or not. To match the behaviour of `pacparser`, ensure that you set the `--proxystring` argument of `test-pbl.py` to match the `expected` column.

| Column     | Detail |
|------------|--------|
| `url`      | URL to test |
| `expected` | Expected output, in the format returned by a PAC file's `FindProxyForURL(url,host)` function.

Example:

```csv
url,expected
http://example.com,DIRECT
# example.net should use proxy
http://example.net,PROXY proxy:8080
```

## Proxy Bypass list file format

`pblparser.py` attempts to simulate the behaviour of Internet Explorer, as documented in Microsoft's Internet Explorer 5 Resource Kit: [Working with Proxy Servers](https://technet.microsoft.com/en-us/library/cc939852.aspx#EBAA)

* A Proxy Bypass list file is made up of one or more Proxy Bypass entries, separated by semicolons (`;`).
* A Proxy Bypass entry is a hostname or IP address
* Parts of the hostname may be replaced by the wildcard `*`, which matches zero or more characters
  * NOTE: pac-test uses [fnmatch](https://docs.python.org/library/fnmatch.html) to implement wildcards. fnmatch supports other special characters not supported by Proxy Bypass lists.
* A Proxy Bypass entry may optionally begin with a protocol.
  * NOTE: Proxy Bypass list only supports protocols `http://`, `https://`, `ftp://` and `gopher://`. pac-test uses [urlparse](https://docs.python.org/2/library/urlparse.html), which supports more protocol types.
* A Proxy Bypass entry may optionally end with a port number, following a colon (`:`).
  * NOTE: pac-test does not currently support this
* If a URL matches a Proxy Bypass list rule, the proxy should be bypassed and the connection made directly.

Example:

```text
*.example.com;www.microsoft.*;123.1*.66.*
```

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
