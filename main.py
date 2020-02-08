# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:07:15 2020

@author: rolly
"""
import pandas as pd
import csvtodb

cd = csvtodb.Csvtodb()

df = cd.openExcel('VA SPP Genap 2019-2020.xlsx')
df = cd.cleanEmptyCell(df)
df = cd.setHeaderfromrow(df)

df = cd.emailValidation(df,'customer_email')

df = cd.joinDatetime(df,'expired_date','expired_time')
# In[]
df.reset_index(inplace = True, drop = True)
# In[]
df['expired_date'] = df['expired_date'].dt.strftime('%Y-%m-%d')+ ' ' +df['expired_time']


# In[]
#df['expired_date'] = df['expired_date'].str.replace("00:00:00",df['expired_time'])
df['expired_date'] = pd.to_datetime(df['expired_date'])
df['expired_time'] = pd.to_datetime(df['expired_time'])
# In[]
df['expired_time'] = pd.Timestamp.combine(df['expired_date'],df['expired_time'])
#df['expired_date'] = df['expired_date']+df['expired_time']