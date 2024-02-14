import numpy as np

x = 4 
y = 5 

u = 6
v = 9 
tab = []


tab = np.append([],(int(x),int(y)))
print(tab) 

tab = np.append(tab,(int(u),int(v)))
print(tab)


for i in range(2): 
    print(tab[i][0],tab[i][1])
