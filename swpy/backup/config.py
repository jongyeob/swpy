#!/usr/bin/python


import logging
from os import path
import os
import re

import ConfigParser as cp


LOG = logging.getLogger(__name__)

class Config():
    '''
    Load config file, if option is not find, save default
    Find config file automatically to parent directories, when current directory does not have config file.
    '''
    _config = None
    _filepath = ''
    _section = ''
    _change = False
    
    def __init__(self,filepath='',section=''):
        
        self._config = cp.SafeConfigParser()
        
        if filepath != '':
            filepath = path.abspath(filepath)
            self._filepath = filepath
            
            is_find = False        
            while(is_find == False):
                dirpath,filename = path.split(filepath)
    
                if path.exists(filepath) == False:
                    if path.ismount(dirpath) == True:
                        break
                    filepath = path.normpath(dirpath +'/../'+filename)
                    LOG.debug('searching ini file at %s'%(filepath))
                else:
                    is_find = True
                    self._filepath = filepath
            
            self._config.read(self._filepath)
        
            if is_find == False:
                LOG.info("No log file is found! %s"%(self._filepath))
        
        self.set_section(section)
            
    def get_working_directory(self):
        if self._filepath == '':
            return os.curdir
        
        dirpath,_ = path.split(self._filepath)
        return dirpath + os.sep
    
    def get_sections(self):
        return self._config.sections()
    
    def set_section(self,section,ns=None):
        if section in [None,'','__main__']:
            self._section = 'DEFAULT'
            return
        
        self._section = section
        if self._config.has_section(self._section) == False:
            self._config.add_section(self._section)
            self._change = True
            
    def load_ns(self,option,ns,section=None):
        default = ''
        if ns.has_key(option) == True:
            default = ns[option] 
        value = self.load(option,default,section)
        ns[option] = value
        
        return value
    def get_option(self,option,value=None):
        if value is not None:
            value = str(value)
            self._config.set(self._section,option,value)

        return self._config.get(self._section,option)
        
    def load(self,option,default,section=None):
        '''
        return option value (string)
        '''
        value = str(default)
        if section is not None:
            self.set_section(section)
         
        if self._config.has_option(self._section, option) == False:
            value = value.replace('%','%%')
            i1 = value.find('%%(')
            while i1 != -1:
                i2 = value.find(')',i1)
                if self._config.has_option(self._section,value[i1+3:i2]) == True:
                    value = value[:i1] + value[i1+1:] # remove one of %
                i1 = value.find('%%(',i2)               
                
            self._config.set(self._section, option, value)
            self._change = True
        
        value = self._config.get(self._section, option)
        
        
        return value
    
    def write(self,filepath=''):
        if filepath != '':
            self._filepath = filepath
            
        if self._filepath == '':
            return
        
        if self._change == True:
            with open(self._filepath,'w') as f:
                self._config.write(f)
                _change = False
            
    def __del__(self):
        self.write()
