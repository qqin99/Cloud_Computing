#!/usr/bin/env python3
import sys


leaguePath = sys.argv[1]

with open(leaguePath) as f:
    lines = f.readlines()
    leagues = [x.strip() for x in lines]

for line in sys.stdin:
    page_id, count = line.strip().split('\t')

    if page_id.strip() in leagues:
        print('%s\t%s' % (page_id, count))  # pass this output to reducer
