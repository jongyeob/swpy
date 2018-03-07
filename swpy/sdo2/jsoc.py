'''
Created on 2017. 4. 7.

@author: parkj
'''

import logging

from swpy.base import UrlPathRequest, TimeFormattedPath
from swpy import utils2 as swut
from cStringIO import StringIO
import os

LOG= logging.getLogger(__name__)

AIA_DATA_DIR = 'http://jsoc.stanford.edu/data/aia/synoptic/{nrt}/%Y/%m/%d/H%H00/'
AIA_DATA_FILE = 'AIA%Y%m%d_%H%M_{wavelength:04}.fits'
AIA_LAST_TIME_URL = 'http://jsoc.stanford.edu/data/aia/synoptic/{nrt}/image_times'

HMI_DATA_DIR = 'http://jsoc.stanford.edu/data/hmi/fits/%Y/%m/%d/'
HMI_DATA_FILE = 'hmi.M_720s.%Y%m%d_%H0000_TAI.fits'
HMI_NRT_DATA_FILE = 'hmi.M_720s_nrt.%Y%m%d_%H0000_TAI.fits' 
HMI_LAST_TIME_URL = 'http://jsoc.stanford.edu/data/hmi/fits/latest_fits_time' 

class JsocSdoAiaUrlPath(UrlPathRequest): pass
class JsocSdoHmiUrlPath(UrlPathRequest): pass
   
class JsocSdoAiaPathFactory():
    
    '''
    WAVELENGTHS   = ['131','1600','1700','171','193','211','304','335','4500','94']
    '''
    @staticmethod
    def create(wavelength,nrt=False):
        nrt_str = ['','nrt'][nrt]
        pattern = (AIA_DATA_DIR + AIA_DATA_FILE).format(wavelength=wavelength,nrt=nrt_str)
        return JsocSdoAiaUrlPath(TimeFormattedPath(pattern))

    @staticmethod
    def get_last_time():
        buf = StringIO()
        swut.download_by_url(AIA_LAST_TIME_URL, buf)
        
        text = buf.getvalue()
        buf.close()
        
        last_time = text.split()[1]
        last_time = swut.parse(last_time)  
    
        return last_time
    
class JsocSdoHmiPathFactory():
    @staticmethod
    def create():
        pattern = HMI_DATA_DIR + HMI_DATA_FILE
        return JsocSdoHmiUrlPath(TimeFormattedPath(pattern))

    @staticmethod
    def get_last_time():
        buf = StringIO()
        swut.download_by_url(HMI_LAST_TIME_URL, buf)
        
        text = buf.getvalue()
        buf.close()
    
        last_time = text.split()[1]
        last_time = os.path.split(last_time)[1]
        last_time = swut.parse(last_time)  
    
        return last_time

