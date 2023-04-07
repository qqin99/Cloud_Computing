#!/usr/bin/env python3
import sys

for line in sys.stdin:
    page, count = line.strip().split('\t')
    if len(count.strip()) > 0:
        print('%s\t%s' % (page, count))

    # print('%s\t%s' % (  ,  )) pass this output to reducer
