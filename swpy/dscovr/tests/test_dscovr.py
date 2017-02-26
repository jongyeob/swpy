'''
Created on 2016. 10. 16.

@author: jongyeob
'''
import os
import swpy
from swpy.utils2 import filepath 
from swpy import dscovr
TEST_MAG_FILE = swpy.RESOURCE_DIR +'/test/dscovr-mag-sample.json'
TEST_PLASMA_FILE = swpy.RESOURCE_DIR +'/test/dscovr-plasma-sample.json'

dscovr.clients.PATH_PATTERN = swpy.TEMP_DIR + dscovr.clients.PATH_PATTERN

def test():
    print "Test()"
    
    testClient = dscovr.DscovrRTClient('mag-1-day')
    print testClient.get('2017-01-01')

    fp = open(TEST_MAG_FILE)
    mag_data = testClient.load(fp)
    fp.close()
    print(mag_data)
    
    fp = open(TEST_PLASMA_FILE)
    plasma_data = testClient.load(fp)
    fp.close()
    print(plasma_data)
    
    
def test2():
    print "Test2()"
    test_data = {
    "time_tag":['20150510'],
    "bx_gsm":[100],
    "by_gsm":[100],
    "bz_gsm":[100],
    "lon_gsm":[100],
    "lat_gsm":[100],
    "bt":[100],
    "worng":[100] # wrong keyword
    }

    
    mag = dscovr.DscovrClient("mag-1-day")
    mag_file =  mag.get("20160510")
    print mag_file
    
    filepath.mkpath(mag_file)
    fp = open(mag_file,'w')
    mag.save(fp,test_data)
    fp.close
    
    save_file = open(mag_file)
    print save_file.read()
    save_file.close()
    
    fp = open(mag_file)
    mag_data = mag.load(fp)
    fp.close()
    print mag_data
    
