'''
Created on 2017. 12. 21.

@author: jongyeob
'''
from . import base as swbs

from . import utils2 as utils


class Time(swbs.TimeUnit):
    def __init__(self,t1,t2=None,step=0):
        self.t1  = utils.time_parse(t1)
        
        self.t2  = None
        if t2:
            self.t2 = utils.time_parse(t2)
        
        self.td  = 0
        if step:
            self.td = step
        
    def get_start(self):
        
        return self.t1

    def get_end(self):
        
        return self.t2
    
    def get_delta(self):
        
        return utils.timedelta(seconds=self.td)

class TimeFormat(swbs.PathUnit):
    def __init__(self,style,substr={}):
        self.style = style.format(**substr)
         
    def get(self,time,substr={}):
        
        style_string = self.style.format(**substr)
        
        time_in = utils.time_parse(time)
        time_string = time_in.strftime(style_string)
        
        return time_string
    
    def get_style(self):
        return self.style
