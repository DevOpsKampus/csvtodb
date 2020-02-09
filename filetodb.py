# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 06:36:46 2020

@author: rolly
"""
import pandas
from validate_email import validate_email

class Filetodb(object):
    def openExcel(self,filename):
        df = pandas.read_excel(filename, sheet_name=0)
        return df
        
    def cleanEmptyCell(self,df):
        thr=int(df.shape[0]*0.5)
        thc=int(df.shape[1]*0.5)
        df = df.dropna(thresh=thc)
        df = df.dropna(thresh=thr, axis=1)
        return df
        
    def setHeaderfromRow(self,df):
        new_header =df.iloc[0]
        df = df[1:]
        df.columns = new_header
        df.reset_index(inplace = True, drop = True)
        return df
    
    def fixEmail(self,df,emailcolumn):
        df[emailcolumn] = df[emailcolumn].str.replace(" ","")
        df[emailcolumn] = df[emailcolumn].str.replace("'","")
        df[emailcolumn] = df[emailcolumn].str.replace('"','')
        df[emailcolumn] = df[emailcolumn].str.replace(';','')
        df[emailcolumn] = df[emailcolumn].str.replace(':','')
        #mencari at atau merubah yang ada jadi at
        df[emailcolumn] = df[emailcolumn].str.replace("!","@")
        df[emailcolumn] = df[emailcolumn].str.replace("#","@")
        df[emailcolumn] = df[emailcolumn].str.replace("$","@")
        df[emailcolumn] = df[emailcolumn].str.replace("%","@")
        df[emailcolumn] = df[emailcolumn].str.replace("^","@")
        df[emailcolumn] = df[emailcolumn].str.replace("&","@")
        df[emailcolumn] = df[emailcolumn].str.replace("*","@")
        #merubah koma menjadi titik
        df[emailcolumn] = df[emailcolumn].str.replace(",",".")
        return df
    
    def fixEmailnoAt(self,df,emailcolumn):
        df[emailcolumn] = df[emailcolumn].apply(lambda x:self.fixEmailProvider(x))
        return df
    
    def fixEmailProvider(self,email):
        emailproviders=['gmail.com','yahoo.com','yahoo.co.id','yahoo.co.uk','poltekpos.ac.id','stimlog.ac.id']
        for emailprovider in emailproviders:
            usern=email.split(emailprovider)
            if len(usern)>1:
                useremail=usern[0][:-1]+'@'+emailprovider
        return useremail
        
    def cekEmailValid(self,df,emailcolumn):
        df['is_valid_email'] = df[emailcolumn].apply(lambda x:validate_email(x))
        return df
        
    def getInvalidEmail(self,df,emailcolumn):
        crot=df[df['is_valid_email'].eq(False)]
        return crot
    
    def joinDatetime(self,df,datecolumn,timecolumn):
        df['expired_date'] = pandas.to_datetime(df[datecolumn].dt.strftime('%Y-%m-%d')+ ' ' +df[timecolumn])
        return df