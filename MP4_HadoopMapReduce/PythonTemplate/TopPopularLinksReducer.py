#!/usr/bin/env python3
import sys


freq = {}
# input comes from STDIN
for line in sys.stdin:
    page, count = line.strip().split('\t')
    freq[page] = freq.get(page, 0) + int(count)


index = 0
ret = []
for x in sorted(freq.items(), key=lambda x: (-x[1], x[0])):
    if index <= 9:
        ret.append(x[0])
        index += 1
    else:
        break

ret.reverse()

for page in ret:
    count = freq[page]
    print('%s\t%s' % (page, count))

# print('%s\t%s' % (  ,  )) print as final output
