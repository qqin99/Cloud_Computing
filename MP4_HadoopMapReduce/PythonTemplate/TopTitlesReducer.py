#!/usr/bin/env python3
import sys
from collections import defaultdict

freq = {}

# input comes from STDIN
for line in sys.stdin:
    word, count = line.strip().split('\t')
    # do i really need dict get and sum if all keys are unique
    freq[word] = freq.get(word, 0) + int(count)

index = 0
ret = []
for x in sorted(freq.items(), key=lambda x: (-x[1], x[0])):
    if index <= 9:
        ret.append(x[0])
        index += 1
    else:
        break

ret.reverse()

for word in ret:
    count = freq[word]
    print('%s\t%s' % (word, count))

#     invt_freq[int(count)].append(word)
#
# for k in invt_freq:
#     invt_freq[k] = sorted(invt_freq[k]) # ascending order word
#
# ret = sorted(invt_freq.items(), reverse=True)
# ret = list(zip(*ret))[1]
# ret = [x for s in ret for x in s]
#
# for word in sorted(ret[:10]):
#     count = freq[word]
#     print('%s\t%s' % (word, count))


# print('%s\t%s' % (  ,  )) print as final output
