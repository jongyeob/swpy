'''
Created on 2015. 4. 26.

@author: jongyeob
'''

import os
import logging
from swpy.utils import date_time as dt
from swpy import utils
from swpy.sdo.hmi_nasa import *
    
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

     
print get_path('Ic', "2010-10-31 00:02:00.101")
print get_path('Ic', "2010-10-31 00:02:00.10")
print len(request("20121003",'Ic',end_datetime="20121005"))
print len(request("20121003",'Ic',end_datetime="20121005",cadence=90))
