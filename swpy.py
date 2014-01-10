'''
Created on 2013. 12. 10.

@author: jongyeob
'''


import sys,os
from os.path import normpath,exists
import ConfigParser as cp


swpy_path = os.getcwd()

data_dir = normpath(swpy_path+'/data')
meta_dir = normpath(swpy_path+'/meta')
conf_dir = normpath(swpy_path+'/conf')
temp_dir = normpath(swpy_path+'/temp')
logs_dir = normpath(swpy_path+'/logs')

print 'swpy path %s'%(swpy_path)
print 'data directory %s'%(data_dir)


def load_config():
    '''
    @summary: load config.file (swpy.conf). config file can be loaded in parents directory if it is not exist.
    if config file can not find last root directory. swpt_path is root/swpy
    '''
    
    global conf_dir,data_dir,meta_dir,temp_dir,logs_dir
    config_file_path = normpath(conf_dir + "/swpy.conf")
    
    if (exists(config_file_path) == False):
        print "The configuration file of SWPy does not exist.";
        print "The configuration file path is '" + config_file_path + "'.";
        return False;

    config = cp.SafeConfigParser();
    config.read(config_file_path);

    
    conf_dir = config.get("swpy", "conf_dir")
    data_dir = config.get("swpy", "data_dir")
    temp_dir = config.get("swpy", "temp_dir")
