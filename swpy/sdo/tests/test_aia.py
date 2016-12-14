import logging
import os
from swpy.utils import filepath as fp
from swpy.sdo import aia
from swpy.utils import datetime as dt
import tempfile
import pytest


logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

    
start = dt.parse('20150101_000000')
end   = dt.parse('20150101_235959')
cadence = 2*3600
aia.DATA_DIR = tempfile.mkdtemp().replace('\\','/') +'/'

def test_request():
    total = 0
    
    for wavelength in aia.WAVELENGTHS:
        for format in aia.FORMATS:
            
            filepath_format = aia.get_path(wavelength, format)
    
            logging.debug("Test file format : %s"%(filepath_format))
        
            for _t in dt.series(start,end,hours=1):
                filepath = dt.replace(filepath_format,_t)
                fp.make_path(filepath)
                logging.debug("Create file : %s"%(filepath))
                if os.path.exists(filepath) == False:
                    with open(filepath,"wb"): pass
                total += 1
            
            logging.debug("Total files : %d"%(total))
            
            ret = aia.request(wavelength,format,start)
            logging.debug("File(%s) : %s"%(str(start),str(ret)))
            
            ret = aia.request(wavelength,format,start,end_datetime=end)
            logging.debug("Number of Files : %d"%(len(ret)))
            
            ret = aia.request(wavelength,format,start,end_datetime=end,cadence=cadence)
            logging.debug("Number of Files (cadence:7200s) : %d"%(len(ret)))

@pytest.mark.online
def test_download_fits():
    start = dt.parse('20150601_000000')
    end   = dt.parse('20150601_020000')
    cadence = 2*3600
    
    wavelength = '304'
    aia.download_fits(wavelength,start,end_datetime=end,cadence=cadence,overwrite=True)
    
    files = aia.request(wavelength, 'fits',start, end, cadence)
    
    logging.debug("# downloaded files : %d"%(len(files)))
    
