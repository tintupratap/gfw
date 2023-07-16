#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 13:47:30 2023

@author: tintu
"""

import requests
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_website_accessibility(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        print("Blocked site detected, adding to gfwlist: " + url)
        return False

# Retrieve the gfwlist.txt file
# You can uncomment the urls for retriving full gfwlist or tinylist.. 
# Tiny gwflist (recommended)

url = 'https://cdn.jsdelivr.net/gh/gfwlist/tinylist/tinylist.txt'


# Full gfwlist (not recommended but if you want full freedom, you can..)
#[Warning] It may take a long time, maybe an hour or maybe a day depending on your connection..]

#url = 'https://cdn.jsdelivr.net/gh/gfwlist/gfwlist/gfwlist.txt'



response = requests.get(url)
gfwlist_base64 = response.text.strip()

# Save the original gfwlist.txt
with open('original_gfwlist.txt', 'w') as file:
    file.write(gfwlist_base64)

# Decode the gfwlist content with Base64
gfwlist = base64.b64decode(gfwlist_base64).decode('utf-8')

# Remove comments and empty lines from the gfwlist
gfwlist_lines = gfwlist.split('\n')
gfwlist_lines = [line.strip() for line in gfwlist_lines if line.strip() and not line.startswith('!')]

# Check accessibility of each website in the gfwlist using multithreading
blocked_sites = []
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_line = {}
    for line in gfwlist_lines:
        if line.startswith('|'):
            url = line[1:]
        if line.startswith('||'):
            url = line[2:]
        elif line.startswith('@@||*'):
            url = line[5:]
        elif line.startswith('@@||'):
            url = line[4:]
        elif line.startswith('@@|'):
            url = line[3:]
        elif line.startswith('@||'):
            url = line[3:]
        elif line.startswith('@|'):
            url = line[2:]
        elif line.startswith('@'):
            url = line[1:]
        else:
            url = None

        if url is not None:
            future = executor.submit(check_website_accessibility, 'https://' + url)
            future_to_line[future] = line

    for future in as_completed(future_to_line):
        line = future_to_line[future]
        if not future.result():
            blocked_sites.append(line)

# Write blocked_sites to updated_gfwlist.txt
with open('updated_gfwlist.txt', 'w') as file:
    #file.write('!----Blocked Sites in in my area----!\n')
    file.write('\n'.join(blocked_sites))

# Encode updated_gfwlist.txt content back to Base64 and save to gfwlist.txt
with open('updated_gfwlist.txt', 'r') as file:
    updated_gfwlist_content = file.read()

gfwlist_base64 = base64.b64encode(updated_gfwlist_content.encode('utf-8')).decode('utf-8')

# Split lines into 64-character wide chunks
gfwlist_base64_chunks = [gfwlist_base64[i:i+64] for i in range(0, len(gfwlist_base64), 64)]

with open('gfwlist.txt', 'w') as file:
    file.write('\n'.join(gfwlist_base64_chunks))


print(" Your gfwlist.txt created..\n Host this somewhere and import in shadowsocks(you can even add the raw file path from github in shadowsocks, no hosting needed).. \n Optionally check original_gwflist.txt and gwflist.txt\n The sites you can't access are listed in updated_gwflist.txt\n\n enjoy.. :)")
