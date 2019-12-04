# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:37:49 2019

@author: Ryan
"""


import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

def ScrapeWebsite():
    ''' List to hold scraped Data '''

    data = []
    
    ''' Lotto Years to get Results '''
    lstofyears = ['1982-1983','1984-1985','1986-1987','1988-1989','1990-1991',\
                  '1992-1993','1994-1995','1996-1997','1998-1999','2000-2001',\
                  '2002-2003','2004-2005','2006-2007','2008-2009','2010-2011',\
                  '2012-2013','2014-2015']

    for i in range(len(lstofyears)):
        list_num = []
        
        url = "http://www.lotto649stats.com/winning-numbers-" + lstofyears[i] + ".html" #URL of website to scrape
        content = urllib.request.urlopen(url).read() #reads the content of the website
        soup = BeautifulSoup(content,"html.parser") #Parses it using html
        
        for j in soup.find_all('tr'):
            for k in j.find_all('td'):
                num = k.get_text()
                list_num.append(num.strip())
                
        preprocess = []
        for elems in list_num[9:]:
            if 'Numbers' not in elems and 'Date' not in elems and 'Bonus' not in elems and 'Jackpot' not in elems:
                preprocess.append(elems)
            
        data.append(preprocess)

    return data

def RestructureData(data):
    
    initPD = {'Date':[],
        'Winning Number1':[],
        'Winning Number2':[],
        'Winning Number3':[],
        'Winning Number4':[],
        'Winning Number5':[],
        'Winning Number6':[],
        'Bonus': []}
    
    PD_dataframe = pd.DataFrame(initPD)
    
    for i in range(len(data)):
        tempdata = data[i]
        index = 0
        
        while index < len(tempdata):
            tempPD_df = {'Date': [tempdata[index]],\
                         'Winning Number1': [tempdata[index+1]],\
                         'Winning Number2': [tempdata[index+2]],\
                         'Winning Number3': [tempdata[index+3]],\
                         'Winning Number4': [tempdata[index+4]],\
                         'Winning Number5': [tempdata[index+5]],\
                         'Winning Number6': [tempdata[index+6]],\
                         'Bonus': [tempdata[index+7]]}
            PD_dataframe = PD_dataframe.append(pd.DataFrame(tempPD_df),ignore_index=True)
            index += 8
            
    PD_dataframe.drop_duplicates(subset ="Date",inplace=True) 
            
    return PD_dataframe

if __name__ == "__main__":
    Data = ScrapeWebsite()
    PD_dataframe = RestructureData(Data)