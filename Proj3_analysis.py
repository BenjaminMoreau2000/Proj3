#Ben Moreau

import numpy as np
from math import *
from matplotlib import pyplot as plt
import os

Num_exp=np.genfromtxt("param.txt",skip_header=1)[101,0]
Num_rolls=np.genfromtxt("param.txt",skip_header=1)[101,1]
Num_sides=np.genfromtxt("param.txt",skip_header=1)[101,2]
Side_number=np.genfromtxt("param.txt",skip_header=1)[101,3]
DPL=np.genfromtxt("param.txt",skip_header=1)[101,4]
DPU=np.genfromtxt("param.txt",skip_header=1)[101,5]

DPC=np.genfromtxt("Det power and actual power.txt")[:,0]
DPA=np.genfromtxt("Det power and actual power.txt")[:,1]



Num_rolls=int(Num_rolls)
# make LLR figure

plt.scatter(DPA,DPC,label="H_1")
plt.scatter(DPA,(abs(DPA-DPC)),label="Error of prediction")

print("Number of experiments:")
print(Num_exp)
print("Number of rolls per experiment:")
print(Num_rolls)
print("Number of sides on the die:")
print(Num_sides)
print("Test side number:")
print(Side_number)
print("Lower limit for the exponential die weight:")
print(DPL)
print("Upper limit for the exponential die weight:")
print(DPU)







   


plt.xlabel('Real weight')
plt.ylabel('Calculated weight')
plt.title("H_1 has a weight with random distribution from "+str(DPL)+" to "+str(DPU))
plt.grid(True)

##Make prediction function
##Calculate stand err

z = np.polyfit(DPA, DPC, 3)
Yu=[]
Yl=[]
stde=0
for i in range(len(DPA)):
    x=DPA[i]
    y_exp = z[0]*x**3+z[1]*x**2+z[2]*x+z[3]
    stde+=abs(y_exp-DPC[i])/np.sqrt(len(DPA))

for i in range(len(DPA)):
    Yu.append(DPC[i]+stde)
    Yl.append(DPC[i]-stde)


    
Xpred=np.linspace(DPL,DPU,1000)
Ypred =z[0]*Xpred**3+z[1]*Xpred**2+z[2]*Xpred+z[3]

plt.scatter(DPA,Yu,marker="^",s=5,label="combined standard deviation of prediction",color="red")
plt.scatter(DPA,Yl,marker="v",s=5,color="red")
plt.plot(Xpred,Ypred,label="Fit function",color="black")
plt.legend()
print("Combined stdev:")
print(stde)
plt.show()


















