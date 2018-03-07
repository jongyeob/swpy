'''
Created on 2017. 10. 17.

@author: jongyeob
'''
import logging
import swpy
from swpy import utils2
from cStringIO import StringIO
from datetime import timedelta

logging.basicConfig(level=10)
    
class TestData(utils2.DataUnit):
    pass
    

class TestClient(utils2.ClientUnit):
    def load(self,file):
        print "Clinet Load()"
        print "file: {}".format(file)
        
        data = TestData(body = file)
        
        return data
    
    def save(self,file,data):
        print "Client Save()"
        print "file: {}".format(file)
        print "data: {}".format(data.body)
        
        
def test_create_dummy():
    
    test_fmt = ['%Y%m%d_%H%M%S',
                '%Y%m%d_%H%M',
                '%Y%m%d_%H',
                '%Y%m%d',
                '%Y%m',
                '%Y']
    
    
    for itest_fmt in test_fmt:
        test_path = utils2.TimeFormatPath(itest_fmt)
        test_client = TestClient(test_path)

        t1 = utils2.parse('20170101_000000')
        t2 = utils2.parse('20171231_235959')
        td = 3600
        
        random_t = utils2.random_time(t1,t2)
        print random_t
        
        test_time = utils2.Time( t1, t2, td )
    
        jitter = 60  #seconds
        drop_rate = 10 #%
        utils2.testing.create_dummy(test_client, test_time,jitter,drop_rate)
        
    