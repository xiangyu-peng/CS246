#homework 2 Q2
#Clustering on Spark~

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

#Read the data.txt
test_file_name = "F:\cs246\homework2\hw2-q2-kmeans\data.txt"
lines = sc.textFile(test_file_name)
lines = lines.map(lambda line: np.array([float(x) for x in line.split(' ')])).cache()

#parameters
k=10 # #of clusterings
iters=20 # # of iterations

# Fuction to calculate the distance of each point to the clustering centroid and fnd the minimum distance and ner clustering group
def calDis(point,lines_centroid):
    index = 0
    min_distance = float("+inf")
    for i in range(int(k)):
        singleDistance = float(np.sum(np.square(np.subtract(point, lines_centroid[i]))))
        if singleDistance < min_distance:
            min_distance = singleDistance
            index = i + 1
    return (index, min_distance)

# finf the new centroid after one iteration
def recentroid(line):
    total_number = line[1][1]
    point = line[1][0]
    point = np.divide(point, total_number)
    return (line[0], point)

# Read the c1.txt first centroid
test_file_centroid = "F:\cs246\homework2\hw2-q2-kmeans\c1.txt"
lines_centroid_1 = sc.textFile(test_file_centroid)
lines_centroid_1 = lines_centroid_1.map(lambda line: np.array([float(x) for x in line.split(' ')])).cache().collect()

cost_list_1=[]
for i in range(iters):
    lines_Dis_1 = lines.map(lambda point: (calDis(point, lines_centroid_1), (point, 1))).map(lambda x: (x[0][0], (x[1][0], x[1][1], x[0][1])))
    total_Dis_1 = lines_Dis_1.reduceByKey(lambda point1, point2: (point1[0] + point2[0], point1[1] + point2[1], point1[2] + point2[2])).sortByKey(True)
    recentroid_1 = total_Dis_1.map(lambda l: recentroid(l)).map(lambda l: l[1]).collect()
    lines_centroid_1 = recentroid_1
    phi_1 = total_Dis_1.map(lambda l: l[1][2]).collect()
    phi_1 = sum(phi_1)
    cost_list_1.append(phi_1)

#parameters for the graph
x = np.arange(1,iters+1,1)
y1 = cost_list_1


test_file_centroid = "F:\cs246\homework2\hw2-q2-kmeans\c2.txt"
lines_centroid_2 = sc.textFile(test_file_centroid)
lines_centroid_2 = lines_centroid_2.map(lambda line: np.array([float(x) for x in line.split(' ')])).cache().collect()

# Read the c2.txt first centroid
cost_list_2=[]
for j in range(iters):
    lines_Dis_2 = lines.map(lambda point: (calDis(point, lines_centroid_2), (point, 1))).map(lambda x: (x[0][0], (x[1][0], x[1][1], x[0][1])))
    total_Dis_2 = lines_Dis_2.reduceByKey(lambda point1, point2: (point1[0] + point2[0], point1[1] + point2[1], point1[2] + point2[2])).sortByKey(True)
    recentroid_2 = total_Dis_2.map(lambda l: recentroid(l)).map(lambda l: l[1]).collect()
    lines_centroid_2 = recentroid_2
    phi_2 = total_Dis_2.map(lambda l:l[1][2]).collect()
    phi_2=sum(phi_2)
    cost_list_2.append(phi_2)

#plot the cost in one figure
y2 = cost_list_2
plt.plot(x, y1, "o",x, y2, "o")
plt.xlabel("# of iterations")
plt.ylabel("cost_list")
plt.show()


# Calculate the percentage change
print("cost_list_1=")
print(cost_list_1)
print("cost_list_2=")
print(cost_list_2)

#  Question 2(b)
#  Solutions

#Read the data.txt
test_file_name = "F:\cs246\homework2\hw2-q2-kmeans\data.txt"
lines = sc.textFile(test_file_name)
lines = lines.map(lambda line: np.array([float(x) for x in line.split(' ')])).cache()

#parameters
k=10 # #of clusterings
iters=20 # # of iterations

# Fuction to calculate the distance of each point to the clustering centroid and fnd the minimum distance and ner clustering group
def calDis(point,lines_centroid):
    index = 0
    min_distance = float("+inf")
    for i in range(int(k)):
        singleDistance = float(np.sum(np.abs(np.subtract(point, lines_centroid[i]))))
        if singleDistance < min_distance:
            min_distance = singleDistance
            index = i + 1
    return (index, min_distance)

# finf the new centroid after one iteration
def recentroid(line):
    total_number = line[1][1]
    point = line[1][0]
    point = np.divide(point, total_number)
    return (line[0], point)

# Read the c1.txt first centroid
test_file_centroid = "F:\cs246\homework2\hw2-q2-kmeans\c1.txt"
lines_centroid_1 = sc.textFile(test_file_centroid)
lines_centroid_1 = lines_centroid_1.map(lambda line: np.array([float(x) for x in line.split(' ')])).cache().collect()

cost_list_1=[]
for i in range(iters):
    lines_Dis_1 = lines.map(lambda point: (calDis(point, lines_centroid_1), (point, 1))).map(lambda x: (x[0][0], (x[1][0], x[1][1], x[0][1])))
    total_Dis_1 = lines_Dis_1.reduceByKey(lambda point1, point2: (point1[0] + point2[0], point1[1] + point2[1], point1[2] + point2[2])).sortByKey(True)
    recentroid_1 = total_Dis_1.map(lambda l: recentroid(l)).map(lambda l: l[1]).collect()
    lines_centroid_1 = recentroid_1
    phi_1 = total_Dis_1.map(lambda l: l[1][2]).collect()
    phi_1 = sum(phi_1)
    cost_list_1.append(phi_1)

#parameters for the graph
x = np.arange(1,iters+1,1)
y1 = cost_list_1


test_file_centroid = "F:\cs246\homework2\hw2-q2-kmeans\c2.txt"
lines_centroid_2 = sc.textFile(test_file_centroid)
lines_centroid_2 = lines_centroid_2.map(lambda line: np.array([float(x) for x in line.split(' ')])).cache().collect()

# Read the c2.txt first centroid
cost_list_2=[]
for j in range(iters):
    lines_Dis_2 = lines.map(lambda point: (calDis(point, lines_centroid_2), (point, 1))).map(lambda x: (x[0][0], (x[1][0], x[1][1], x[0][1])))
    total_Dis_2 = lines_Dis_2.reduceByKey(lambda point1, point2: (point1[0] + point2[0], point1[1] + point2[1], point1[2] + point2[2])).sortByKey(True)
    recentroid_2 = total_Dis_2.map(lambda l: recentroid(l)).map(lambda l: l[1]).collect()
    lines_centroid_2 = recentroid_2
    phi_2 = total_Dis_2.map(lambda l:l[1][2]).collect()
    phi_2=sum(phi_2)
    cost_list_2.append(phi_2)

#plot the cost in one figure
y2 = cost_list_2
plt.plot(x, y1, "o",x, y2, "o")
plt.xlabel("# of iterations")
plt.ylabel("cost_list")
plt.show()

# Calculate the percentage change
print("cost_list_1=")
print(cost_list_1)
print("cost_list_2=")
print(cost_list_2)