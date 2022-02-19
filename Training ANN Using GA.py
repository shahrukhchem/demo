# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 00:01:50 2021

@author: Shahrukh
"""

import numpy as np 
import random 
import math
import pandas as pd

def genrating_weight_between_layer(l1,l2,lower_limit=-1,upper_limit=1):
    weight_matrix=np.random.randint(lower_limit, upper_limit, (l1,l2))+np.random.rand(l1,l2);
   # weight_matrix=np.random.rand(l1,l2);
    
    return weight_matrix


def neuron_value_of_layer(NVofpreviouslayer,wbl):
    a=NVofpreviouslayer
    a=a.transpose()
    return np.dot(a,wbl)

def activation_functions_on_neurons(output_neurons):
    e=2.718
    sigmoid_func= lambda x:(1/(1+e**(-x)))
    #vectorized_sigmoid_func = np.vectorize(sigmoid_func)
    s=sigmoid_func(output_neurons)
    return s
    
def Initializing_the_network(Architechture_list):
    Weights_list=[]
    for i in range(0,len(Architechture_list)-1):
         Weights_list.append(genrating_weight_between_layer(Architechture_list[i],Architechture_list[i+1]))
         
    return Weights_list
    
    
#define Architechture of ANN in form of list where length of list is number of layers
#each element in the list signifies number of Neurons in layers

def forward_pass_on_network(weights_of_network,Input_value):
    Outputlayer=Input_value
    for i in range(0,len(weights_of_network)):
        Outputlayer=neuron_value_of_layer(Outputlayer,weights_of_network[i])
        Outputlayer=activation_functions_on_neurons(Outputlayer)
        Outputlayer=Outputlayer.transpose()
    column_wise_sum=np.sum(Outputlayer,axis=0)
    Outputlayer=Outputlayer/column_wise_sum    
    return Outputlayer


def computing_loss(predicted_value,true_value):
    r,NOE=predicted_value.shape
    logloss=np.log(predicted_value)
    loss=np.multiply(true_value.transpose(),logloss)
    loss=np.sum(np.sum(loss))
    loss=-1*loss/NOE
    return loss



No_of_layer=4
Input_layer=3      #Input Layer with 2 feature
hidden_layer1=4     ##No of Neuron in hidden layer 1
hidden_layer2=20   #No of Neuron in hidden layer 2
output_layer=2       #No of Neuron Out put layer 2   

Architechture_list=[Input_layer,hidden_layer1,hidden_layer2,output_layer]
weights_of_network=Initializing_the_network(Architechture_list) 
#Input_value=np.random.randint(0, 10, (Input_layer,2))
#Input_value=np.array([1,1])
data=pd.read_csv(r'C:\Users\Shahrukh\Linear Optimization using CPLEX\dummydata.csv')
#No of columns
l=len(data. columns)
Input_value=data.iloc[:,0:(l-1)]
Input_value=Input_value.to_numpy()
Input_value=Input_value.transpose()
Output_value=data.iloc[:,l-1]
Output_value=pd.get_dummies(Output_value)
Output_value=Output_value.to_numpy()
Output_of_input=forward_pass_on_network(weights_of_network,Input_value)
loss=computing_loss(Output_of_input,Output_value)

def Generating_Population(popnumber):
    pop=[]
    for i in range(0,popnumber):
        pop.append(Initializing_the_network(Architechture_list) )
        
    return pop

def fitness_of_networks(pop):
    networks=[]
    for i in range(0,len(pop)):
        won=pop[i]
        OOI=forward_pass_on_network(won,Input_value)
        loss=computing_loss(OOI,Output_value)
        fitness=1/loss #higher the fitness of network lower the loss
        c=(won,fitness)
        networks.append(c)
    return networks

def selecting_among_population(population_score,elite_size):
    sorted_population = sorted(population_score, key=lambda x: x[1],reverse=True)
    return sorted_population[0:elite_size]

def matingpool(selected_population):
    mating_pool = [a[0] for a in selected_population]
    return mating_pool


def breedpopulation(mating_pool,npop):
    children=[]
    length=len(mating_pool)
    for i in range(0,npop):
        parents=np.random.choice(range(0,len(mating_pool)), size=(2,1), replace=False)
       
        parent1=mating_pool[int(parents[0])]
        parent2=mating_pool[int(parents[1])]
        child=[]
        for j in range(0,len(parent1)):
            w=np.random.rand()
            child.append(w*parent1[j]+(1-w)*parent2[j])
        children.append(child)
    return children
        
        
        
        
pop=Generating_Population(100)    
net=fitness_of_networks(pop)
sop=selecting_among_population(net,20)
#sop=selecting_among_population(net,2)
mp=matingpool(sop)
childs=breedpopulation(mp,100)
gen1=fitness_of_networks(childs)


for i in range(0,1000):
    net=fitness_of_networks(pop)
    sop=selecting_among_population(net,20)
    #sop=selecting_among_population(net,2)
    mp=matingpool(sop)
    childs=breedpopulation(mp,100)
    gen=fitness_of_networks(childs)
    print('fitness score',sum([x[1] for x in gen])/len(gen))
    pop=[p[0] for p in gen]

fn=gen[0]
fn=fn[0]

Output_of_input=forward_pass_on_network(fn,Input_value)
loss=computing_loss(Output_of_input,Output_value)




