'''
Created on 2017. 12. 22.

@author: jongyeob
'''
import os

from swpy import utils2 as swut
from timepath import TimeFormat


class RequestUnit():
    def __init__(self,path,cache_size=10,margin=0):
        self.path  = TimeFormat(path)
        self._margin = margin
        self._cache = {}
        self._cache_size = cache_size
        self._cache_index = []
        
    def request(self,time):
        raise NotImplemented
            
    def search(self,time):
        
        time_in  = swut.time_parse(time)
        path_format = self.path.get_style()
        
        dir_format,file_format = os.path.split(path_format)
        dir_path = time_in.strftime(dir_format)
        
        dir_time = swut.time_string(dir_format,dir_path)
        
        request_time = [] 
        
        try:
            request_time = self._cache[dir_time]
            self._cache_index.remove(dir_time)
            self._cache_index.append(dir_time)
        except KeyError:
            request_time = self.request(time_in)
            self._cache[dir_time] = request_time
            self._cache_index.append(dir_time)
        finally:
            if len(self._cache_index) > self._cache_size:
                delete_time = self._cache_index.pop(0)
                self._cache.pop(delete_time)
        
        if not request_time:
            return
        
        diff_time = [abs((rt-time_in).total_seconds()) for rt in request_time]
        zip_diff_time = zip(diff_time,request_time)
        zip_diff_time.sort()
        min_diff,best_time = zip_diff_time[0]
        
        if min_diff <= (self._margin/2.):
            return best_time
        
        