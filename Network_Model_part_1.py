# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:00:47 2021

@author: Shahrukh
"""
capacities = {1: 15, 2: 20}
demands = {3: 7, 4: 10, 5: 15}
costs = {(1,3): 2, (1,5):4, (2,4):5, (2,5):3} #cost_values_for_Source_target_values


source = range(1, 3) # {1, 2}
target = range(3, 6) # {3,4,5}


from docplex.mp.model import Model

m=Model(name='Transportation Network')

x = {(i,j): m.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in source for j in target}
#m.minimize()
m.minimize(m.sum(x[i,j]*costs.get((i,j),0) for i in source for j in target))

# for each node, total outgoing flow must be smaller than available quantity
for i in source:
    m.add_constraint(sum(x[i,j] for j in target)<=capacities[i],ctname='C1')
    
#for each target node, total ingoing flow must be greater thand demand    
for i in target:
     m.add_constraint(sum(x[j,i] for j in source)>=demands[i])
     
ms=m.solve()
ms.get_value(x[1,4])
for i in source:
    for j in target:
            print('quantity tarnsported from',i,'to ',j, 'is',ms.get_value(x[i,j]))
m.get_constraint_by_name('C1')     #How to see the constraint by name