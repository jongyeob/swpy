'''
Created on 2017. 2. 23.

@author: parkj
'''
from datetime import datetime,timedelta
import logging
from cStringIO import StringIO

logging.basicConfig(level=10)

import swpy
from swpy import sharp
from swpy import utils2 as swut
from swpy.utils2 import testing

TEST_JSON_FILE = swpy.RESOURCE_DIR + '/test/jsoc-sharp-sample.json'  
TEST_TXT_FILE = swpy.RESOURCE_DIR + '/test/jsoc-sharp-sample.txt'

def test():
    client = sharp.SharpJsocClient()
    print client.get_last_time()
    
    client = sharp.SharpJsocClient(cea=False)
    print client.get_last_time()
    
    client = sharp.SharpJsocClient(nrt=True)
    print client.get_last_time()
    
    client = sharp.SharpJsocClient(cea=False,nrt=True)
    print client.get_last_time()
    
        
def test2():
    query_time = datetime.utcnow() - timedelta(days=90)
    
    keywords = [None,sharp.DEFAULT_KEYWORDS]
    
    for key in keywords:
        print 'Test for selected keys'
        if key:
            print 'The number of keys: ',len(key)
        else:
            print "For all of keywords"
        
        client = sharp.SharpJsocClient(keywords=key)
        url = client.get(query_time)
        
        ## Download all
        str_input = StringIO()
        
        swut.download_by_url(url, str_input)
        
        content = str_input.getvalue()
        str_input.close()
        

def test3():
    keywords = sharp.DEFAULT_KEYWORDS
    client = sharp.SharpJsocClient(keywords=keywords)
    
    ## Load
    fr = open(TEST_JSON_FILE,'r')
    
    data = client.load(fr)
    
    fr.close()
        
    print "The number of data keys: ", len(data.keys())

    local = sharp.SharpClient(keywords)
    
    path = local.get("20170101")
    print path
    
    fw = open(TEST_TXT_FILE,'w')
    local.save(fw,data)
    fw.close()
    
    fr = open(TEST_TXT_FILE,'r')
    data2 = local.load(fr)
    fr.close()
    
    print "Keys: {} vs {}".format(len(data),len(data2))
    
if __name__ == "__main__":
    testing.run_test(locals())