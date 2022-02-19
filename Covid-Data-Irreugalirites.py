# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 15:36:58 2021

@author: Shahrukh

"""


import pandas as pd

covid_data=pd.read_csv('C:/Users/Shahrukh/DS_ML_AI_Python/state_wise_daily.csv')

covid_data_confirmed = covid_data[covid_data.Status == 'Confirmed']


def calculating_benford_data(covid_data_confirmed):
    c=covid_data_confirmed['UP'].astype(str)
    covid_data_confirmed['Leading_Digit']=c[c.index][0]
    
    
    return covid_data_confirmed
    
