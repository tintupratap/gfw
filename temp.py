#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 13:47:30 2023

@author: tintu
"""

import requests
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

# Encode updated_gfwlist.txt content back to Base64 and save to gfwlist.txt
with open('updated_gfwlist.txt', 'r') as file:
    updated_gfwlist_content = file.read()

gfwlist_base64 = base64.b64encode(updated_gfwlist_content.encode('utf-8')).decode('utf-8')

# Split lines into 64-character wide chunks
gfwlist_base64_chunks = [gfwlist_base64[i:i+64] for i in range(0, len(gfwlist_base64), 64)]

with open('gfwlist.txt', 'w') as file:
    file.write('\n'.join(gfwlist_base64_chunks))