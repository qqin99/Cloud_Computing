#!/usr/bin/env python3
import sys


for line in sys.stdin:
    # TODO
    word, count = line.strip().split('\t')
    print('%s\t%s' % (word, count))
    # print('%s\t%s' % (  ,  )) pass this output to reducer
