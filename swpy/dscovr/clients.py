'''
Created on 2016. 10. 15.

@author: jongyeob
'''

from __future__ import absolute_import


import json
from  datetime import datetime
import logging

from swpy.utils2 import date_time as swdt
from swpy.utils2 import TableIO
LOG= logging.getLogger('discovr')


DATASERIES = [
'mag-1-day',
'mag-2-hour',
'mag-3-day',
'mag-5-minute',
'mag-6-hour',
'mag-7-day',
'plasma-1-day',
'plasma-2-hour',
'plasma-3-day',
'plasma-5-minute',
'plasma-6-hour',
'plasma-7-day']

MAG_KEY = ["time_tag","bx_gsm","by_gsm","bz_gsm","lon_gsm","lat_gsm","bt"]
MAG_STYLE =["<24","<10","<10","<10","<10","<10","<10"]
PLASMA_KEY = ["time_tag","density","speed","temperature"]
PLASMA_STYLE = ["<24","<12","<12","<12"]

URL_PATTERN = 'http://services.swpc.noaa.gov/products/solar-wind/{data_series}.json'
PATH_PATTERN = '/discovr/{data_series}/%Y/%Y%m/{data_series}_%Y%m%d.txt'


class DscovrRTClient():
    def __init__(self,data_series):
        self.data_series = data_series
               
    def get(self,time):
        url = URL_PATTERN.format(data_series=self.data_series)
        return url
    
    def load(self,file):

        decoded = json.load(file)
        
        keywords = decoded[0]
        data_cols = zip(*decoded[1:])
        
        
        return dict(zip(keywords,data_cols))
    
class DscovrClient():
    def __init__(self,data_series):
        self.data_series = data_series
        
        self.key = []
        self.style = []
        if self.data_series.startswith('mag'):
            self.key = MAG_KEY
            self.style = MAG_STYLE
            
        if self.data_series.startswith('plasma'):
            self.key = PLASMA_KEY
            self.style = PLASMA_STYLE
            
        self.table = TableIO(self.style)
        
        
    def get(self,time):
        
        parsed_time = swdt.parse(time)
        path = PATH_PATTERN.format(data_series=self.data_series)
        path = datetime.strftime(parsed_time,path)
        
        return path
    
    def load(self,file):
        
        read_data = self.table.read(file, self.key)
        
        return read_data
    
    def save(self,file,data):
        
        
        self.table.write(file, data,key=self.key)

        return 0

    


    
    