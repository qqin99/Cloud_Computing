#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopTitleStatistics")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)

counts = lines.map(lambda line: int(line.strip().split('\t')[1].strip()))
Mean = int(counts.mean())
Sum = counts.sum()
Min = counts.min()
Max = counts.max()
Var = int(counts.variance())

#TODO

outputFile = open(sys.argv[2], "w")
'''
TODO write your output here
write results to output file. Format
'''
outputFile.write('Mean\t%s\n' % Mean)
outputFile.write('Sum\t%s\n' % Sum)
outputFile.write('Min\t%s\n' % Min)
outputFile.write('Max\t%s\n' % Max)
outputFile.write('Var\t%s\n' % Var)

outputFile.close()
sc.stop()

