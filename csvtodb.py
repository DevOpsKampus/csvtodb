# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 06:36:46 2020

@author: rolly
"""
import pandas

class Csvtodb(object):
    def openExcel(self,filename):
        df = pandas.read_excel(filename, sheet_name=0)
        return df
        
    def cleanEmptyCell(self,df):
        thr=int(df.shape[0]*0.5)
        thc=int(df.shape[1]*0.5)
        df = df.dropna(thresh=thc)
        df = df.dropna(thresh=thr, axis=1)
        return df
        
    def setHeaderfromrow(self,df):
        new_header =df.iloc[0]
        df = df[1:]
        df.columns = new_header
        return df