import fnmatch
import sys

# Allows the module's variables to persist
# See https://stackoverflow.com/a/35904211/813821
this = sys.modules[__name__]

def init():
    # Proxy Bypass List
    this.__pbl = []
    # Default proxy string
    this.__proxy = 'PROXY proxy:8080'

def set_proxy(proxy):
    """Update the proxy string to return"""
    this.__proxy = proxy

def get_pbl():
    return this.__pbl

def parse_pbl(file):
    """Import a proxy bypass list from file"""
    with open(file, 'rt') as f:
        this.__pbl = f.read().strip().split(';')

def find_proxy(host):
    """Return the proxy configuration for a host"""
    for pattern in this.__pbl:
        if(fnmatch.fnmatch(host, pattern)):
            # VERBOSE
            # print("host '{}' matched pattern: '{}'".format(host, pattern))
            return 'DIRECT'
    return this.__proxy
