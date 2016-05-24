'''
Created on 2016. 5. 11.

@author: jongyeob
'''
import logging
from collections import deque
from swpy.utils import datetime as swdt
from swpy.utils import filepath as swfp
from urllib import urlretrieve


LOG = logging.getLogger(__name__)

class ClientBase():
    pass

class TimedCache():
    def __init__(self,size=100):
        self.datalist = deque(maxlen=size)
        
    def request(self,time,margin=0):
        
        input_time  = swdt.parse(time)
        
        tx = self.datalist
        if not tx:
            return None
    
        diff_t = [abs((ty[0]-input_time).total_seconds()) for ty in tx]
        dtx = zip(diff_t,tx)
        dtx.sort()
        min_diff,best_tx = dtx[0]
        
        if min_diff <= margin:
            return best_tx
        
    def update(self,datalist):
        self.datalist.extend(datalist)
        

                
class TimedClientBase(ClientBase):
    def __init__(self,format):
        self.format = format
        
    def get_url(self,time=''):
        if not time:
            return self.format
        
        return swdt.replace(self.format,time)
    
    def request(self,time):
        ti = swdt.parse(time)
        path = self.get_url(ti)
        
        return (ti,path)
                

class LocalTimedClient(TimedClientBase):
    def __init__(self,format,margin=0,cache_size=100):
        TimedClientBase.__init__(self, format)
        self.cache  = TimedCache(size=cache_size)
        self.margin = margin

    def request(self,time,margin=None):
        
        input_margin = self.margin
        if margin is not None:
            input_margin = margin
                
        ret = self.cache.request(time,margin=input_margin)
        if ret:  return ret
                
        format = self.get_url()
        tdel  = swdt.timedelta(seconds=margin/2)
        res = swfp.request_files(format,time,time+tdel)
        
        if not res: return None          
        self.cache.update(res)
        
        return res[0]