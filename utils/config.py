#!/usr/bin/python


from os import path

import ConfigParser as cp
import logging
LOG = logging.getLogger(__name__)

class Config():
    '''
    Load config file, if option is not find, save default
    Find config file automatically to parent directories, when current directory does not have config file.
    '''
    _config = None
    _filepath = None
    _section = None
    _change = False
    
    def __init__(self,filepath,section):
        
        filepath = path.abspath(filepath)
        self._filepath = filepath
        self._section = section
        self._config = cp.SafeConfigParser()
        
        is_find = False        
        while(path.ismount(filepath) == False and is_find == False):
            if path.exists(filepath) == False:
                dirpath,filename = path.split(filepath)
                filepath = path.normpath(dirpath +'/../'+filename)
                LOG.debug('searching ini file at %s'%(filepath))
            else:
                is_find = True
                self._filepath = filepath
        
        self._config.read(self._filepath)
        
        if is_find == False:
            LOG.info("No log file is found! %s"%(self._filepath))
        
        if self._config.has_section(section) == False:
            self._config.add_section(section)
            self._change = True
    def get_working_directory(self):
        dirpath,_ = path.split(self._filepath)
        return dirpath 
    def load(self,option,default):
        '''
        return option value (string)
        '''
        value = default
            
        if self._config.has_option(self._section, option) == False:
            self._config.set(self._section, option, str(default))
            self._change = True
        else:
            value = self._config.get(self._section, option)
        return value
    
    def write(self):
        if self._change == True:
            with open(self._filepath,'w') as f:
                self._config.write(f)
                _change = False
            
    def __del__(self):
        self.write()