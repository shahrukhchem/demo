# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 22:03:59 2021

@author: Shahrukh
"""

import pandas as pd
pd.set_option('display.max_columns',6)
import geopy
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans 
from scipy.spatial import distance_matrix
import numpy as np
def geo_code(df):
    locator = Nominatim(user_agent="myGeocoder")
    df['Latitude']=float("NaN")
    df['Longitude']=float("Nan")
    Nod=len(df)
    for i in range(0,Nod):
        District_name=df['District name'][131+i]
        State_name='Uttar Pradesh'
        s=District_name + ','+ State_name
        location = locator.geocode(s)
        if(location==None):
                pass
        else:
                lat=location[1][0]
                long=location[1][1]
                df['Latitude'][i+131]=lat
                df['Longitude'][i+131]=long
     
    return df

def data_cleaning():
    India_data=pd.read_csv('india-districts-census-2011.csv')
    UP_data=India_data[India_data['State name']== 'UTTAR PRADESH']
    UP_data.describe()
    column_names=UP_data.columns.tolist()
    UP_data=geo_code(UP_data)
    eLat=UP_data.Latitude.isna().sum()
    eLong=UP_data.Longitude.isna().sum()
    #Shrawasti,Siddharthnagar,Sant Ravidas Nagar (Bhadohi), Kanshiram Nagar
    
    UP_data.loc[UP_data['District name'] == "Shrawasti", "Latitude"] = 27.5978
    UP_data.loc[UP_data['District name'] == "Shrawasti", "Longitude"]=81.9535
    
    UP_data.loc[UP_data['District name'] == "Siddharthnagar", "Latitude"] = 27.2716
    UP_data.loc[UP_data['District name'] == "Siddharthnagar", "Longitude"]=82.8210
   #° N, ° E
    UP_data.loc[UP_data['District name'] == "Sant Ravidas Nagar (Bhadohi)", "Latitude"] = 25.3264
    UP_data.loc[UP_data['District name'] == "Sant Ravidas Nagar (Bhadohi)", "Longitude"]=82.4319
    
    UP_data.loc[UP_data['District name'] == "Kanshiram Nagar", "Latitude"] = 27.7952
    UP_data.loc[UP_data['District name'] == "Kanshiram Nagar", "Longitude"]=78.7930
    return UP_data

def Potential_locations(UP_data):
    #since the area of interest is smaller we assume that Eucledian distance is 
    #equivalent to Geodesic distance (or GEographical-Distance)
    d=UP_data[['Latitude','Longitude','District name']]
    #d=pd.DataFrame([UP_data["Latitude"],UP_data["Longitude"]],index=UP_data['District name'])
    d_kmeans = d.set_index('District name')
    flag=0
    noc=1
    while(flag==0):
     
        kmeans=KMeans(n_clusters=noc,max_iter=50)  
        kmeans.fit(d_kmeans)
        #ssd=[]
        #ssd.append(kmeans.inertia_)    
        cluster_centroid=kmeans.cluster_centers_
        labels=kmeans.labels_
        p=kmeans.predict(d_kmeans)
        p=np.array([p])
        p=p.T
        d_kmeans['clusters']=p
        fit=evaluate_clusters(d_kmeans,noc,labels,cluster_centroid)
        if (fit==True):
            flag=1
        else:
            flag=0
            noc=noc+1
# def evaluate_clusters():
    
    
#     if 
    
    return cluster_centroid,d_kmeans

def evaluate_clusters(d_kmeans,noc,lbl,cll):
    
    
    for i in range(0,noc):
        clust_eval=d_kmeans[d_kmeans['clusters']==i]
        clust_lat_long=cll[i]
        clust_lat_long=np.array([clust_lat_long])
        clust_lat_long=clust_lat_long[:,0:2]
        
        latlong=clust_eval[['Latitude','Longitude']].to_numpy()
        dl=distance_matrix(latlong,clust_lat_long,2)
        dl=np.multiply(dl,111)
        s=sum(dl>100)
        if (s>=1):
            print(noc)
            return False
        else:
            pass
    return True
    
    



UP_data=data_cleaning()
ccll,d_kmeans=Potential_locations(UP_data)



plt.scatter(d_kmeans['Longitude'], d_kmeans['Latitude'],c=d_kmeans['clusters'])  
plt.scatter(ccll[:,1], ccll[:,0],c='black')
plt.show() 