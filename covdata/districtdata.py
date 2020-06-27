# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:38:06 2020

@author: Dripta
"""

import urllib
import json
import warnings
import pandas as pd
from datetime import datetime



warnings.filterwarnings("ignore")


class districtwiseData():
    def __init__(self):
        url='https://api.covid19india.org/districts_daily.json'
        json_url = urllib.request.urlopen(url)
        data=json.loads(json_url.read())
        self.district_data=data['districtsDaily']
        self.district_dict_={}
        for state in self.district_data.keys():
            self.district_dict_[f'{state}']=list(self.district_data[state].keys())
            '''if 'Unknown' in self.district_dict_[f'{state}']:
                self.district_dict_[f'{state}']=self.district_dict_[f'{state}'].remove('Unknown')'''
            
    def districtDate(self,district,date='All'):
        word_list=district.split(" ")
        if 'and' in word_list:
            for i,j in enumerate(word_list):
                if j != 'and':
                    word_list[i]=j.title()
            district=" ".join(word_list)   
        else:
            district=district.title()
        flag=0
        if date == 'All':
            for key in self.district_data.keys():
                for dis_name in self.district_data[key].keys():
                    if dis_name==district:
                        dis_df=pd.DataFrame(self.district_data[key][dis_name]).drop(columns=['notes'])
                        flag=1
        else:
            newdate=datetime.strftime(datetime.strptime(date,'%d/%m/%Y'),'%Y-%m-%d')
            for key in self.district_data.keys():
                for dis_name in self.district_data[key].keys():
                    if dis_name==district:
                        dis_df=pd.DataFrame(self.district_data[key][dis_name]).drop(columns=['notes'])
                        dis_df=dis_df[dis_df['date']==newdate]
                        if dis_df.empty != True:
                            flag=1
        if flag ==1:
            return dis_df
        else:
            raise Exception(f'No data found for {district} for {date}')
        