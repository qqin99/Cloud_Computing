#!/usr/bin/env python3
import sys
#TODO

dict={}
# input comes from STDIN
for line in sys.stdin:
    page_id, count = line.strip().split('\t')
    dict[page_id] = dict.get(page_id, 0) + int(count)


# for x in sorted(dict.items(), key=lambda x: (-x[0], x[1])):
# negate could not be in front of string. so we negate number and then reverse
sorted_dict = sorted(dict.items(), key=lambda x: int(x[0]), reverse=True)
# sorted dict is already a list of dict items
for k, v in sorted_dict:
    rank = 0
    for page in dict:
        if dict.get(page, 0) < v:
            rank += 1
    print('%s\t%s' % (k, rank))

#TODO
# print('%s\t%s' % (  ,  )) print as final output