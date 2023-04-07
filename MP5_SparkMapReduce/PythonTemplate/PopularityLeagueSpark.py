#!/usr/bin/env python

# Execution Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt
import sys
from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setMaster("local").setAppName("PopularityLeague")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)


def mapper(line):
    page_id, targets = line.strip().split(': ')
    targets = targets.strip().split(' ')
    targets = [t.strip() for t in targets]
    targets = filter(lambda x: len(x) > 0, targets)

    ls = [(t, 1) for t in targets if t in league_ls]
    return ls


# read in links file and leagues file
lines = sc.textFile(sys.argv[1], 1)
leagueIds = sc.textFile(sys.argv[2], 1)

league_ls = leagueIds.map(lambda x: x.strip()).collect()

counts = lines.flatMap(mapper).reduceByKey(add)
counts = counts.sortByKey()
tops = counts.sortBy(keyfunc=lambda a: a[0]).collect()

dict = {}
for k, v in tops:
    dict[k] = v

ranks = []
for k, v in dict.items():
    rank = 0
    for page in league_ls:
        if dict.get(page, 0) < v:
            rank += 1
    ranks.append((k, rank))

# ranks.sort()

# TODO
output = open(sys.argv[3], "w")
# write results to output file. Foramt for each line: (key + \t + value +"\n")
for (page, cnt) in ranks:
    output.write(page + "\t"+str(cnt)+"\n")
output.close()
sc.stop()
