#Ben Moreau

import numpy as np
from math import *
from matplotlib import pyplot as plt
import os
from scipy import optimize
##
#
## DONT RUN THIS IN SHELL, IT WONT WORK. RUN IT IN PYTHON 3 FROM TEH CMB or TERMIANAL
#
#
res_f0=open("Dice_Roll_Res0.txt","w+")
res_f1=open("Dice_Roll_Res1.txt","w+")
powers = open("Det power and actual power.txt","w+")
param=open("param.txt","w+")
Num_exp=100
Num_rolls=1000
Num_sides=20
Side_number=11#default
Dice_Power_Lower=1
Dice_Power_Upper=1.6
print("Input custom values? Y/N")
y=input()
while(y!="Y" and y!="N"):
    print("Input custom values? Y/N")
    y=input()

if(y=="Y"):
    print("input the number of exp:")
    Num_exp=float(input())
    print("input the number of rolls/exp:")
    Num_rolls=float(input())
    print("input the number of side on the die:")
    Num_sides=float(input())
    print("input the number of the side you want to test for:")
    Side_number=float(input())
    print("input lower limit of the dices uniform weight (it may cause errors for values above 1.8 or so):")
    Dice_Power_Lower=float(input())
    print("input upper limit of the dices uniform weight (it may cause errors for values above 1.8 or so):")
    Dice_Power_Upper=float(input())
Num_exp=int(Num_exp)
Num_rolls=int(Num_rolls)
Num_sides=int(Num_sides)
Side_number=int(Side_number)
#user input . pls don't put in weird values or it will get messed up
print("A")
for i in range(10):
    param.write("Num_exp Num_rolls Num_sides Side_number Dice_Power_Lower Dice_Power_Upper"+"\n") #need this or else it wont work for some reason




if(Side_number>Num_sides):
    print("Number of sides updated to ",Side_number+1)
for i in range(100):
    param.write(str(Num_exp)+" "+str(Num_rolls)+" "+str(Num_sides)+" "+str(Side_number)+" "+str(Dice_Power_Lower)+" "+str(Dice_Power_Upper)+"\n")

avg_result=0#define vars
Exp_res=[]
Exp_successes=[]
Roll_res=[]
Npass0=[]
LogLikeRatio0=[]


####Define a function based on the power of the weight
# Minimizing this function of the power should give us the power
Npass=0
def Like(power):
    if(power==0):
        print(power)
        print(Roll_res)
    if(power>5):
        print(power)
        print(Roll_res)
            
    ns = Npass
    nf = Num_rolls-Npass
    pC=[1000000000]
    for mm in range(Num_sides-1):
        pC.append(pC[0]/power**(mm+1)) #For a dice cube weighted so that the probability of a side is lowered by a factor of Dice_power for each side greater than 1
        
    #print(sum(p1))
    Sp1=float(sum(pC))
    for mm in range(Num_sides):
        pC[mm]=float(float(pC[mm])/float(Sp1))
    
    return -(sum(pC[Side_number-1:])**ns*(1-sum(pC[Side_number-1:]))**nf) #-Likelihood

#####


avg_result=sum(Exp_res)/Num_exp
Exp_res1=[]
Exp_successes1=[]
Npass1=[]
Dice_powers_C=[]
Dice_powers_A=[]


for i in range(Num_exp):
###
    p1=[100000000]
    Dice_power=np.random.randint(Dice_Power_Lower*10**18,Dice_Power_Upper*10**18)/10**18
    for mm in range(Num_sides-1):
        p1.append(p1[0]/Dice_power**(mm+1)) #For a dice cube weighted so that the probability of a side is lowered by a factor of Dice_power for each side greater than 1
        
        #print(sum(p1))
    Sp1=sum(p1)
    for mm in range(Num_sides):
        p1[mm]=p1[mm]/Sp1
    #Those probabilities for the loaded die sum to 1

    Roll_res=[]
    LLR = 0
    Npass=0
    for l in range(Num_rolls):

        
        a=np.random.randint(1,10**18+1)/10**18*Dice_power**Num_sides
        
        #print(a)
        lmno=1
        while(1==1):

            if(a>Dice_power**(Num_sides-lmno)):
                a=lmno#Choose the side number in a way that reflects the exponent, for a factor of two, 1 has a 50% chance, 2 has a 25% chance, etc.
                break;

            #if a is too small, it is the least probable side
            if(lmno>len(p1)-2):
                a=lmno
                break;
            lmno+=1
        res_f1.write(str(a)+" "+str(Dice_power)+"\n")

        #print(a)
        if(a>=Side_number):

            
            Roll_res.append(1) #If the random number is higher than the side number specified, the roll was a success
            Npass += float(1)

        else:
            Roll_res.append(0) #Conversely, it fails
    
    Npass1.append(Npass)
    #Calculate the power of the weight by minimizing the negative likelihood (maximizing likelihood)
    result = optimize.minimize_scalar(Like,[1,1.5],method="Brent", tol=np.finfo(1.).eps,bounds=[1,5])
    powers.write(str(result.x)+" "+str(Dice_power)+"\n")
    #print(result)
