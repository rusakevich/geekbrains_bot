import re
import numpy as np
from scipy import spatial
with open("C:/Users/v_rusakevich/Desktop/sentenses.txt", 'r') as f:
    sentence = list(f)
    sen = []
    for w in sentence: sen.append(w.lower())

with open("C:/Users/v_rusakevich/Desktop/sentenses.txt", 'r') as f:
    text = f.read().lower()
    word = list(frozenset(re.split('[^a-z]', text)))
    word.remove('')
 
print(len(word)) 
m = []
for s in sen:
    k = []

    for j in word:
        h = 0
        for i in re.split('[^a-z]', s):
        
            if j == i:
                h += 1
        k.append(h)
    m.append(k)

M = np.array(m)
print(M)
g=1
d=[]
while g < 22:
    d.append('{}-{}'.format(spatial.distance.cosine(M[0,:],M[g,:]),g))
    g+=1
d.sort()
print(d)




