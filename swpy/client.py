'''
Created on 2017. 12. 21.

@author: jongyeob
'''
import os
from datetime import datetime

from swpy import utils2 as swut
from request import RequestUnit
from timepath import TimeFormat

class ClientUnit(RequestUnit):
    
    def request(self,time):
        
        input_time = swut.time_parse(time)
        
        path = self.path.get(input_time)
        path_format = self.path.get_format()
        
        dir_path, file_name = os.path.split(path)
        dir_format, file_format = os.path.split(path_format)
                    
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
    
    def load(self,time,*args,**kwargs):
        raise NotImplemented
