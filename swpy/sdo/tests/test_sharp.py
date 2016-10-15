'''
Created on 2015. 11. 18.

@author: jongyeob
'''
from __future__ import absolute_import

import pytest
import shutil

from swpy.sdo import sharp
from swpy.utils import test 
from swpy.utils import datetime as dt
import os

def test_load():
    test_time = '20150301'
    
    path = sharp.SharpPath()
    client = sharp.SharpClient(path)
    data = client.load(test_time)
    
    
    
    
def test_path():
    test_dir  = 'temp/sharp_test'
    test_path = test_dir+'/%Y/%Y%m.txt'
    
    start = '20150101'
    end   = '20151231'
    sample = 86400
    
    test_time = '20150301'
    
    test.create_timed_dummies(test_path, start, end, delta={'months':1})
    
    
    timed_path = sharp.TimedFilePath(test_path)
    best_time = timed_path.query(test_time)
    print "Best time : {}".format(best_time)
    response = timed_path.request(best_time)
    print "File response : {}".format(response.path)
    
    os.remove(response.path)
    print "File deleted!"
    
    best_time = timed_path.query(test_time)
    print "Best time : {}".format(best_time)
    response = timed_path.request(best_time)
    print "File response : {}".format(response.path)
    
    shutil.rmtree(test_dir)
    
def test_sharp_request():
    time = '20151001_000000'
    
    remote = sharp.SharpPathJSOC('hmi.sharp_720s')
    last_time = remote.get_last_time()
    print "Last time : {}".format(last_time)
    
    best_time = remote.query(time)
    print "Best time : {}".format(best_time)
     
    response  = remote.request(time)
    text = response.read()
    print text

import sys    
def test_sharp_download():
    start = '20151001_000000'
    end   = '20151003_235959'
    sample= 86400
    
    reader  = sharp.SharpPathJSOC('hmi.sharp_720s')
    writter = sharp.SharpPath()
    
    
    down = sharp.TimedDownloader(reader,writter)
    down.download(start,end,step=sample) 
    down.download(start,end,step=sample,overwrite=True)
    down.download(start,end,step=sample)
    
    
if __name__ == '__main__':
    test_load()
    #test_sharp_download()
    #test_sharp_request()
    #test_path()