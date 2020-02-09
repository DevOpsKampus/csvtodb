# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:07:15 2020

@author: rolly
"""
import filetodb

fd = filetodb.Filetodb()

df = fd.openExcel('VA SPP Genap 2019-2020.xlsx')
df = fd.cleanEmptyCell(df)
df = fd.setHeaderfromRow(df)
df = fd.joinDatetime(df,'expired_date','expired_time')

df = fd.fixEmail(df,'customer_email')
df = fd.cekEmailValid(df, 'customer_email')
emailnovalid = fd.getInvalidEmail(df,'customer_email')


# In[]

crot=df[df['is_valid_email'].eq(False)]

df.loc[df['is_valid_email'] == False, 'customer_email'] = 10
#pake index
df.at[0,'customer_email']= 20
#
# In[]
email = fd.fixEmailnoAt(emailnovalid,'customer_email')