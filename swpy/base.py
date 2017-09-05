'''
Created on 2017. 4. 5.

@author: jongyeob
'''

import os
import logging
from datetime import datetime,timedelta
from collections import deque
from cStringIO  import StringIO
from . import utils2 as swut

LOG = logging.getLogger(__name__)

class TimeFormattedPath():
    def __init__(self,time_format,header={}):
        self.format = time_format.format(**header)
         
    def get(self,time):
        time_in = swut.time_parse(time)
        path = time_in.strftime(self.format)
        return path
    
class PathRequest():
    def __init__(self,path,cache_size=10,margin=0):
        self.path  = path
        self._margin = margin
        self._cache = {}
        self._cache_size = cache_size
        self._cache_index = []
        
    def request(self,time):
        raise NotImplemented
            
    def get(self,time):
        
        time_in  = swut.time_parse(time)
        dir_format,file_format = os.path.split(self.path.format)
        dir_path,file_name = os.path.split(self.path.get(time_in))
        
        dir_time = swut.parse_string(dir_format,dir_path)
        
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
            return self.path.get(best_time)
                        
class FilePathRequest(PathRequest):
    def request(self,time):
        
        input_time = swut.time_parse(time)
        
        path = self.path.get(input_time)
        dir_path, file_name = os.path.split(path)
        dir_format, file_format = os.path.split(self.path.format)
                    
        files = swut.get_files(dir_path + '/*')
        file_time_list = []
        for f in files:
            sub_dir,file_name = os.path.split(f)
            try:
                file_time = datetime.strptime(file_name,file_format)
                file_time_list.append(file_time)
            except:
                pass
            
        file_time_list.sort()
        
        return file_time_list
    
class UrlPathRequest(PathRequest):
    def request(self,time):
        
        input_time = swut.time_parse(time)
    
        path = self.path.get(input_time)
        dir_path, file_name = os.path.split(path)
        dir_format, file_format = os.path.split(self.path.format)
        
        buf = StringIO()

        swut.download_by_url(dir_path, buf)
        file_time_list = []   
        
        contents = buf.getvalue()
        buf.close()
                
        start_index = 0
        end_index = 0
        
        while True:
            start_index = contents.find("<a href=\"", end_index)
            start_index += 9
            if (start_index == -1 or start_index < end_index):
                break
            
            end_index = contents.find("\"", start_index)
            if (end_index == -1):
                break
            
            url_path = contents[start_index:end_index]
            sub_dir,file_name = os.path.split(url_path)
            
            try:
                file_time = datetime.strptime(file_name,file_format)
                file_time_list.append(file_time)
            except:
                pass
            
        file_time_list.sort()
        
        return file_time_list
    
class DataUnit():
    def __init__(self,header={},data=[]):
        self.header = header
        self.data = data