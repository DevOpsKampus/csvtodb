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

if len(invalidemails) == 0 and len(unregisteredemail) == 0:
    print('email valid semua')

if len(unregisteredphone) > 0:
    print("telepon tidak valid:")
    print(unregisteredphone)
# In[]
    
from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@127.0.0.1/{db}"
                       .format(user="root",
                               pw="rollyganteng",
                               db="va"))

# In[]

df=df.rename(columns={"prodi ": "Prodi_ID", "jenjang": "Jenjang_ID"})
# In[]

df.to_sql('upload', con = engine, if_exists = 'append', chunksize = 1000)


    
# In[]

import pymysql


# Connect to the database
connection = pymysql.connect(host='localhost',
                         user='root',
                         password='rollyganteng',
                         db='va')


# create cursor
cursor=connection.cursor()

# creating column list for insertion
cols = 'upload_id`,`client_id`,`trx_id`,`virtual_account`,`customer_name`,`customer_email`,`customer_phone`,`trx_amount`,`expired_date`,`expired_time`,`description`,`status`,`approval`,`prodi`,`jenjang'

# Insert DataFrame recrds one by one.
for i,row in df.iterrows():
    sql = "INSERT INTO `book_details` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))

    # the connection is not autocommitted by default, so we must commit to save our changes
    connection.commit()