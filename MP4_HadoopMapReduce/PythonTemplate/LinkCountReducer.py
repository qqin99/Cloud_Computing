#!/usr/bin/env python3
import sys
from collections import defaultdict

dict = {}
# input comes from STDIN
for line in sys.stdin:
    # TODO
    page_id, target = line.strip().split('\t')
    # do i need to exclude itself?
    dict[page_id.strip()] = dict.get(page_id, 0) + 1

for page in dict:
    count = dict[page]
    print('%s\t%s' % (page, count)) #print as final output