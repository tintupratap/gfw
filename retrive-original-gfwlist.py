#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import re
import base64
import codecs

# the URL of gfwlist
baseurl = 'https://cdn.jsdelivr.net/gh/gfwlist/gfwlist/gfwlist.txt'
domain_pattern = r'([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
fs = open('domain-gfwlist.txt', 'w')
content = urllib.request.urlopen(baseurl, timeout=15).read()
decoded_content = codecs.decode(content, 'base64').decode('utf-8')

# remember all blocked domains, in case of duplicate records
domainlist = []

for line in decoded_content.splitlines():
    if re.findall(domain_pattern, line):
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
            except ValueError:
                domainlist.append(domain[0])
                fs.write(domain[0] + '\n')
print('done!')
