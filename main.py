# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:07:15 2020

@author: rolly
"""

import pandas

df = pandas.read_excel('VA SPP Genap 2019-2020.xlsx', sheet_name='va excel')

df = df.dropna(how='all')
thr=int(len(df)*0.8)
df = df.dropna(thresh=thr, axis=1)

# In[]
new_header =df.iloc[0]
df = df[1:]
df.columns = new_header