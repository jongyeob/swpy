'''
Created on 2016. 10. 31.

@author: jongyeob
'''

try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

from os import path

class Config():
    def __init__(self,filepath):
        self.filepath = filepath
        self.parser = ConfigParser()
        if path.exists(self.filepath):
            self.parser.read(self.filepath)
        
    def load(self,cfg,section_name,format={}):
        
        if not section_name in self.parser.sections():
            self.parser.add_section(section_name)
            for key in cfg.keys():
                self.parser.set(section_name,key,cfg[key])
            with open(self.filepath,'wb') as fp:
                self.parser.write(fp)
                    
        for key in cfg.keys():
            val  = self.parser.get(section_name,key,cfg[key])
            if format.has_key(key):
                val = format[key](val)
                        
            cfg[key] = val
