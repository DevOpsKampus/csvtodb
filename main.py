# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:07:15 2020

@author: rolly
"""
import filetodb

fd = filetodb.Filetodb()

df = fd.openFile('VA SPP Genap 2019-2020.xlsx')
df = fd.cleanEmptyCell(df)
df = fd.checkSetHeader(df,'upload_id')
df = fd.joinDatetime(df,'expired_date','expired_time')

df = fd.fixEmail(df,'customer_email')
df = fd.cekEmailValid(df, 'customer_email')
df = fd.fixPhoneNumber(df,'customer_phone')
invalidemails = fd.getInvalidEmails(df,'customer_email')
unregisteredemail = fd.getUnregEmails()
unregisteredphone = fd.getUnregPhones()

if len(invalidemails) == 0 and len(unregisteredemail) == 0 and len(unregisteredphone) == 0:
    fd.toDB(df)
    print('ok')
else:
   print('{ "invalid_phones" :')
   print(unregisteredphone)
   print(',')
   print(' "invalid_emails" :')
   print(unregisteredemail)
   print('}')
   
# In[]
 