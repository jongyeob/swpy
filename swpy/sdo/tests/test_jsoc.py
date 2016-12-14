'''
Created on 2015. 5. 26.

@author: jongyeob
'''

import logging
from swpy.sdo import jsoc


logging.basicConfig(level=logging.DEBUG,format="%(asctime)s %(message)s") 



def test_download():
    jsoc.download('hmi','M_45s',"2015-04-01T00:00:00","2015-04-01T01:00:00")
    
    
    jsoc.download('hmi','M_45s',"2015-04-01T00:00:00","2015-04-01T01:00:00",90)
    

    jsoc.download('aia','304',"2015-04-01T00:00:00","2015-04-01T01:00:00",3600)
    
        
