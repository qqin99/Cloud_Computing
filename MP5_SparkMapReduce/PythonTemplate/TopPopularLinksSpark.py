#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)


# TODO
# for each line, u generate a list of tuple with page_id,0 and target, 1
def mapper(line):
    page_id, targets = line.strip().split(': ')
    targets = targets.strip().split(' ')
    targets = [t.strip() for t in targets]
    targets = filter(lambda x: len(x) > 0, targets)

    ls = [(page_id, 0)]
    for t in targets:
        ls.append((t, 1))
    return ls


counts = lines.flatMap(mapper).reduceByKey(add)
tops = counts.takeOrdered(10, key=lambda a: -a[1])
tops = sorted(tops)

output = open(sys.argv[2], "w")

for (page, count) in tops:
    output.write(page + "\t" + str(count)+"\n")

# write results to output file. Foramt for each line: (key + \t + value +"\n")
output.close()
sc.stop()
