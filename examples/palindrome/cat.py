#!/usr/bin/env python

import sys

data = sys.stdin.readlines()

print(data)

all_number = []

for line in data:
    k, v = line.rstrip().split('=', 1)
    print(k, v)
    if k in ['pal_first', 'pal_second']:
        all_number += v.split(' ')

all_number.sort()
print(all_number)

print('JSUB_FINAL_all_number=%s' % ','.join(all_number))
