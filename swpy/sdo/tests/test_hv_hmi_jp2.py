'''
Created on 2015. 4. 26.

@author: jongyeob
'''

import logging
import os
from swpy import utils
from swpy.sdo import hv_hmi_jp2 as hv
from swpy.utils import datetime as dt
import pytest


logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

test_starttime = '20121003'
test_endtime   = '20121005'
test_cadence   = 6*3600

def test_make_url():
    for type in hv.TYPES:
        for time in dt.iseries(test_starttime,test_endtime,days=1):
            url = hv.make_url(type, time)
            print url
        
@pytest.mark.online
def test_request():
    for type in hv.TYPES:
        hv.request(type,test_starttime,end=test_endtime)

@pytest.mark.online
def test_download():
    for type in hv.TYPES:
        hv.download(type,test_starttime, end=test_endtime, cadence=test_cadence)
    
