#homework 4 Q1
#SVM

import time
import numpy as np
import os
import copy
import matplotlib.pyplot as plt #cmd: pip install matplotlib
import copy


# parameters
feature_name = "F:\cs246\homework4\\features.txt"
target_name = "F:\cs246\homework4\\target.txt"
dataNumbers = 6414
featureNumbers = 122
C = 100

# open file
feature_file = open(feature_name, "r")
target_file = open(target_name, "r")

# contruct a list, in every index, there are 122 features and 1 target
dataPoints = []
for line in feature_file:
    featuresstring = line.strip().split(",")
    features = [int(i) for i in featuresstring]
    dataPoints.append(features)  #map each feature as int instead of char

for (i, line) in enumerate(target_file):
    target = line.strip()
    dataPoints[i].append(int(target))

#iterate initialization
k = 0
w = np.zeros(featureNumbers) * 1.0
b = 0.0
fks = [C * dataNumbers]
eta = 0.0000003
epsilon = 0.25

start = time.clock()  # timer

while True:
    # calculate w_new
    second_sum = np.zeros(featureNumbers)
    for each in dataPoints:
        x = np.array(each[:-1])
        y = np.array(each[-1])
        xw = np.dot(x,w)          #a vector
        cond = y * (xw + b)       #condition
        if cond >= 1:            #check 0 or yixi
            pass
        else:
            second_sum -= y * x
    w_new = w - eta * (w + C * second_sum)   #new w

    b_sum = 0.0
    for each in dataPoints:
        x = each[:-1]       #xi
        y = each[-1]        #yi
        xw =  np.dot(x,w)   #a number (xi *  w)
        cond = y * (xw + b)
        if cond >= 1:
            pass
        else:
            b_sum -= y
    b_new = b - eta * C * b_sum   #new b

    # At the end of iteration, we update w and b
    w = copy.deepcopy(w_new)
    b = copy.deepcopy(b_new)

    # calculate the fk
    fk_firstPart = 0.5 * np.dot(w, w)  #First part of fk
    fk_secondPart = 0.0
    for each in dataPoints:
        x = each[:-1]
        y = each[-1]
        xw = np.dot(x, w)
        cond = y * (xw + b)
        fk_secondPart += C * max(0, (1 - cond))
    fk = fk_firstPart + fk_secondPart
    fks.append(fk)

    # calculate delta
    if 0 == k:
        pass
    else:
        delta = abs(fks[k - 1] - fks[k]) / fks[k - 1] * 100
        # show progress
        # if k % 10 == 0:
        print('%d iteration: %f delta: %f' % (k, fk, delta))
        if delta <= epsilon:
            break

    # increment # of iteration
    k += 1

end = time.clock()
timeUsed = end - start
print(timeUsed)

#write the file
if os.path.isfile('batch.txt'):
    os.remove("batch.txt")
if os.path.isfile('batch.time.txt'):
    os.remove("batch.time.txt")

with open('batch.txt', 'a') as write_file:
    for i, each in enumerate(fks):
        write_file.write(str(i) + "," + str(each) + '\n')
with open('batch.time.txt', 'a') as write_file:
    write_file.write(str(timeUsed))

# SGD
feature_file = open(feature_name, "r")
target_file = open(target_name, "r")

# contruct a list, in every index, there are 122 features and 1 target
dataPoints = []
for line in feature_file:
    featuresstring = line.strip().split(",")
    features = [int(i) for i in featuresstring]
    dataPoints.append(features)  #map each feature as int instead of char

for (i, line) in enumerate(target_file):
    target = line.strip()
    dataPoints[i].append(int(target))
#shuffle the dataPoints
np.random.shuffle(dataPoints)

#parameters
i = 0
k = 0
w = np.zeros(featureNumbers) * 1.0
b = 0.0
fks2 = [C * dataNumbers] #initialize fk0 = C * 1 * n
eta = 0.0001
epsilon = 0.001
deltas=[0]

start = time.clock()

while True:
# calculate w_new
    second_sum = np.zeros(featureNumbers)
    x = np.array(dataPoints[i][:-1])
    y = dataPoints[i][-1]
    xw = np.dot(x, w)
    cond = y * (xw + b)
    if cond >= 1:
        pass
    else:
        second_sum -= np.multiply(y, x)
    w_new = w -eta * (w + C * second_sum)

# calculate b and i
    b_sum = 0.0
    if cond >=1:
        pass
    else:
        b_sum -= y
    b_new = b - eta * b_sum * C

#Update b, w
    w = w_new[:]
    b = b_new

# calculate fk
    fk_firstPart = 0.5 * np.dot(w, w)  #First part of fk
    fk_secondPart = 0.0
    for each in dataPoints:
        x = np.array(each[:-1])
        y = each[-1]
        xw = np.dot(x, w)
        cond = y * (xw + b)
        fk_secondPart += C* max(0, (1 - cond))
    fk = fk_firstPart + fk_secondPart
    fks2.append(fk)

# Calculate delta to break the loop
    delta = abs(fks2[k-1] - fks2[k]) * 100 / fks2[k]
    if k == 0:
        pass
    elif k == 1:
        delta = abs(fks2[k - 1] - fks2[k]) / fks2[k - 1] * 100
        deltas.append(delta)
    else:
        delta = abs(fks2[k - 1] - fks2[k]) / fks2[k - 1] * 100
        delta_curr = 0.5 * deltas[k - 1] + 0.5 * delta
        deltas.append(delta_curr)
        # show progress
        # if k % 10 == 0:
        #     print('%d iteration: %f delta: %f' % (k, fk, delta_curr))
        if delta_curr <= epsilon:
            break

#Update k and i
    k += 1
    i = (i + 1) % dataNumbers

end = time.clock()
timeUsed = end - start
print(timeUsed)

if os.path.isfile('stochastic.txt'):
    os.remove("stochastic.txt")
if os.path.isfile('stochastic.time.txt'):
    os.remove("stochastic.time.txt")

with open('stochastic.txt', 'a') as write_file:
    for i, each in enumerate(fks2):
        write_file.write(str(i) + "," + str(each) + '\n')
with open('stochastic.time.txt', 'a') as write_file:
    write_file.write(str(timeUsed))



# MBGD
feature_file = open(feature_name, "r")
target_file = open(target_name, "r")

# contruct a list, in every index, there are 122 features and 1 target
dataPoints = []
for line in feature_file:
    featuresstring = line.strip().split(",")
    features = [int(i) for i in featuresstring]
    dataPoints.append(features)  #map each feature as int instead of char

for (i, line) in enumerate(target_file):
    target = line.strip()
    dataPoints[i].append(int(target))
#shuffle the dataPoints
np.random.shuffle(dataPoints)

k = 0
l = 0
w = np.zeros(featureNumbers) * 1.0
b = 0.0
fks3 = [C * dataNumbers]
deltas = [0]
eta = 0.00001
epsilon = 0.01
batch_size = 20

start = time.clock()

while True:
    mini_batch = dataPoints[int(l * batch_size) : int(min(dataNumbers, (l + 1) * batch_size))]
    second_sum = np.zeros(featureNumbers)
    for each in mini_batch:
        x = np.array(each[:-1])
        y = each[-1]
        xw = np.dot(x, w)
        cond = y * (xw + b)
        if cond >= 1:
            pass
        else:
            second_sum -= y * x
    w_new = w - eta * (w + C * second_sum)

    # calculate new b using old b, w
    b_sum = 0.0
    for each in mini_batch:
        x = np.array(each[:-1])
        y = each[-1]
        xw = np.dot(x, w)
        cond = y * (xw + b)
        if cond >= 1:
            pass
        else:
            b_sum -= y
    b_new = b - eta * C * b_sum

    # update w and b
    w = w_new[:]
    b = b_new

    # calculate error
    fk = 0.5 * sum(w * w)
    fk_secondPart = 0.0
    for each in dataPoints:
        x = each[:-1]
        y = each[-1]
        xw = sum(x * w)
        cond = y * (xw + b)
        fk_secondPart += C * max(0, (1 - cond))
    fk += fk_secondPart
    fks3.append(fk)

    # calculate delta
    if k == 0:
        pass
    elif k == 1:
        delta = abs(fks3[k - 1] - fks3[k]) / fks3[k - 1] * 100
        deltas.append(delta)
    else:
        delta = abs(fks3[k - 1] - fks3[k]) / fks3[k - 1] * 100
        delta_curr = 0.5 * deltas[k - 1] + 0.5 * delta
        deltas.append(delta_curr)
        if delta_curr <= epsilon:
            break

    # increment # of iteration
    k += 1
    l = (l + 1) % ((dataNumbers + batch_size - 1) / batch_size)

end = time.clock()
timeUsed = end - start
print(timeUsed)

if os.path.isfile('mini.txt'):
    os.remove("mini.txt")
if os.path.isfile('mini.time.txt'):
    os.remove("mini.time.txt")

with open('mini.txt', 'a') as write_file:
    for i, each in enumerate(fks3):
        write_file.write(str(i) + "," + str(each) + '\n')
with open('mini.time.txt', 'a') as write_file:
    write_file.write(str(timeUsed))



# make the plot!



a = plt.subplot(1,1,1)
a1 = a.plot(np.arange(1,len(fks) + 1), fks, "b-", label = 'BGD',linewidth=0.6)
a2 = a.plot(np.arange(1,len(fks2) + 1), fks2, "r-", label = 'SGD', linewidth=0.6)
a3 = a.plot(np.arange(1,len(fks3) + 1), fks3, "g-", label = 'MBGD', linewidth=0.6)
plt.xlabel("# of iterations")
plt.ylabel("cost")
plt.show()
