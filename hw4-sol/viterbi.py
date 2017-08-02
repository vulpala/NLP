import sys
import math
import decimal
import collections
#f1 = open(sys.argv[1], 'r')
#f2 = open(sys.argv[2], 'r')
f1 = open('sents.txt')
f2 = open('probs.txt')
probs = []
sents = []
postags = ['noun', 'verb', 'inf', 'prep']
poslen = postags.__len__()
while True:
    line = f2.readline()
    if not line:
        break
    else:
        l = line.split()
        probs.append([l[0] + " " + l[1], l[2]])
while True:
    line = f1.readline()
    if not line:
        break
    else:
        sents.append(line)
def vitprobs(viterbi):
    print "FINAL VITERBI NETWORK"
    a = 0
    while (a < viterbi.__len__()):
        print "P(" + viterbi[a][0]+"="+viterbi[a][1] + ")" + " = " + str(format(viterbi[a][5], '.10f'))
        a = a + 1
def sentences(sent):print ("\nPROCESSING SENTENCE:" + sent)
def backptr(viterbi):
    print "\nFINAL BACKPOINTER NETWORK"
    a = poslen
    while (a < viterbi.__len__()):
        print "Backptr("+viterbi[a][0]+"="+viterbi[a][1]+")" + " => " + viterbi[a][4]
        a = a + 1
def besttag(viterbi, il):
    maxProb = viterbi[il][5]
    tempi = il
    string = ""
    while True:
        string = string + viterbi[tempi][0] + "->" + viterbi[tempi][1] + "\n"
        tempi = viterbi[tempi][6]
        if (tempi == '$'):
            break
    print "\nBEST TAG SEQUENCE HAS PROBABILITY = " + str(format(maxProb, '.10f'))
    print string
def forprobs(viterbi):
    seqSum = []
    seq = 0
    count = 0
    value = 0
    while (count < viterbi.__len__()):
        value = value + float(viterbi[count][7])
        if (seq == poslen - 1):
            seqSum.append(value)
            seq = 0
            value = 0
            count += 1
            continue
        seq += 1
        count += 1
    print "FORWARD ALGORITHM RESULTS"
    count = 0
    while (count < viterbi.__len__()):
        print "P(" + viterbi[count][0]+"="+viterbi[count][1] + ") = " + str(format(float(viterbi[count][7] / seqSum[int(count / poslen)]), '.10f'))
        count = count + 1
for sentence in sents:
    a = 0
    vitl = []
    words = sentence.split()
    for word in words:
        for pos in postags:
            vitl.append([word, pos, 0.0, 0.0, "Undefined", 0.0, 0, 0.0])
    while (a < vitl.__len__()):
        x = 0
        y = 0
        for t in probs:
            if ((vitl[a][0] + " " + vitl[a][1]).lower() in t[0]):
                vitl[a][2] = t[1]
                x = 1
            if (a - 4 < 0):
                if (vitl[a][1] + " phi" in t[0]):
                    vitl[a][3] = t[1]
                    y = 1
        if (x == 0):
            vitl[a][2] = 0.0001
        if (y == 0):
            vitl[a][3] = 0.0001
        if (a - 4 < 0):
            vitl[a][4] = "$"
            vitl[a][5] = float(vitl[a][2]) * float(vitl[a][3])
            vitl[a][6] = "$"
            vitl[a][7] = float(vitl[a][2]) * float(vitl[a][3])
        else:
            if (a % poslen == 0):
                diff = 1
            else:
                diff = (a % poslen) + 1
            c = a - diff
            temp = 0
            ind = 0
            test = 0
            maxVal = 0
            forwardProb = 0.0
            while (c >= (a - (diff + poslen - 1))):
                tempstr = vitl[a][1] + " " + vitl[c][1]
                flag = 0
                val = 0
                for tp in probs:
                    if (tempstr.lower() in tp[0]):
                        val = tp[1]
                        flag = 1
                        break
                if (flag == 0):
                    val = 0.0001
                test = float(val) * float(vitl[c][5])
                forwardProb = forwardProb + (float(val) * float(vitl[c][7]))
                if (test > maxVal):
                    ind = c
                    maxVal = test
                c = c - 1
            vitl[a][5] = float(vitl[a][2]) * maxVal
            vitl[a][4] = vitl[ind][1]
            vitl[a][6] = ind
            vitl[a][7] = float(vitl[a][2]) * forwardProb
        a = a + 1
    max = vitl.__len__() - 1
    b = 0
    fMax = 0
    i = 0
    while (b < 4):
        if (vitl[max - b][5] > fMax):
            i = max - b
            fMax = vitl[max - b][5]
        b = b + 1
    sentences(sentence)
    vitprobs(vitl)
    backptr(vitl)
    besttag(vitl, i)
    forprobs(vitl)