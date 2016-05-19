'''
Created on 2015. 7. 29.

@author: jongyeob
'''

import os
import logging
import swpy
from swpy.utils import datetime as swdt
from swpy import utils
from swpy import nobeyama as swnb
from pandas import tseries
    
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

swnb.LOCAL_URL = swpy.SWPY_ROOT + "/res/test/data/ICCON/NOBEYAMA/NoRH/%Y/%Y%m%d/%Y%m%d_%H%M%S_NoRH.fits"
norh10 = swnb.NoRH10minClient()
norh10r= swnb.RemoteNoRH10minClient()


print norh10.get_url()
print norh10r.get_url()

print norh10.get_url("2010-10-31 00:02:00.101")
print norh10r.get_url("2010-10-31 00:02:00.101")

print norh10.get_url("20150101_000000")
print norh10r.get_url("20150101_000000")


tseries = swdt.series("20150101_000000", "20150101_030000", hours=1)
files = map(norh10.request,tseries)
print files


tseries = swdt.series("20150101_000000", "20150101_090000", hours=1)
files = map(norh10r.request,tseries)
print files

