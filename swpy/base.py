'''
Created on 2017. 4. 5.

@author: jongyeob
'''

import os
import logging
from datetime import datetime

from swpy import utils2 as swut

LOG = logging.getLogger(__name__)


class DataUnit():
    def __init__(self,header={},body=[]):
        self.header = header
        self.body = body
        
class FitsData(DataUnit): pass
        
class PathUnit():
    def __init__(self,path,*args,**kwargs):
        self.path = path
    def get(self,*args,**kwargs):
        return self.path
    
class TimeUnit():
    def __init__(self,*args,**kwargs):
        self.t1 = None
        self.t2   = None
        self.td = 0    # Seconds 
