#!/usr/bin/env python
import os
import sys
from pyspark import SparkConf, SparkContext
from operator import add


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


conf = SparkConf().setMaster("local").setAppName("OrphanPages")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)

pairs = lines.flatMap(mapper)
counts = pairs.reduceByKey(lambda a, b: a + b)
orphans = counts.filter(lambda x: x[1] == 0).sortByKey()

output = open(sys.argv[2], "w")
# write results to output file. Foramt for each line: (line+"\n")
for (page, count) in orphans.collect():
    output.write(page + "\n")
# with open(sys.argv[2], "w") as output:
#     for tup in counts.collect():
#         output.writelines(tup[0]+'\t'+str(tup[1])+os.linesep)

output.close()
sc.stop()
