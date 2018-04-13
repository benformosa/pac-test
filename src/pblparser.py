#!/usr/bin/env python3
"""Test tool for Proxy Bypass lists, similar to pacparser"""

from urllib.parse import urlparse
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

def find_proxy(url):
    """Return the proxy configuration for a url"""
    for pattern in this.__pbl:
        # If the pattern has a URL scheme, match against `url`
        parsed_pattern = urlparse(pattern)
        if(parsed_pattern.scheme):
            target = url
        else:
            # Else, match agains the hostname extracted from `url`
            target = urlparse(url).hostname
            
        if(fnmatch.fnmatch(target, pattern)):
            # print("url '{}' matched pattern: '{}'".format(target, pattern))
            return 'DIRECT'
    
    # print("url '{}' did not match any bypass rules".format(url))
    return this.__proxy
