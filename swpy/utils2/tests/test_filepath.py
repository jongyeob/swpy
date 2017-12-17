'''
Created on 2017. 4. 6.

@author: parkj
'''

from datetime import datetime, timedelta
import swpy
from swpy import utils2 as swut
from swpy.utils2.filepath import *


def test_TimeFormattedPath():
    time_format = "%Y%m%d_%H%M%S"
    test_path = TimeFormattedPath(time_format)
    start_time = datetime(2017,04,06)
    end_time   = datetime(2017,04,06,10)
    time_step  = timedelta(hours=1)
    
    current_time = start_time
    while(current_time < end_time):
        path = test_path.get(current_time)
        assert path == current_time.strftime(time_format)
        current_time += time_step
        
def test_PathRequest():
    time_format = "%Y%m%d_%H%M%S"
    test_path = TimeFormattedPath(time_format)
    start_time = datetime(2017,04,06)
    end_time   = datetime(2017,04,06,10)
    valid_time = datetime(2017,04,06)
    invalid_time = datetime(2017,04,07)

    
    class TestRequest(PathRequest):
        def request(self,time):
            return swut.time_series(start_time, end_time, hours=1)
            
    test_request = TestRequest(test_path)
    
    request_path = test_request.get(valid_time)
    request_time = datetime.strptime(request_path,time_format)
    assert request_time == valid_time
    
    try:
        request_path = test_request.get(invalid_time)
        assert False
    except:
        print "Invalid_time"
    
def test_FilePathRequest():
    test_dir = swpy.TEMP_DIR + 'test/'
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    
    time_format = test_dir + "%Y%m%d_%H%M%S"
    test_path = TimeFormattedPath(time_format)
    
    start_time = datetime(2017,04,06)
    end_time   = datetime(2017,04,06,10)
    time_step  = timedelta(hours=1)
    
    current_time = start_time
    while(current_time < end_time):
        f = open(test_path.get(current_time),'w')
        f.close()
        current_time += time_step
        
    
    test_request = FilePathRequest(test_path)
    
    request_path = test_request.get(start_time)
    assert request_path == start_time.strftime(time_format)
    
    margin = 60
    test_request = FilePathRequest(test_path,margin=margin)
    
    request_path = test_request.get(start_time + timedelta(seconds=1))
    assert request_path == start_time.strftime(time_format)
    
    request_path = test_request.get(start_time + timedelta(seconds=margin/2+1))
    assert not request_path 
    
    current_time = start_time
    while(current_time < end_time):
        os.remove(test_path.get(current_time))
        current_time += time_step
    os.rmdir(test_dir)
    
def test_UrlPathRequest():
    url_path_pattern = 'http://jsoc.stanford.edu/data/aia/synoptic/%Y/%m/%d/H%H%M/AIA%Y%m%d_%H%M_0094.fits'
    test_time = datetime(2017,03,01)
    
    time_step = timedelta(hours=1)
    url_path = UrlPathRequest(TimeFormattedPath(url_path_pattern))
    
    time_list = url_path.request(test_time)
    
    request_path = url_path.get(time_list[0])
    
    assert request_path == test_time.strftime(url_path_pattern)