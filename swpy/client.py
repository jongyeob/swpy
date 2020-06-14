'''
Created on 2017. 12. 21.

@author: jongyeob
'''
import os
from datetime import datetime

from . import utils2 as swut
from .request import RequestUnit
from .timepath import TimeFormat

import logging

LOG = logging.getLogger(__name__) 

class ClientUnit(RequestUnit):
    def set_downloader(self,downloader):
        self.downloader = downloader
        
    def get_downloader(self):
        return self.downloader
    
    def download(self,t,overwrite=False):
        if not self.downloader:
            LOG.debug("Downloader not exists")
            return ''
        
        time_in = swut.time_parse(t)
        dst_path = self.path.get(t)
        
        download_path = self.downloader.retrieve(time_in,dst=dst_path,overwrite=overwrite)
        
        if download_path:
            LOG.debug("Download Success! : " + download_path)
            
        return download_path
    
    def request(self,time):
        
        input_time = swut.time_parse(time)
        
        path = self.path.get(input_time)
        path_format = self.path.get_style()
        
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
