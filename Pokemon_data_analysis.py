# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 17:08:13 2021

@author: Shahrukh
"""

import pandas as pd
import numpy as np

df=pd.read_csv('pokemon_data.csv')
df.head()
#read headers
print(df.columns)
print(df['Name'])
#reading rows
print(df.iloc[1])


#iterating over rows

for i,r in df.iterrows():
    print(i,r['Name'])


df.loc[df['Type 1']=="Grass"]

df.describe()


#sorting_Describing_value
sorted_df=df.sort_values(['Name','HP'],ascending=[False,False])

#MakingChangesto Data

df['Total']=df['HP']+df['Attack']+df['Defense']+df['Sp. Atk']+df['Sp. Def']+df['Speed']



