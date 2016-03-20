#!/usr/bin/env python

from __future__ import print_function
import json
import sys
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
args = parser.parse_args()

config = {}
with open(args.config, 'r') as f:
    config = json.load(f)

if not config.has_key('ip_id'):
    print("Error parsing config file!")
    print(config)
    sys.exit(1)
