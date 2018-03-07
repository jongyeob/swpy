'''
Created on 2017. 2. 23.

@author: parkj
'''
import os
import logging; logging.basicConfig(level=10)


import swpy
from swpy import utils2 as swut
from cStringIO import StringIO
from datetime import datetime

import threading

LOG = logging.getLogger(__name__)

HTTPD = None
HTTP_PORT = 8504

def setup_function(function):
    global HTTPD
     
    test_dir = swpy.RESOURCE_DIR + '/test/'
 
    HTTPD = swut.HttpServer(test_dir,HTTP_PORT) 
    HTTPD.start()
     
    print "HTTP server started"
     
def teardown_function(function):
    HTTPD.stop()

def test_download_by_url():
    
    test_url = ['http://localhost:{}/testfile'.format(HTTP_PORT),
                {'url':'http://localhost:{}/testfile'.format(HTTP_PORT)}]
    
    
    for url in test_url:
        io = StringIO()
        swut.download_by_url(url, io)
        text = io.getvalue()
        length = len(text)
        
        print 'Download {} bytes'.format(length)
        
        io.close()
