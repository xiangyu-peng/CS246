"""
Xiangyu Peng
2018/1/24
"""
#threshhold s, in this question, s=100
s = 100
test_file_name= "F:\cs246\wo.txt"
f = open(test_file_name, 'r')

# obtain all the items by looping~ and count every item~PS: Apply Dictionary~
Countitem = {}
for l in f:
    items = l.strip().split(" ")
    for item in items:
        if item in Countitem:
            Countitem[item] = Countitem[item] + 1
        else:
            Countitem[item] = 1
# get the frequent items, s=100
Frequentitem= {}
for item in Countitem:
    if Countitem[item] > s:
        Frequentitem[item] = Countitem[item]

# Count the item pairs, use dictionary~
f.seek(0)
Countpair = {}
for l in f:
    items = l.strip().split(" ")
    index=len(items);
    for i in range(index):
        for j in range(i + 1, index):
            if (items[i] in Frequentitem) and (items[j] in Frequentitem):
                key = (items[i], items[j])
                if key in Countpair:
                    Countpair[key] = Countpair[key] + 1
                else:
                    Countpair[key] = 1
                key = (items[j], items[i])
                if key in Countpair:
                    Countpair[key] = Countpair[key] + 1
                else:
                    Countpair[key] = 1
#
# Get the frequent pairs, s=100
Frequentpair = {}
for key in Countpair:
    if Countpair[key] > s:
        Frequentpair[key] = Countpair[key]

#Calculate the confidence~
confidence = []
for key, val in Frequentpair.items():
    itemA= key[0]
    itemB = key[1]
    prob = val / (1.0 * Frequentitem[itemA])
    confidence.append((itemA, prob, itemB))

print("The top 5 rules are as follows")
sortListL2 = sorted(confidence, key=lambda x:x[1], reverse = True)
for i in range(5):
    print(str(sortListL2[i][0]) + " ⇒ " + str(sortListL2[i][2]) + "   " + str(sortListL2[i][1]))

# Triple Rules
f.seek(0)
Counttriple = {}
for l in f:
    items = l.strip().split(" ")
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            for k in range(j + 1, len(items)):
                pair1 = (items[i], items[j])
                pair2 = (items[i], items[k])
                pair3 = (items[j], items[k])
                if (pair1 in Frequentpair) and (pair2 in Frequentpair) and (pair3 in Frequentpair):
                    key = (items[i], items[j], items[k])
                    if key in Counttriple:
                        Counttriple[key] = Counttriple[key] + 1
                    else:
                        Counttriple[key] = 1

                    key = (items[i], items[k], items[j])
                    if key in Counttriple:
                        Counttriple[key] = Counttriple[key] + 1
                    else:
                        Counttriple[key] = 1

                    key = (items[k], items[i], items[j])
                    if key in Counttriple:
                        Counttriple[key] = Counttriple[key] + 1
                    else:
                        Counttriple[key] = 1

                    key = (items[k], items[j], items[i])
                    if key in Counttriple:
                        Counttriple[key] = Counttriple[key] + 1
                    else:
                        Counttriple[key] = 1

                    key = (items[j], items[i], items[k])
                    if key in Counttriple:
                        Counttriple[key] = Counttriple[key] + 1
                    else:
                        Counttriple[key] = 1

                    key = (items[j], items[k], items[i])
                    if key in Counttriple:
                        Counttriple[key] = Counttriple[key] + 1
                    else:
                        Counttriple[key] = 1
# Filter  and obtain the frequent triple
Frequenttriple = {}
for key in Counttriple:
    if Counttriple[key] > s:
        Frequenttriple[key] = Counttriple[key]

#Calculate the confidence of triple
confidencetri = []
for key, val in Frequenttriple.items():
    pairA = (key[0], key[1])
    prob = val / (1.0 * Frequentpair[pairA])
    confidencetri.append((pairA, prob, key[2]))
    pairB = (key[0], key[2])
    prob = val / (1.0 * Frequentpair[pairB])
    confidencetri.append((pairB, prob, key[1]))
    pairC = (key[1], key[2])
    prob = val / (1.0 * Frequentpair[pairC])
    confidencetri.append((pairC, prob, key[0]))

confidencetri=list(set(confidencetri))

print("The top 5 rules are as follows")
sortconfidencetri = sorted(confidencetri, key=lambda x:x[1], reverse = True)
for i in range(5):
    print(str(sortconfidencetri[i][0][0]) +", "+str(sortconfidencetri[i][0][1])+ "⇒" + str(sortconfidencetri[i][2]) + "  " + str(sortconfidencetri[i][1]))