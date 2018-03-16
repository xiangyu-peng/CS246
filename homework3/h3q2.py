#homework 3 Q2
#Pagerank on Spark~

import numpy as np
import re
import sys
import os
from collections import Counter
import itertools
import math
import cmath
import matplotlib.pyplot as plt #cmd: pip install matplotlib
# Path for spark source folder
os.environ['SPARK_HOME'] = "F:\spark\spark-2.2.1-bin-hadoop2.7"
# Append pyspark to Python Path
sys.path.append("F:\spark\spark-2.2.1-bin-hadoop2.7\python")
sys.path.append("F:\spark\spark-2.2.1-bin-hadoop2.7\python\lib\py4j-0.10.4-src.zip")
from pyspark import SparkConf, SparkContext
conf = SparkConf().set("spark.driver.memory", "8g")
sc = SparkContext(conf = conf)
#conf.set("spark.executor.memory", "16g")
#conf.set("spark.driver.memory", "8g")
from collections import Counter
import itertools

#  Question 2(a)
#  Solutions
#change the directed node number to list
def changeToList(line):
    return (int(line[0]), [int(line[1])])

#change the row to column
def changeToList2(line):
    return (int(line[1]), [int(line[0])])

#delete the overlapped ones and count the number
def count(line):
    i = 0
    line[1].sort()
    while i < len(line[1]) - 1:
        if line[1][i] == line[1][i + 1]:
            del line[1][i]
        else:
            i += 1
    num = len(line[1])
    return (line[0], 1/num)

#delete the overlapped ones
def count2(line):
    i = 0
    line[1].sort()
    while i < len(line[1]) - 1:
        if line[1][i] == line[1][i+1]:
            del line[1][i]
        else:
            i+=1
    return (line[0], line[1])

#multiply the matrix to the vector
def multiply(line, r, matrixcol):
    sum = 0
    for i in range(0, len(line[1])):
        sum += beta * r[line[1][i] - 1]* matrixcol[line[1][i] - 1][1]
    sum += (1-beta)/n
    return (line[0], line[1], sum)

#Read the data.txt
test_file_name = "F:\cs246\homework3\graph.txt"
lines = sc.textFile(test_file_name)
matrixcol = lines.map(lambda l:l.split('\t')).map(lambda line: changeToList(line)).reduceByKey(lambda v1 ,v2: v1 + v2).sortBy(lambda node:node[0], ascending=True).map(lambda line: count(line)).collect()
matrixrow = lines.map(lambda l:l.split('\t')).map(lambda line: changeToList2(line)).reduceByKey(lambda v1 ,v2: v1 + v2).sortBy(lambda node:node[0], ascending=True).map(lambda line: count2(line))

#parameters
iters = 40
n = 1000
r = []
beta = 0.8
for i in range(n):
    r.append(1/n)    #initialize r

#iteration
for i in range(iters):
    rnewmatrix = matrixrow.map(lambda line: multiply(line, r, matrixcol))
    r = rnewmatrix.map(lambda l: l[2]).collect()

#Statistics
rtop = r[:]
rbot = r[:]

for i in range(5):
    max1 = rtop.index(max(rtop))
    value1 = rtop[max1]
    print('Top %d is %d and its score is %f' % (i + 1, max1 + 1, value1))
    rtop[max1] = 0


for j in range(5):
    min1 = rbot.index(min(rbot))
    value2 = rbot[min1]
    print('Bottom %d is %d and its score is %f' % (j + 1, min1 + 1, value2))
    rbot[min1] = 1000000

#  Question 2(b)
#  Solutions

def multiply2(line, h):
    sum = 0
    for i in range(0, len(line[1])):
        sum += lamda * h[line[1][i] - 1]

    return (line[0], line[1], sum)

#Read the data.txt

matrix = lines.map(lambda l:l.split('\t')).map(lambda line: changeToList(line)).reduceByKey(lambda v1 ,v2: v1 + v2).sortBy(lambda node:node[0], ascending=True).map(lambda line: count2(line))
matrixT = lines.map(lambda l:l.split('\t')).map(lambda line: changeToList2(line)).reduceByKey(lambda v1 ,v2: v1 + v2).sortBy(lambda node:node[0], ascending=True).map(lambda line: count2(line))

#parameters
lamda = 1
mu = 1

#initialize h
h = []
for i in range(n):
    h.append(1)

#iteration
for i in range(iters):
    amatrix = matrixT.map(lambda line: multiply2(line, h))
    a = amatrix.map(lambda l: l[2]).collect()
    maxa = max(a)
    for i in range(len(a)):                                     #Scale a
        a[i] = a[i]/maxa
    hmatrix = matrix.map(lambda line: multiply2(line, a))
    h = hmatrix.map(lambda l: l[2]).collect()
    maxh = max(h)
    for i in range(len(h)):                                    #Scale h
        h[i] = h[i]/maxh

#Statistics
htop = h[:]
for i in range(5):
    max1 = htop.index(max(htop))
    value=htop[max1]
    print('Top %d is %d and its score is %f' % (i+1, max1 + 1,value))
    htop[max1] = 0

hbot = h[:]
for i in range(5):
    min1 = hbot.index(min(hbot))
    value=hbot[min1]
    print('Bottom %d is %d and its score is %f' % (i+1, min1 + 1,value))
    hbot[min1] = 1000000

atop = a[:]
for i in range(5):
    max1 = atop.index(max(atop))
    value=atop[max1]
    print('Top %d is %d and its score is %f' % (i+1, max1 + 1,value))
    atop[max1] = 0

abot = a[:]
for i in range(5):
    min1 = abot.index(min(abot))
    value=abot[min1]
    print('Bottom %d is %d and its score is %f' % (i+1, min1 + 1,value))
    abot[min1] = 1000000