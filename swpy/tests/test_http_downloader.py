'''
Created on 2017. 12. 21.

@author: jongyeob
'''
import os
import SimpleHTTPServer
import SocketServer

import swpy
from swpy import utils2 as swut

from cStringIO import StringIO
from datetime import datetime

import threading


HTTPD = None
HTTP_PORT = 8510

def setup_function(function):
    global HTTPD
     
    test_dir = swpy.RESOURCE_DIR + '/test/'
 
    HTTPD = swut.HttpServer(test_dir,HTTP_PORT) 
    HTTPD.start()
     
     
def teardown_function(function):
    HTTPD.stop()


def test_http_downloader_search():
    
    test_time = datetime(2017,12,20,17,01,22)
    
    downloader = swpy.HttpDownloader('http://localhost:{}/%Y%m%d/%Y%m%d_%H%M%S'.format(HTTP_PORT))
    
    
    match_time = downloader.search(test_time)
    
    
    assert match_time == test_time
    
def test_http_downloader_fetch():
    
    test_time = datetime(2017,12,20,17,01,22)
    
    downloader = swpy.HttpDownloader('http://localhost:{}/%Y%m%d/%Y%m%d_%H%M%S'.format(HTTP_PORT))
    
    contents = downloader.fetch(test_time)
    
    assert contents == '20171220_170122'


if __name__ == "__main__":
    swut.run_test(locals())