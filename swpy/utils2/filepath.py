'''
Created on 2016. 10. 20.

@author: jongyeob
'''
import os
import glob
import logging
from cStringIO  import StringIO
from datetime import datetime

import date_time as swdt
import download  as swdl
import base as swbs


LOG = logging.getLogger(__name__)


def mkdirs(pathstr):
    pathstr = os.path.normpath(pathstr+'/')
    if os.path.exists(pathstr) == False:
        os.makedirs(pathstr)

def mkpath(pathstr):    
    pathstr = os.path.normpath(pathstr)
    dirpath,filename = os.path.split(pathstr)

    if len(dirpath) > 0 and os.path.exists(dirpath) == False:
        os.makedirs(dirpath)
        
    return pathstr

def get_files(path_exp):
    # path_exp : expression of path
    arg_path = os.path.split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(dirname+'/'+ arg_path[1]):
            filepath = filepath.replace('\\','/')
            file_list.append(filepath)
        
    return file_list


class TimeFormatPath(swbs.PathUnit):
    def __init__(self,time_format,header={}):
        self.format = time_format.format(**header)
         
    def get(self,time,header={}):
        
        format_string = self.format.format(**header)
        
        time_in = swdt.parse(time)
        path = time_in.strftime(format_string)
        
        return path

    
class PathRequestUnit():
    def __init__(self,path,cache_size=10,margin=0):
        self.path  = path
        self._margin = margin
        self._cache = {}
        self._cache_size = cache_size
        self._cache_index = []
        
    def request(self,time):
        raise NotImplemented
            
    def get(self,time):
        
        time_in  = swdt.time_parse(time)
        dir_format,file_format = os.path.split(self.path.format)
        dir_path,file_name = os.path.split(self.path.get(time_in))
        
        dir_time = swdt.parse_string(dir_format,dir_path)
        
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
                        
class FilePathRequest(PathRequestUnit):
    def request(self,time):
        
        input_time = swdt.time_parse(time)
        
        path = self.path.get(input_time)
        dir_path, file_name = os.path.split(path)
        dir_format, file_format = os.path.split(self.path.format)
                    
        files = get_files(dir_path + '/*')
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
    
class UrlPathRequest(PathRequestUnit):
    def request(self,time):
        
        input_time = swdt.time_parse(time)
    
        path = self.path.get(input_time)
        dir_path, file_name = os.path.split(path)
        dir_format, file_format = os.path.split(self.path.format)
        
        buf = StringIO()

        swdl.download_by_url(dir_path, buf)
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