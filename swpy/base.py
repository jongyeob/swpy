'''
Created on 2017. 4. 5.

@author: jongyeob
'''

import logging

LOG = logging.getLogger(__name__)


class DataUnit():
    def __init__(self,header={},body=[]):
        self.header = header
        self.body = body
        
        
class PathUnit():
    def __init__(self,style,substr={},*args,**kwargs):
        self.style = style.format(**substr)
        
    def get(self,substr={},*args,**kwargs):
        path_string = self.stlye.format(**substr)
        
        return path_string
    
    def get_style(self):
        return self.style
    
class TimeUnit():
    def __init__(self,*args,**kwargs):
        self.t1 = None
        self.t2   = None
        self.td = 0    # Seconds 

class PlotUnit():
    def draw(self,data):
        raise NotImplementedError()
    def save(self,path,data):
        raise NotImplementedError()