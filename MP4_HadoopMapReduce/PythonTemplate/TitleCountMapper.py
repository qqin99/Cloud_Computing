#!/usr/bin/env python3
import re
import sys
import string

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]

with open(stopWordsPath) as f:
    stop_list = []
    for line in f:
        stop_list.append(line.lower().strip('\n').strip())
    print(stop_list)
# TODO
with open(delimitersPath) as f:
    # for line in f:
    delimiters = f.readline()
    # print(delimiters)

delimiters = '[\\t,;.:?!\\-@\\[\\](){}_*/\\n]'

for line in sys.stdin:

    parts = re.split(delimiters, line.lower())
    results = list(filter(None, parts))

    for word in results:
        if word not in stop_list:
            print('%s\t%s' % (word, 1))


# print('%s\t%s' % (  ,  )) pass this output to reducer
