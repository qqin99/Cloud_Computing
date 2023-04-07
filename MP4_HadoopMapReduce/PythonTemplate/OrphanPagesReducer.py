#!/usr/bin/env python3
import sys
from collections import defaultdict

dict = defaultdict(list)

for line in sys.stdin:
    # TODO
    page_id, target = line.strip().split('\t')
    if len(target.strip()) == 0:
        continue
    else:
        dict[page_id.strip()].append(target.strip())

dict_items = dict.items()
# sort by int value not string so here turn string to int
sorted_dict = sorted(dict_items, key = lambda x: int(x[0]))

for page, value in sorted_dict:
    if (len(value) == 1 and value[0] == 'self') or \
            (len(value) == 2 and ((value[0] == page and value[1] == 'self') or
                                  (value[1] == page and value[0] == 'self'))):
        print(page)  # print as final output