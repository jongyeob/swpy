'''
Created on 2016. 10. 22.

@author: jongyeob
'''

import swpy
from swpy.utils2 import date_time as swdt 
from swpy.utils2.database import DataBase
DB_TESTFILE = swpy.TEMP_DIR + '/dbTest.pkl'

class TestClient():
    data = {}
    def get(self,time):
        time_str = time.strftime("%Y%m%d_%H%M%S")
        return time_str
    
    def load(self,time):
        parsed_time = swdt.parse(time)
        data = {'time':parsed_time.strftime("%Y%m%d_%H%M%S")}
        self.data = data
        
        return self.data
    
    def save(self,time,data):
        parsed_time = swdt.parse(time)
        self.data = data



def test():
    testClient = TestClient()
    dbTest = DataBase(testClient)
    dbTest.save(DB_TESTFILE)
    dbTest.restore(DB_TESTFILE)
    
    request_time = swdt.parse("20161029_030000")
    data = dbTest.request(request_time)
    print "db request: ", data
    print "db cache: ", dbTest.cache
    
    data['new_key'] = 100
    dbTest.update(request_time,data)
    print "db cache: ", dbTest.cache
    print "client data: ", testClient.data