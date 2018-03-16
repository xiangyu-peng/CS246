#homework 4 Q4
#Data Stream

import sys
import math
import time
import numpy as np
import matplotlib.pyplot as plt

#parameters
delta = math.pow(math.e, -5)
epsilon = math.e * math.pow(10, -4)
p = 123457
n_buckets = int(math.e / epsilon)

# hash function parameters 5 tuples = 5 (a, b)
hashParams = []
hash_file = open("F:\cs246\homework4\hash_params.txt", "r")
for line in hash_file:
    items = line.strip().split("\t")
    hashParams.append((int(items[0]), int(items[1])))
hash_file.close()


# hash functions
def hash_func(hashParams, p, n_buckets, x):
    res = []
    for i in range(len(hashParams)):
        y = x % p
        hash_val = (hashParams[i][0] * y + hashParams[i][1]) % p
        r = hash_val % n_buckets
        res.append(r)
    return res

# Initialize the hash matrix
matrix = np.zeros((len(hashParams), n_buckets))

# Read words file
words_file = open("F:\cs246\homework4\words_stream.txt", "r")
count_words = 0
for line in words_file:
    count_words += 1
    x = int(line.strip())
    hash_vals = hash_func(hashParams, p, n_buckets, x)
    for i in range(len(hashParams)):
        matrix[i][hash_vals[i]] += 1                               #hash the word to the buckets and record through matrix
words_file.close()



errors = []
freqs = []
# calculate the error
count_file = open("F:\cs246\homework4\counts.txt", "r")
count_error = 0
for line in count_file:
    count_error += 1
    items = line.strip().split("\t")
    id = int(items[0])
    freq = int(items[1])
    hash_vals = hash_func(hashParams, p, n_buckets, id)
    freqEstimate = sys.maxsize
    for i in range(len(hashParams)):
        freqEstimate = min(freqEstimate, matrix[i][hash_vals[i]])
    error = (freqEstimate - freq) / freq
    errors.append(error)
    freqs.append(freq / count_words)
count_file.close()


#plot the figure
plt.loglog(freqs, errors, "+")
plt.title("Relative Error vs Word Frequency")
plt.xlabel("Word Frequency (log)")
plt.ylabel("Relative Error (log)")
plt.grid()
plt.show()
