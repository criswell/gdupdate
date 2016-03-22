#!/usr/bin/env python

from __future__ import print_function
import json
import sys
import argparse
from datetime import datetime, timedelta
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
        'refresh_time' not in config or \
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

# Note: Here we only concern ourselves with days, hours, seconds, and weeks
dt = timedelta(
        days=config['refresh_time'].get('days', 0),
        hours=config['refresh_time'].get('hours', 0),
        seconds=config['refresh_time'].get('seconds', 0),
        weeks=config['refresh_time'].get('weeks', 0)
        )

now = datetime.today()

update_now = False

if 'last_update' in config:
    last_update = datetime.strptime(config['last_update'], '%Y-%m-%d %H:%M:%S.%f')
    if now - last_update > dt:
        update_now = True
else:
    update_now = True

if 'last_ip' in config:
    if my_ip != config['last_ip']:
        update_now = True

if update_now:
    my_acct = Account(api_key=config['key'], api_secret=config['secret_key'])
    client = Client(my_acct)

    domain = config['domain']
    sub = config['sub-domain']

    print(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
    if not client.update_ip(my_ip, domains=[domain], subdomains=[sub]):
        print("ERROR UPDATING DOMAIN!")
    else:
        print("Domain updated successfully!")

    print("Current domain info:")
    print("\t{0}".format(client.get_a_records(domain)))

    config['last_update'] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    config['last_ip'] = my_ip

    with open(args.config, 'w') as f:
        json.dump(config, f)

