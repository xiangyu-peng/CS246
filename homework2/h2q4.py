#homework 2 Q3

import numpy as np


#open file
file_name="F:\cs246\homework2\hw2-q4-dataset\q1-dataset\q1-dataset\\user-shows.txt"
R = np.loadtxt(file_name, delimiter=" ")
R_t= R.T

#Compute P and Q
P_before=np.dot(R,R_t)
P=np.zeros([len(P_before),len(P_before[0])])
for i in range(len(P)):
    for j in range(len(P[i])):
        if i == j:
            P[i][j]=P_before[i][j]

Q_before=np.dot(R_t,R)
Q=np.zeros([len(Q_before),len(Q_before[0])])
for i in range(len(Q)):
    for j in range(len(Q[i])):
        if i == j:
            Q[i][j]=Q_before[i][j]

# Shows' name
file_name = "F:\cs246\homework2\hw2-q4-dataset\q1-dataset\q1-dataset\\shows.txt"
showsName = open(file_name, 'r')
names_list = []
for eachline in showsName:
    names = eachline.strip().strip("\"").split("\"\"")
    names_list += names

#Compute collaborative filtering recommendations: gama
P_sqrt = np.zeros([len(P_before),len(P_before[0])])
for i in range(len(P_sqrt)):
    for j in range(len(P_sqrt[i])):
        if i == j:
            P_sqrt[i][j]=1/np.sqrt(P[i][j])
gama = np.dot(P_sqrt, R)
gama = np.dot(gama, R_t)
gama = np.dot(gama, P_sqrt)
gama = np.dot(gama, R)

#Compute Alex's score

index=499#Alex is the 500th user
S=gama[index]
top100list=[]
for i in range(100):
    top100list.append((i,S[i]))
func = lambda x: x[1]
top100list = sorted(top100list, key=func, reverse=True) #sort the first 100 scores

# get the top five name and score
topFive_Name_score=[]
for i in range(5):
    topFive_Name_score.append((names_list[int(top100list[i][0])], top100list[i][1]))


# Compute movie-movie gama2
Q_sqrt = np.zeros([len(Q_before),len(Q_before[0])])
for i in range(len(Q_sqrt)):
    for j in range(len(Q_sqrt[i])):
        if i == j:
            Q_sqrt[i][j]=1/np.sqrt(Q[i][j])

gama2 = np.dot(R, Q_sqrt)
gama2 = np.dot(gama2, R_t)
gama2 = np.dot(gama2, R)
gama2 = np.dot(gama2, Q_sqrt)

#Compute Alex's score
index=499#Alex is the 500th user
S2=gama2[index]
top100list2=[]
for i in range(100):
    top100list2.append((i,S2[i]))
func = lambda x: x[1]
top100list2 = sorted(top100list2, key=func, reverse=True) #sort the first 100 scores

# get the top five name and score
topFive2_Name_score=[]
for i in range(5):
    topFive2_Name_score.append((names_list[int(top100list2[i][0])], top100list2[i][1]))

print(topFive_Name_score)
print(topFive2_Name_score)