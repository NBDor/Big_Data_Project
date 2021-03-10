import numpy as np
from random import sample

"""
Crossover functions to be compared
"""

# Order Crossover (OX)
def ox(p1, p2, n):
    c1 = np.zeros(n, dtype=int)
    c2 = np.zeros(n, dtype=int)

    a,b = sample(range(n+1),2)
    a,b = min(a,b),max(a,b)    

    c1[a:b]=np.copy(p1[a:b])
    c2[a:b]=np.copy(p2[a:b])

    j1=j2=0

    for i in range(n):

        if j1>=a and j1<b:
            j1=b
        if j2>=a and j2<b:
            j2=b

        if p1[i] not in p2[a:b]:
            c2[j1]=np.copy(p1[i])
            j1+=1
        if p2[i] not in p1[a:b]:
            c1[j2]=np.copy(p2[i])
            j2+=1

    return c1,c2

# Position-Based Crossover (PX)
def px(p1, p2, n):
    c1 = np.zeros(n, dtype=int)
    c2 = np.zeros(n, dtype=int)

    points = sample(range(n),n//2)
    
    for p in points:
        c1[p]=np.copy(p1[p])
        c2[p]=np.copy(p2[p])

    j1=0
    j2=0
    for i in range(n):
        if p1[i] not in c2:
            while c2[j1]!=0:
                j1+=1
            c2[j1]= np.copy(p1[i])
        if p2[i] not in c1:
            while c1[j2]!=0:
                j2+=1
            c1[j2]= np.copy(p2[i])
            
    return c1,c2

# Cycle Crossover (CX)
def cx(p1,p2,n):
    c1 = np.zeros(n, dtype=int)
    c2 = np.zeros(n, dtype=int)
    
    c1[0]= np.copy(p1[0])
    
    l=0
    i=0
    while True:
        if p2[l]==c1[0]:
            break

        if p1[i] == p2[l]:
            c1[i]= np.copy(p1[i])
            l=i
        i=(i+1)%n
     
    l=0
    i=0
    while True:
        if p1[l]==c2[0]:
            break

        if p2[i] == p1[l]:
            c2[i]= np.copy(p2[i])
            l=i
        i=(i+1)%n
    
    j1=0
    j2=0
    for i in range(n):
        if p1[i] not in c2:
            while c2[j1]!=0:
                j1+=1
            c2[j1]= np.copy(p1[i])
        if p2[i] not in c1:
            while c1[j2]!=0:
                j2+=1
            c1[j2]= np.copy(p2[i])
            
    return c1,c2
    

"""
Mutation functions to be compared
"""

# Reverse Sequence Mutation (RSM)
def rsm(chromosome, n):
    a,b = sample(range(n+1),2)
    a,b = min(a,b),max(a,b)  
    chromosome[a:b]=chromosome[a:b][::-1]
    
# Twors Mutation
def twors(chromosome, n):
    a,b = sample(range(n),2)
    chromosome[a],chromosome[b] = chromosome[b],chromosome[a]

# Insertion Mutation (IM)
def im(chromosome,n):
    c = int(np.random.random()*n)
    p = int(np.random.random()*n)
    
    if c==p:
        return
    num = np.copy(chromosome[c])
    
    if p<c:
        for i in range(c,p,-1):
            chromosome[i]=chromosome[i-1]
    else:
        for i in range(c,p,1):
            chromosome[i]=chromosome[i+1]
            
    chromosome[p]=num
    
# Centre inverse mutation (CIM)
def cim(chromosome, n):
    
    p = int(np.random.random()*n)
    chromosome[0:p]=chromosome[0:p][::-1]
    chromosome[p:n]=chromosome[p:n][::-1]

# Partial Shuffle Mutation (PSM)
def psm(chromosome, n):
    i = int(np.random.random()*n)
    while i<n:
        i+=1
        a = int(np.random.random()*n)
        b = int(np.random.random()*n)
        chromosome[a],chromosome[b] = chromosome[b],chromosome[a]
        