'''
Created on 2017. 12. 31.

@author: jongyeob
'''

import swpy
from datetime import datetime

import os

def test_retrieve():
    
    
    test_hostname = 'github.com'
    test_path     = '/jongyeob/swpy'
    test_url = 'http://' + test_hostname + test_path
    
    temp_dir  = swpy.downloader.CFG['temp-dir']
        
    class TestDownloader(swpy.downloader.DownloaderUnit):
        def fetch(self,time,wfile):
            pass
            
        
    downloader = TestDownloader(test_url) 
    
    test_time = datetime.now()
    out_path = downloader.retrieve(test_time)
    valid_path = temp_dir + test_hostname + test_path
    
    assert out_path == valid_path, "File location different"
    assert os.path.exists(out_path), "File not exists"
    
    # Test Overwrite Option False
    out_path = downloader.retrieve(test_time, overwrite=False)
    assert out_path == valid_path, "File location different"
    
    # Test Overwrite Option True
    time_before = os.path.getmtime(valid_path)
    out_path = downloader.retrieve(test_time, overwrite=True)
    time_after = os.path.getmtime(valid_path)
    assert time_before !=  time_after, "File not created"
    
    os.remove(out_path)
    
    test_path = './testfile'
    out_path = downloader.retrieve(test_time, test_path)
    
    assert out_path == test_path, "File not created in specific file path"
    
    os.remove(test_path)
     
    