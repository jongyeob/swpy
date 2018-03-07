'''
Created on 2015. 4. 24.

@author: jongyeob
'''

import logging
import os
from swpy.utils import filepath as fp
from swpy.sdo import hmi
from swpy.utils import datetime as dt
import tempfile
import pytest


logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))
hmi.DATA_DIR = tempfile.mkdtemp().replace('\\','/') +'/'

def test_request():
    total = 0
    start = dt.parse('20150101_000000')
    end   = dt.parse('20150101_235959')
    cadence = 2*3600
    
    for type in hmi.TYPES:
        for format in hmi.FORMATS:
            
            filepath_format = hmi.get_path(type, format)
            
            logging.debug("Test file format : %s"%(filepath_format))
            
        
            for _t in dt.series(start,end,hours=1):
                filepath = dt.replace(filepath_format,_t)
                fp.make_path(filepath)
                logging.debug("Create file : %s"%(filepath))
                if os.path.exists(filepath) == False:
                    with open(filepath,"wb"): pass
                total += 1
            
            logging.debug("Total files : %d"%(total))
            
            ret = hmi.request(type,format,start)
            logging.debug("File(%s) : %s"%(str(start),str(ret)))
            
            ret = hmi.request(type,format,start,end_datetime=end)
            logging.debug("Number of Files : %d"%(len(ret)))
            
            ret = hmi.request(type,format,start,end_datetime=end,cadence=cadence)
            logging.debug("Number of Files (cadence:7200s) : %d"%(len(ret)))

@pytest.mark.online
def test_download_fits():
    start = dt.parse('20150601_000000')
    end   = dt.parse('20150601_020000')
    cadence = 2*3600
    
    type = 'Ic_45s'
    hmi.download_fits(start,type,end_datetime=end,cadence=cadence,overwrite=True)
    
    files = hmi.request(start, type, 'fits', end, cadence)
    
    logging.debug("# downloaded files : %d"%(len(files)))
    
