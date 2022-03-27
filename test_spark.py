from __future__ import print_function

import sys
from operator import add
import time
import pyspark
from pyspark.sql import SparkSession

if __name__ == "__main__":

	spark = SparkSession \
		.builder \
		.appName("WordCount") \
		.getOrCreate()
	
	start_time = time.time()

	lines = spark.sparkContext.textFile("hdfs:///sampledata.txt")
	counts = lines.flatMap(lambda x: x.split(' ')) \
		.map(lambda x: (x, 1)) \
		.reduceByKey(add) \
		.map(lambda x: (x[1], x[0])) \
		.sortByKey(False)

	counts.coalesce(1).saveAsTextFile("hdfs:///output")
	
	output = counts.take(10)
	print("The 10 most frequent words are :\n")
	i = 1
	for count, word in output:
		print("{}. {} ---> {}".format(i, word, count))
		i+=1

	
	end_time = time.time()

	print("Query took {:0.2f} seconds".format(end_time - start_time))
	print("Number of unique words in file {}".format(counts.count()))
