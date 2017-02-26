'''
Created on 2016. 10. 31.

@author: jongyeob
'''
from ConfigParser import ConfigParser
from os import path

class Config():
    def __init__(self,filepath):
        self.filepath = filepath
        self.config = ConfigParser()
        if path.exists(self.filepath):
            self.config.read(self.filepath)
        
    def load(self,cfg,section_name,format={}):
        
        if not section_name in self.config.sections():
            self.config.add_section(section_name)
            for key in cfg.keys():
                self.config.set(section_name,key,cfg[key])
            with open(self.filepath,'wb') as fp:
                self.config.write(fp)
                    
        for key in cfg.keys():
            val  = self.config.get(section_name,key,cfg[key])
            if format.has_key(key):
                val = format[key](val)
                        
            cfg[key] = val