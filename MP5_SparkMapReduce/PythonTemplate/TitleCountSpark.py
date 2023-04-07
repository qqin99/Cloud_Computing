#!/usr/bin/env python

'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''
import re
import sys
from pyspark import SparkConf, SparkContext
from operator import add

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]

with open(stopWordsPath) as f:
    stop_list = []
    for line in f:
        stop_list.append(line.lower().strip('\n').strip())
    # print(stop_list)

with open(delimitersPath) as f:
    # TODO
    delimiters = f.readline()
    print(delimiters)

delimiters = '[\\t,;.:?!\\-@\\[\\](){}_*/\\n]'


def tokenize(line):
    line = line.lower().strip().strip('\n')
    line = re.split(delimiters, line)
    line = filter(None, line)
    line = filter(lambda x: x not in stop_list, line)
    return line


# creating a Spark Context. conf is the configuration for a spark application
conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)  # an object of SparkContext

# initializing an RDD using a text file: rdd = sc.textFile()
# this method takes the path as an argument and optionally takes a number of partitions as the second argument
lines = sc.textFile(sys.argv[3], 1)  # base RDD
# Spark flatMap() transformation flattens the RDD/DataFrame column after applying the function on every element
# and returns a new RDD/DataFrame respectively.
words = lines.flatMap(tokenize)

# reduce is the action in spark
# .reduceByKey(add) lambda a, b: a + b
counts = words.map(lambda word: (word, 1)) \
    .reduceByKey(add) \
    .sortByKey(ascending=False)

# can i use takeOrdered() here
# tops = counts.sortBy(ascending=False, keyfunc=lambda a: a[1]).take(10)
tops = counts.takeOrdered(10, key=lambda a: -a[1])
tops = sorted(tops)

# write results to output file. Foramt for each line: (line +"\n")
outputFile = open(sys.argv[4], "w")
for (word, count) in tops:
    outputFile.write(word + "\t" + str(count) + "\n")

outputFile.close()
sc.stop()
