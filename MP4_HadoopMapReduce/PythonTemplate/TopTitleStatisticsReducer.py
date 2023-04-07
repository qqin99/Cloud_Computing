#!/usr/bin/env python3
import sys
import math


#TODO
nums = []

for line in sys.stdin:
    # TODO
    word, count = line.strip().split('\t')
    nums.append(int(count))

stats = {'Min': min(nums), 'Max': max(nums), 'Sum': sum(nums), 'Mean': sum(nums) // len(nums)}

s = 0
for n in nums:
    s += (n - stats['Mean'])**2
stats['Var'] = s // len(nums)

for stat in ['Mean', 'Sum', 'Min', 'Max', 'Var']:
    print('%s\t%s' % (stat, stats[stat])) # print as final output
