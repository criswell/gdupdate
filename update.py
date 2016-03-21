#!/usr/bin/env python

from __future__ import print_function
import json
import sys
import argparse
import requests
from godaddypy import Client, Account

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
args = parser.parse_args()

config = {}
with open(args.config, 'r') as f:
    config = json.load(f)

if 'ip_url' not in config or \
        'key' not in config or \
        'domain' not in config or \
        'sub-domain' not in config or \
        'secret_key' not in config:
    print("Error parsing config file!")
    print(config)
    sys.exit(1)

r = requests.get(config['ip_url'])
ip_info = r.json()

if 'ip' not in ip_info:
    print("Error getting IP from 'ip_url'!")
    print(ip_info)
    sys.exit(1)

my_ip = ip_info['ip']

my_acct = Account(api_key=config['key'], api_secret=config['secret_key'])
client = Client(my_acct)

domain = config['domain']
sub = config['sub-domain']

print(client.update_ip(my_ip, domains=[domain], subdomains=[sub]))

print(client.get_a_records(domain))
