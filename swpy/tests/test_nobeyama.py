'''
Created on 2015. 7. 29.

@author: jongyeob
'''

import os
import logging
from swpy.utils import datetime as dt
from swpy import utils
from swpy import nobeyama as nb
    
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

     
print nb.get_path("2010-10-31 00:02:00.101")
files = nb.download("20150101_000000",end="20150101_010000",cadence=600,download=False)
nb.download("20150101_000000",end="20150101_010000",cadence=600)
files = nb.request("20150101_000000",end="20150101_010000")
print "Found ",len(files)
files = nb.request("20150101_000000",end="20150101_010000",cadence=600)
print "Found ",len(files)
