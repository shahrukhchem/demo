# -*- coding: utf-8 -*-
"""
Created on Sat May 15 17:17:55 2021

@author: Shahrukh
"""
#Ridge_Regression

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures,MinMaxScaler
data={'Market Spending (Million $)': [23,26,30,34,43,48],
      'Sales (Million $)': [651,762,856,1063,1190,1298]
      }
df=pd.DataFrame(data)
sns.scatterplot(x=df['Market Spending (Million $)'],y=df['Sales (Million $)'])
#SCaling BEtween Zero and One
scaler=MinMaxScaler()
df[['Market Spending (Million $)','Sales (Million $)']]=scaler.fit_transform(df[['Market Spending (Million $)','Sales (Million $)']])

sns.scatterplot(x=df['Market Spending (Million $)'],y=df['Sales (Million $)'])
#Fit Linear REGRESSIONLINE
reg=LinearRegression()
reg.fit(data['Market Spending (Million $)'],data['Sales (Million $)'])
