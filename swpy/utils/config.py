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
    
    def __init__(self,filepath,section=''):
        
        filepath = path.abspath(filepath)
        self._filepath = filepath
        self._config = cp.SafeConfigParser()
        
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
        dirpath,_ = path.split(self._filepath)
        return dirpath
    def get_sections(self):
        return self._config.sections()
    def set_section(self,section):
        if section is None or section == '':
            self._section = 'DEFAULT'
            return
        
        self._section = section
       
        if self._config.has_section(self._section) == False:
            self._config.add_section(self._section)
            self._change = True
    
    def load(self,option,default,section=None):
        '''
        return option value (string)
        '''
        value = default
        if section is not None:
            self.set_section(section)
         
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
