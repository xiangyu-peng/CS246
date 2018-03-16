import re
import sys
import os
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

test_file_name = "F:\cs246\soc-LiveJournal1Adj.txt"
out_file_name = "F:\cs246\Homework1Q1"

#Define a function that
def friendMap(line):
  user=line[0]
  friends=list(set(line[1]))
  connecteds = [((user, friend), -10000000000) for friend in friends]
  commons = [(pair, 1) for pair in itertools.permutations(friends, 2)]
  return connecteds + commons


#lines=sc.textFile(sys.argv[1])
lines=sc.textFile(test_file_name)

#We get [(User,[friends]),(User,[friends]),(User,[friends])]
lines=lines.map(lambda l:l.split('\t')).map(lambda pair: (pair[0],pair[1].split(',')))
#We can get [(friend1 ,friend2,1),(friend1,friend3,-10000)…]
user=lines.flatMap(lambda l: friendMap(l))
#Calculate the number of two people's common friends
mutual=user.reduceByKey(lambda v1,v2:v1+v2).filter(lambda pair_number:pair_number[1]>0)
#Recommend the friend to the user who have the most common friends with hin/her.
recommendation=mutual.map(lambda x:(x[0][0],(int(x[0][1]),x[1]))).sortBy(lambda recommend:recommend[1][0], ascending=True).sortBy(lambda recommend:recommend[1][1], ascending=False).reduceByKey(lambda v1,v2:v1+v2).map(lambda x:(int(x[0]),x[1])).sortByKey(True).collect()
recidtotal=[]
j=0
#Recommend up to 10 friends to one user
while j<len(recommendation):
  recid = recommendation[j][1]
  i=0
  recidlist=[]
  while i<min(19,len(recid)):
      recidlist.append(str(recid[i]))
      recidlist.append(',')
      i+=2


  recidlist=[str(recommendation[j][0])]+['\t']+recidlist
  recidlist.pop()
  recidlist=''.join(recidlist)
  recidtotal.append(recidlist)
  j+=1

#Output the data
distData = sc.parallelize(recidtotal)
distData.repartition(1).saveAsTextFile(out_file_name)
sc.stop()



