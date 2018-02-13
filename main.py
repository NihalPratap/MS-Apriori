from __future__ import division
import re
import operator
import math
import collections
from collections import Counter
import math
      
#importing transacction data
with open(r'/home/nihal/data_pj1/input.txt', 'r') as infile,open(r'/home/nihal/data_pj1/input1.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace("{", "")
    data = data.replace("}", "\n")
    data = data.replace(" ", "")
    data = data.replace("<", "")
    data = data.replace(">", "")
    data = data.strip(',')
    outfile.write(data)


with open('/home/nihal/data_pj1/input1.txt',) as f:
    transactions = [[ int(j) for j in i.split(',')]for i in f.read().split("\n")]



#loading MIS values
SDC = 0
must_have = []
cannot_be_together = []
MIS = {}
with open('parameterFile.txt') as f:
    lines = f.readlines()
    for line in lines:
        list1 = re.findall(r'^must-have: .*[\d*\.\d+].*$',line)
        if list1:
            must_have = re.findall("\d+\.?\d*",str(list1))


        list2 = re.findall(r'^cannot_be_together: .*[\d*\.\d+].*$',line)
        if list2:
            s = re.findall("\d+",str(list2))
            i  = 0
            while i < len(s):
                cannot_be_together.append(tuple((s[i],s[i+1])))
                i = i + 2
            

        list3 = re.findall(r'^SDC = \d*\.\d+',line)
        if list3:
            q = re.findall("\d+\.\d+",str(list3))



        list4 = re.findall(r'^MIS.*\d*\.\d+$',line)
        if list4:
            list5 = re.findall(r'\d*\.\d+|\d+',str(list4))
            dict = {list5[0] : list5[1]}
            MIS.update(dict)
sorted_MIS = sorted(MIS.items(), key=operator.itemgetter(1))


#setting the counter variable
c = collections.Counter()
for sublist in transactions:
    c.update(sublist)



# function to calculate the subsets of itemset
import itertools
def subs(l):
    res = []
    i = len(l)-1
    for combo in itertools.combinations(l, i):
    	res.append(list(combo))
    return res
                
                
SDC=float(q[0])
#SDC = 1.0

def level2candidategen(L,SDC):
    C = []
    for i in range(0,len(L)):
        if float(c[int(L[i])]/len(transactions)) >= float(MIS[L[i]]):
            for j in range(i+1,len(L)):
                if float(c[int(L[j])]/len(transactions)) >= float(MIS[L[i]]):
                    if abs(float(c[int(L[j])]/len(transactions)) - float(c[int(L[i])]/len(transactions))) <= float(SDC):
                        tp = [L[i],L[j]]
                        C.append(tp); 
    return C;



def MScandidategen(F,SDC):
    F1=[x[:-1] for x in F]
    F2=[x[-1] for x in F]
    temp1=[]
    for k in range(0,len(F1)):
        for j in range(0,len(F1)):
            if F1[k] == F1[j]:
                if int(F2[k]) < int(F2[j]):# double check
                    if abs(float(c[int(F2[k])]/len(transactions)) - float(c[int(F2[j])]/len(transactions))) <= float(SDC):
                        T = list(F1[k])
                        T.append(F2[k])
                        T.append(F2[j])
                        temp1.append(T)
    for val in temp1:
        X=subs(val)
        for item in X:
            if val[0] in item or (MIS[val[1]]==MIS[val[0]]): #condition
                if item not in F:
                    temp1.remove(val)
                    break;
    return temp1
            

L = []                     #List L (init-pass)
h=0;
ele = 0

for key in sorted_MIS:
    if (float(c[int(key[0])]/len(transactions))) >= float(key[1]):
        ele=key[0];
        break;
    else:
        h=h+1;

L.append(ele)

for key in sorted_MIS[h+1:]:            
    if float(c[int(key[0])]/len(transactions)) >= float(MIS[ele]):
        L.append(key[0])

F = []  #List F for first frequent items
if must_have:
	for key in L:
		if float(c[int(key)]/len(transactions)) >= float(MIS[key]):
			if key in must_have:
				F.append(key)
else:
	for key in L:
		if float(c[int(key)]/len(transactions)) >= float(MIS[key]):
			F.append(key)

k = 2;
C = []

print "frequent item set-1"				#print frequent item set 1
for var in F:
    print c[int(var)], " : " , var
print "total no of frequent itemsets ",len(F)


while F:
    if k == 2:
        C = level2candidategen(L,SDC)
    else:
    	C = []
        C = MScandidategen(F,SDC)

    if C and k > 1:
    	print "     "
        print "frequent item set-",k
    temp = []							#List temp is used to copy frequent items into F after printing
    tempc = []
    tempt = []
    temp2 = []
    for key in C:
        keylist=list(key);
        fin_count=0;
        c_count=0;
        for item in transactions:
            count=0;
            count1=0;
            i = 0;
            while i < len(keylist):
                if int(keylist[i]) not in item:
                    break;
                else:
                    count=count+1;
                i = i + 1
            if len(keylist)==count :
                fin_count=fin_count+1
            
            j=0
            F3 = keylist[1:len(keylist)]
            while j < len(F3):
                if int(F3[j]) not in item:
                    break;
                else:
                    count1=count1+1;
                j = j + 1
            if len(F3)==count1 :
                c_count=c_count+1   
        if keylist:
            if (float(fin_count/len(transactions))) >=float(MIS[keylist[0]]):
            	temp2.append(key)
                temp.append(key)
                tempc.append(fin_count)
                tempt.append(c_count)
                if cannot_be_together:
                	for item in temp:					#implementing cannot be together
                		for can in cannot_be_together:
                			count3 = 0
                			for l in range(0,len(can)):
                				if can[l] not in item:
                					count3 = count3 + 1
                			if count3 == 0:
                				temp.remove(key)
                				tempc.remove(fin_count)
                				tempt.remove(c_count)
        if must_have:
        	for a in range(0,len(temp)):				#implementing must_have
        		track = 0
        		for must in must_have:
        			if must in temp[a]:
        				break;
        			else:
        				track = track + 1
        		if track == len(must_have):
        			temp.remove(temp[a])
        			tempc.pop(a)
        			tempt.pop(a)
    s = 0
    while s < len(temp):							#print the frequent items sets and count
        print tempc[s]," : ",temp[s]
        print "tail count is-",tempt[s]
        s = s + 1
    if temp:
    	print "total no of frequent itemsets", len(temp)
    F = temp2    
    k = k + 1