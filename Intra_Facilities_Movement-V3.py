# -*- coding: utf-8 -*-

"""
Created on Sun May 30 19:53:14 2021

@author: Shahrukh
"""

import pandas as pd
from docplex.mp.model import Model
import numpy as np


def create_dummy_data():
    '''
    cities -> Name of Cities
    cm-> cost of going from City i to City J
    Initial Inventory-> Inventpry avaialbe at city i before Intra-Site Movement
    Required Inventory -> Required Inventory at Site i  after Movement
    
    '''
    cities=['City1','City2','City3','City4','City5','City6']
    cm ={}
    for i in cities:
        for j in cities:
            if (i==j):
                cm[i,j]=0
            elif (j,i) in cm:
                cm[i,j]=cm[j,i]            
            else:
                cm[i,j]=np.random.randint(50,100)
    Initial_Inventory={'City1':np.random.randint(50,60),
                       'City2':np.random.randint(50,60),
                       'City3':np.random.randint(50,60), 
                        'City4':np.random.randint(50,60),
                        'City5':np.random.randint(50,60),
                        'City6':30
                            #np.random.randint(50,60),
                                       }  #City 6 is a Head Quarter
    Required_Inventory={'City1':np.random.randint(70,80),
                       'City2':np.random.randint(20,30),
                       'City3':np.random.randint(70,80), 
                        'City4':np.random.randint(70,80),
                        'City5':np.random.randint(30,40),
                        'City6': 0,}
            
        
    #Key Represents number of Truck & Value Represent name of Truck
    Trucks_info={1:('Truck1',15),2:('Truck2',15),3:('Truck3',15),4:('Truck4',15)}
    #Capacity_of_Truck=[50,50,50,50]
    return cm ,Initial_Inventory,Required_Inventory,Trucks_info

def solve_model():
    cm,Ic,Rc,Ti=create_dummy_data()
    m=Model(name='Intra_Facilities_Movement_with_Truck_Routing',log_output=True)
    M=1000
    x=m.binary_var_cube(dict.keys(Ic),dict.keys(Ic),dict.keys(Ti),name='x%s%s%s')
    #1, if movement  of truck k takes place from  (i to j
      
   #from any city truck can go to exactly one city
    m.add_constraints(sum(x[i,j,k] for j in dict.keys(Ic) if(j!=i))
                          <=1 for i in dict.keys(Ic) for k in dict.keys(Ti))
    
    m.add_constraints(sum(x[i,j,k] for j in dict.keys(Ic) if(j!=i))-
                      sum(x[j,i,k] for j in dict.keys(Ic) if(j!=i))==0
        for i in dict.keys(Ic) for k in dict.keys(Ti))
    #cities=['C1','C2','C3','C4','C5','C6']
    cities=['City1','City2','City3','City4','City5','City6']
    Ts=m.integer_var_matrix(dict.keys(Ic),dict.keys(Ti),ub=15,name='Ts%s-%s') #delivered to 
    Tf=m.integer_var_matrix(dict.keys(Ic),dict.keys(Ti),ub=15,name='Ds%s-%s') #delivered from
    To=m.integer_var_matrix(dict.keys(Ic),dict.keys(Ti),name='To%s-%s')
    From=m.integer_var_matrix(dict.keys(Ic),dict.keys(Ti),name='From%s-%s')
    # for i in dict.keys(Ic):
    #       for j in dict.keys(Ic):
    #           for k in dict.keys(Ti):
    #                m.add_if_then(x[i,j,k]==1, To[j,k]==1)
    #                m.add_if_then(x[i,j,k]==1, From[i,k]==1)
    # m.add_constraints(x[i,j,k]==To[j,k]
    #                   for i in dict.keys(Ic)  
    #                   for j in dict.keys(Ic)  
    #                   for k in dict.keys(Ti)) 
    # m.add_constraints(x[i,j,k]==From[j,k]
    #                   for i in dict.keys(Ic)  
    #                   for j in dict.keys(Ic)  
    #                   for k in dict.keys(Ti)) 
    
    # m.add_constraints(Ts[i,k]*M>=To[i,k]
    #                   for i in dict.keys(Ic)  
    #                   for k in dict.keys(Ti)) 
    # m.add_constraints(From[i,k]*M>=Tf[i,k]
    #                   for i in dict.keys(Ic)  
    #                   for k in dict.keys(Ti))                    
    # for i in dict.keys(Ic):
          
    #           for k in dict.keys(Ti):
    #                m.add_if_then(To[i,k]==1, Ts[i,k]>=0)
    #                m.add_if_then(From[i,k]==1, Tf[i,k]>=0)
    #amount-delivered at city i for product i 
    I=m.integer_var_dict(dict.keys(Ic),name='I_%s')
    m.add_constraints(Ic[i]+
                     sum (Ts[i,k] for k in dict.keys(Ti))
                    
                        ==I[i]for i in dict.keys(Ic))
    m.add_constraints(I[i]>=Rc[i] for i in dict.keys(Ic))
    
    
    
   
    
   # m.add_constraints(I[i[0],i[1]]>=Rc[i] for i in dict.keys(Ic))

    m.minimize(m.sum(x[i,j,k]*cm[i,j] for i in dict.keys(Ic) for j in dict.keys(Ic)  for k in dict.keys(Ti)))
   
  
    
    if(m.solve()):
        m.print_information()
        m.print_solution(print_zeros=False)
    else:
        print('notsolved')
    

solve_model()
    

    
    
    
    
    
    
    
    
   