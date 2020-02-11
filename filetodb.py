# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 06:36:46 2020

@author: rolly
"""
import pandas
from validate_email import validate_email

class Filetodb(object):
    def __init__(self):
        self.unregemail=[]
        self.unregphone=[]
        
    def getCSVSeparator(self,filename):
        with open(filename) as f:
        	line = f.readline()
        separators=[',',';','|']
        for sep in separators:
            if line.find(sep) > 1:
                separator = sep
                break
        return separator

    def openFile(self,filename):
        try:
            df = pandas.read_excel(filename, sheet_name=0)
        except:
            #separator detection
            sep=self.getCSVSeparator(filename)
            df = pandas.read_csv(filename,sep=sep)
        return df
        
    def cleanEmptyCell(self,df):
        thr=int(df.shape[0]*0.5)
        thc=int(df.shape[1]*0.5)
        df = df.dropna(thresh=thc)
        df = df.dropna(thresh=thr, axis=1)
        return df
        
    def checkSetHeader(self,df,firstcolumnname):
        if df.columns[0] != firstcolumnname:
            df = self.setHeaderfromFirstRow(df)
        return df
    
    def setHeaderfromFirstRow(self,df):
        new_header =df.iloc[0]
        df = df[1:]
        df.columns = new_header
        df.reset_index(inplace = True, drop = True)
        return df
    
    def dropSpCharIn(self,df,columnname):
        #hapus tanda kutip spasi dan titik dua
        df[columnname] = df[columnname].str.replace(" ","")
        df[columnname] = df[columnname].str.replace("'","")
        df[columnname] = df[columnname].str.replace('"','')
        df[columnname] = df[columnname].str.replace(';','')
        df[columnname] = df[columnname].str.replace(':','')
        #hapus karakter khusus yang tidak lazim di alamat email
        df[columnname] = df[columnname].str.replace("!","")
        df[columnname] = df[columnname].str.replace("#","")
        df[columnname] = df[columnname].str.replace("$","")
        df[columnname] = df[columnname].str.replace("%","")
        df[columnname] = df[columnname].str.replace("^","")
        df[columnname] = df[columnname].str.replace("&","")
        df[columnname] = df[columnname].str.replace("*","")
        df[columnname] = df[columnname].str.replace("[","")
        df[columnname] = df[columnname].str.replace("]","")
        df[columnname] = df[columnname].str.replace("{","")
        df[columnname] = df[columnname].str.replace("}","")
        df[columnname] = df[columnname].str.replace("+","")
        df[columnname] = df[columnname].str.replace("=","")
        df[columnname] = df[columnname].str.replace("|","")
        df[columnname] = df[columnname].str.replace("\\","")
        df[columnname] = df[columnname].str.replace("(","")
        df[columnname] = df[columnname].str.replace(")","")
        df[columnname] = df[columnname].str.replace("`","")
        df[columnname] = df[columnname].str.replace("~","")
        df[columnname] = df[columnname].str.replace("<","")
        df[columnname] = df[columnname].str.replace(">","")
        df[columnname] = df[columnname].str.replace("?","")
        df[columnname] = df[columnname].str.replace("/","")
        #utf-8 char
        df[columnname] = df[columnname].str.replace("\u202d","")
        return df
        
    def fixPhoneNumber(self,df,phonecolumn):
        df=self.dropSpCharIn(df,phonecolumn)
        df[phonecolumn] = df[phonecolumn].apply(lambda x:self.fixPhoneProvider(x))
        return df
    
    def fixPhoneProvider(self,phonedata):
        phonedata=str(phonedata)
        if phonedata[:2] == '08':
            phone='62'+phonedata[1:]
        elif phonedata[:1] == '8':
            phone='62'+phonedata
        elif phonedata[:4] == '0966':
            phone=phonedata[1:]
        else:
            phone=phonedata
            self.unregphone.append(phonedata)
        return phone
    
    def getUnregPhones(self):
        return self.unregphone
        
    def fixEmail(self,df,emailcolumn):
        df=self.dropSpCharIn(df,emailcolumn)
        #merubah koma menjadi titik
        df[emailcolumn] = df[emailcolumn].str.replace(",",".")
        #pengecekan satu persatu
        df[emailcolumn] = df[emailcolumn].apply(lambda x:self.fixEmailProvider(x))
        return df
    
    def fixEmailProvider(self,email):
        email=email.lower()
        emailproviders=['gmail.com','yahoo.com','posindonesia.co.id','ymail.com',
                        'poltekpos.ac.id','stimlog.ac.id','ftmd.itb.ac.id',
                        'hotmail.com','semenindonesia.com','icloud.com',
                        'bukitasam.co.id','poltekkespalembang.ac.id','bps.go.id',
                        'hrs-indonesia.co.id','sucofindo.co.id','geosistem.co.id',
                        'yahoo.co.id','ykk.co.id','antam.com','rocketmail.com',
                        'bapeten.go.id','airasia.com','moriroku.co.id','cgglobal.com',
                        'jssbdo.com','telpp.com','engineer.com'
                        ]
        for emailprovider in emailproviders:#identify provider with no at or wrong at position
            usern=email.split(emailprovider)
            if len(usern) == 2:#if found the provider
                if len(usern[0].split('@')) > 1 :#check if double at symbol in string
                    useremail=usern[0].replace('@','')+'@'+emailprovider
                else :
                    useremail=usern[0][:-1]+'@'+emailprovider
                break
        if 'useremail' not in locals():#unregistered provider or typo provider
            typo_email=email.split('@')
            if len(typo_email) == 2: #normal at only one
                if len(typo_email[1]) == 9:
                    typo_email[1]=typo_email[1].replace('gamil.com','gmail.com')
                    typo_email[1]=typo_email[1].replace('gmali.com','gmail.com')
                    typo_email[1]=typo_email[1].replace('gmail.con','gmail.com')
                    typo_email[1]=typo_email[1].replace('gmail.vom','gmail.com')
                    useremail=typo_email[0]+'@'+typo_email[1]
                elif len(typo_email[1]) == 8:
                    typo_email[1]=typo_email[1].replace('gmailcom','gmail.com')
                    typo_email[1]=typo_email[1].replace('gmai.com','gmail.com')
                    useremail=typo_email[0]+'@'+typo_email[1]
                elif len(typo_email[1]) == 5:
                    typo_email[1]=typo_email[1].replace('gmail','gmail.com')
                    typo_email[1]=typo_email[1].replace('gamil','gmail.com')
                    typo_email[1]=typo_email[1].replace('gmali','gmail.com')
                    useremail=typo_email[0]+'@'+typo_email[1]
                elif len(typo_email[1]) == 4:
                    typo_email[1]=typo_email[1].replace('gmai','gmail.com')
                    typo_email[1]=typo_email[1].replace('gmil','gmail.com')
                    useremail=typo_email[0]+'@'+typo_email[1]
                else:
                    useremail=email
                    self.unregemail.append(email)
            else:#abnormal at, no at or more than one
                useremail=email
                self.unregemail.append(email)
        return useremail
        
    def getUnregEmails(self):
        return self.unregemail
    
    def cekEmailValid(self,df,emailcolumn):
        df['is_valid_email'] = df[emailcolumn].apply(lambda x:validate_email(x))
        return df
        
    def getInvalidEmails(self,df,emailcolumn):
        crot=df[df['is_valid_email'].eq(False)]
        return crot
    
    def joinDatetime(self,df,datecolumn,timecolumn):
        try:
            df[datecolumn] = pandas.to_datetime(df[datecolumn].dt.strftime('%Y-%m-%d')+ ' ' +df[timecolumn])
        except:
            df[datecolumn] = pandas.to_datetime(df[datecolumn]+ ' ' +df[timecolumn])
        return df