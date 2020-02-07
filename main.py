# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:07:15 2020

@author: rolly
"""

import csvtodb

cd = csvtodb.Csvtodb()

df = cd.openExcel('VA SPP Genap 2019-2020.xlsx')
df = cd.cleanEmptyCell(df)
df = cd.setHeaderfromrow(df)