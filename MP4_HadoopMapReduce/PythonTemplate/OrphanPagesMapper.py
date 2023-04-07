#!/usr/bin/env python3
import sys


for line in sys.stdin:
    # parent_id, targets = line.strip().split(':')
    # child_links = targets.split()
    # if child_links:
    #     print(f'{parent_id}\t0')
    #     for link in child_links:
    #         print(f'{link}\t1')

    page_id, targets = line.strip().split(': ')
    targets = targets.strip().split(' ')
    targets = [t.strip() for t in targets]
    targets = filter(lambda x: len(x) > 0, targets)
    for target in targets:
        print('%s\t%s' % (target, page_id)) # pass this output to reducer
    # do I have to print a self as value for orphan page?
    print('%s\t%s' % (page_id, 'self'))
