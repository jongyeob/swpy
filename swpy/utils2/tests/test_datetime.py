'''
Created on 2015. 7. 9.

@author: jongyeob
'''
import logging

from datetime import datetime
from swpy.utils2.date_time import *

logging.basicConfig(level=0)

def test_series():
    time_list = series('2017-01-01','2017-12-31',86400)
    print "Number of Time: ",len(time_list)
    
    time_list = series('2017-01-01','2017-12-31',86400,jitter=10)
    print "Number of Time (jitter=10): ",len(time_list)
    
    time_list = series('2017-01-01','2017-12-31',86400,drop_rate=0.1)
    print "Number of Time (10% drop): ",len(time_list)
            

    
def test_sample():
    
    time_list = series('2017-01-01','2017-12-31',86400)
    print "Number of Time: ",len(time_list)
    match_time_list = sample(time_list,86400)
    print "Number of Time for 1 day: ", len(match_time_list)
    
    match_time_list2 = sample(time_list,86400*2)
    print "Number of Time for half day: ", len(match_time_list2)
    


def test_parse():
    print parse_string("%Y%m%d","20140201")
    print parse_string("%y%m%d %H%M%S.%f","990201 030201.3")
    print parse_string("%Y-%b-%d","2014-Jul-01")
    print parse_string("%H:%M:%S","20:01:03")
    index = []
    print parse_string("%H:%M:%S","20130103/20:01:03",index=index)
    print index
    
    index = []
    print parse_date("20130303",index=index)
    print index
    
    index = []
    print parse_time("130303",index=index)
    print index
    
    print parse_datetime('2013')
    
    print parse_datetime('2013',prior='time')
    print parse_datetime("asdf/20130101 010101")
    print parse_datetime("130303")
    print parse_datetime("130303",prior='time')
    print parse_datetime("20140101")
    print parse_datetime("010101 20140313")
    print parse_datetime("010101 20140401",prior='time')
       
       
    
    print "parse()"
    print parse(2010) == datetime(2010,1,1)
    print datetime(2010,2,27) == parse(2010,2,27)== \
                                 parse((2010,2,27))== \
                                 parse("20100227")
    print datetime(1999,12,31,11,22,33,444000)
    print parse(1999,12,31,11,22,33.444)
    print parse("19991231_112233.444")
    
    text = "abcd/abcdef/2013/20140202/2014-02-02_002233" # Multiple detect
    print parse(text)
      
    text = '2-Jul-02'
    print parse(text)
    
    print parse_string("/abcd/%Y/%Y%m%d","/abcd/2014/20140101") 
