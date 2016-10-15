'''
Created on 2015. 7. 29.

@author: jongyeob
'''

import logging
import os
from swpy import utils
from swpy.sdo import jsoc_aia_jp2 as jp2
from swpy.utils import datetime as dt
import pytest

logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

test_starttime = '20121003'
test_endtime   = '20121005'
test_cadence   = 6*3600

def test_make_url():
    for wave in jp2.WAVELENGTHS:
        for time in dt.iseries(test_starttime,test_endtime,days=1):
            url = jp2.make_url(wave, time)
            print url
        
@pytest.mark.online
def test_request():
    for wave in jp2.WAVELENGTHS:
        jp2.request(wave,test_starttime,end=test_endtime)

@pytest.mark.online
def test_download():
    for wave in jp2.WAVELENGTHS:
        jp2.download(wave,test_starttime, end=test_endtime, cadence=test_cadence)
    
