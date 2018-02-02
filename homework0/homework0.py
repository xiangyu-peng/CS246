import re
import sys


# When run it in the pycharm, we need these.
import os
# Path for spark source folder
os.environ['SPARK_HOME'] = "F:\spark\spark-2.2.1-bin-hadoop2.7"

# Append pyspark to Python Path
sys.path.append("F:\spark\spark-2.2.1-bin-hadoop2.7\python")
sys.path.append("F:\spark\spark-2.2.1-bin-hadoop2.7\python\lib\py4j-0.10.4-src.zip")


from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf = conf)

test_file_name = "C:/Users/Rebekah/Desktop/pg100.txt"
out_file_name = "C:/Users/Rebekah/Desktop/output"

#Read the file
data = sc.textFile(test_file_name)
#data = sc.textFile(sys.argv[1])
#Separate every word and ignore all non-alphabetic characters.
line=data.flatMap(lambda line: re.split(r'\W+',line))
linefilter=line.filter(lambda word: re.match('^[A-Za-z]',word))
# Consider all words as lower case
wordlower=linefilter.map(lambda word:word.lower())
# Only consider the forst letter of every word.
letter=wordlower.map(lambda word: word[0])
# Output the number of words that start with each
counts=letter.map(lambda c: (c,1)).reduceByKey(lambda v1,v2:v1+v2).sortBy(lambda letter:letter[0], ascending=True)
#counts.repartition(1).saveAsTextFile(sys.argv[2])
counts.repartition(1).saveAsTextFile(out_file_name)
sc.stop()

