#!/usr/bin/env python3
import sys

# TODO

for line in sys.stdin:
    word, value = line.strip().split('\t')
    try:
        count = int(value)
    except ValueError:
        continue
    print('%s\t%s' % (word, count))


#TODO
# print('%s\t%s' % (  ,  )) pass this output to reducer
