#homework 2 Q3

import numpy as np
import matplotlib.pyplot as plt #cmd: pip install matplotlib

# parameters
k = 20
lamb = 0.1
iters = 40
ratevalue = 0.025

#open file
file_name="F:\cs246\homework2\hw2-recommendations\\ratings.train.txt"
trainingFile = open(file_name,'r')

#initiallize p q
q = {}
p = {}

for line in trainingFile:
    items = line.strip().split("\t")
    q_row = int(items[0])
    p_row = int(items[1])
    if q_row not in q.keys():
        q[q_row] = np.random.rand(k) * np.sqrt(5.0/k) # initiallize p  as the random value from 1 to sqrt(5.0/float(k))
    if p_row not in p.keys():
        p[p_row] = np.random.rand(k) * np.sqrt(5.0/k)

# Iterate
error_list=[]


for i in range(iters):
    #Read files everytime
    trainingFile = open(file_name, 'r')
    for eachline in trainingFile:
        ratings = eachline.strip().split("\t")
        q_ix = int(ratings[0])
        p_ix = int(ratings[1])
        rate = int(ratings[2])

        qi = q[q_ix]
        pu = p[p_ix]
        pu_t = pu.reshape(k,1)
        errors = 2 * (rate - np.dot(qi, pu_t))
        qi_new = qi + ratevalue * (errors * pu - 2 * lamb * qi)
        pu_new = pu + ratevalue * (errors * qi - 2 * lamb * pu)
        # update
        q[q_ix] = qi_new
        p[p_ix] = pu_new
        #Calculate errors every time
    errorsE = 0
    trainingFile = open(file_name, 'r')
    for line in trainingFile:
        ratings = line.strip(' ').split("\t")
        q_ix = int(ratings[0])
        p_ix = int(ratings[1])
        rate = int(ratings[2])
        qi = q[q_ix]
        pu = p[p_ix]
        pu_t = pu.reshape(k,1)

        errorsE += (rate - np.dot(qi,pu_t)) ** 2
    for pu_key in p.keys():
        errorsE += np.sum(p[pu_key] * p[pu_key])

    for qi_key in q.keys():
        errorsE += np.sum(q[qi_key] * q[qi_key])
    error_list.append(errorsE.reshape(()))

x = np.arange(1,iters+1,1)
y = error_list
plt.plot(x,y, "o")
plt.xlabel("# of iterations")
plt.ylabel("E")
plt.show()