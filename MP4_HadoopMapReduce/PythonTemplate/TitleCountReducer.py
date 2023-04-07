#!/usr/bin/env python3
from operator import itemgetter
import sys


dict = {}
# input comes from STDIN
for line in sys.stdin:
    # TODO
    key, val = line.split('\t')
    dict[key] = dict.get(key, 0) + 1

for k in dict:
    print('%s\t%s' % (k, dict[k]))

# TODO
# print('%s\t%s' % (  ,  )) print as final output