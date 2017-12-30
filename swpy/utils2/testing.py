'''
Created on 2015. 11. 19.

@author: jongyeob
'''

import sys
import os
import logging
import cPickle as Pickle
import random
from datetime import timedelta
import math
import traceback

import SimpleHTTPServer
import SocketServer
import threading

import date_time as swdt
import filepath as swfp

LOG = logging.getLogger(__name__)

TEST_CACHE_FILE = 'test_cache.pkl'

def create_dummy_file(timed_path,start,end,**kwargs):
    total = 0
    
    delta = {}
    delta['days'] = kwargs.pop('days',0)
    delta['hours'] = kwargs.pop('hours',0)
    delta['minutes'] = kwargs.pop('minutes',0)
    delta['seconds'] = kwargs.pop('seconds',0)
        
    for _t in swdt.series(start,end,**delta):
        filepath = _t.strftime(timed_path)
        
        swfp.mkpath(filepath)
                
        if not os.path.exists(filepath):
            with open(filepath,"wb"): pass
        
        total += 1
        
    LOG.debug("The number of created files : %d"%(total))

class HttpServer():
    def __init__(self,base_dir,port):
        self.httpd = None
        self.base_dir = base_dir
        self.port = port
        
    def start(self):
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    
        os.chdir(self.base_dir)
        
        self.httpd = SocketServer.TCPServer(("",self.port),handler) 
        
        server_thread = threading.Thread(target=self.httpd.serve_forever)       
        server_thread.start()
        
        
    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()        
        self.httpd = None
        self.server_thread = None    
    
    
def run_test(test_functions):
    '''
    test_functions: dict[function name]=function address
    '''
    test_file = sys.argv[0]
    
    cache = {}
    try:
        fr = open(TEST_CACHE_FILE,'r')
        cache = Pickle.load(fr)
        fr.close()
    except: pass
    
    if not cache.has_key(test_file):
        cache[test_file] = set()
    
    functions = set([ name for name in test_functions 
                if name.startswith('test')
                and callable(test_functions[name])]) 
    
    new_functions = []
    if functions == cache[test_file]:
        new_functions = list(functions)
        LOG.debug("All tested, start testing again")
    else:
        new_functions = list(functions-cache[test_file]) 
    
    new_functions.sort()
    
    
    for name in new_functions:
            
        LOG.debug("Testing for {}()".format(name))
        
        try:
            test_functions[name]()
            cache[test_file].add(name)
        except Exception as err:
            traceback.print_exc()
            LOG.error("Test abort")
            break
        
        
    fw = open(TEST_CACHE_FILE,'w')
    Pickle.dump(cache,fw)
    fw.close()
