import numpy # if cannot find numpy: open cmd and type "pip install numpy"
from numpy import *;
import numpy as np;
import scipy
from scipy import linalg

M = np.array(((1, 2), (2, 1), (3, 4), (4, 3)))
U, s, Vh = linalg.svd(M, full_matrices=False)

Evals, Evecs=linalg.eigh(np.dot(M.T,M))
print("Evals =",Evals);
print("Evecs =",Evecs);
list=[];
for i in range(len(Evals)):
    list.append((Evals[i], (Evecs.T)[i]))
func = lambda x : x[0]
sortedList = sorted(list, key = func, reverse=True)
print (sortedList);