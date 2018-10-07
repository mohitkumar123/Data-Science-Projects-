# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 21:54:39 2018

@author: zjpla
"""
import pandas as pd 
df=pd.read_excel("Category5.xlsx")
for i in range(len(df)):
    df.loc[i, "wind speeds"]=int(df.loc[i, "wind speeds"][-9:-6])
    df.loc[i, "Pressure"]=int(df.loc[i, "Pressure"][:3])
df.rename(columns={"wind speeds":"wind speeds(km/h)", "Pressure": "Pressure(hPa)"}, inplace=True)
df.to_excel("Cat5.xlsx")