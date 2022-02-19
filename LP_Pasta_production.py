# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:40:11 2021

@author: Shahrukh
"""


'''
The model aims at minimizing the production cost for a number of products while satisfying customer demand.

Each product can be produced either inside the company or outside, at a higher cost.
The inside production is constrained by the company's resources, while outside production is considered unlimited.
The model first declares the products and the resources. The data consists of the description of the products (the demand, the inside and outside costs, and the resource consumption) and the capacity of the various resources. The variables for this problem are the inside and outside production for each product
'''
products = [("kluski", 100, 0.6, 0.8),
            ("capellini", 200, 0.8, 0.9),
            ("fettucine", 300, 0.3, 0.4)]

# resources are a list of simple tuples (name, capacity)
resources = [("flour", 20),
             ("eggs", 40)]

consumptions = {("kluski", "flour"): 0.5,
                ("kluski", "eggs"): 0.2,
                ("capellini", "flour"): 0.4,
                ("capellini", "eggs"): 0.4,
                ("fettucine", "flour"): 0.3,
                ("fettucine", "eggs"): 0.6}
#from docplex.mp.model import Model
#m=Model(name="Pasta Production")
from docplex.mp.environment import Environment
env = Environment()
env.print_information()  # ENvironment Contains info regarding other modules of interest
                          #CPLEX, Numpy & matplotlib are installed

from docplex.mp.model import Model
m=Model(name="Pasta Production")

#add variable
x=m.continuous_var_dict(products,name="Pasta Produced Outside")
y=m.continuous_var_dict(products,name="Pasta Produced Inside")


#Constraints ::: Demand Satisfaction 

#Basically, the total pasta manufactured produdecd Inside +Outside should be more than the demand 
m.add_constraints((x[prod]+y[prod]>=prod[1],'Demand_of_%s' %prod[0])for prod in products)
"""
For getting the value of resource consumed for the particular product we pass the key as a tuple in 
form of [product,resource]
"""
m.add_constraints((m.sum(y[p] * consumptions[p[0], res[0]] for p in products) <= res[1], '%s_consumed:' % res[0]) for res in resources)

m.print_information() 

#OBjective
total_inside_cost=sum(y[p]*p[2] for p in products)
total_outside_cost=m.sum(x[p]*p[3] for p in products)
m.minimize(total_inside_cost+total_outside_cost)
m.solve()
obj = m.objective_value

for p in products:
    print("Outside production of {product}: {x}".format(product=p[0], x=x[p].solution_value))


