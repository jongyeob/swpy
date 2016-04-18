from __future__ import absolute_import

import logging
from .. import utils
from ..utils import datetime as dt
from ..utils import download as dl
from ..utils import filepath as fp

from . import kasi, jsoc

LOG    = logging.getLogger(__name__)

VALID_KEYS = ['type','format']
DATA_DIR  = 'data/NASA/SDO/HMI/%(format)/%(type)/%Y/%Y%m%d/'
DATA_FILE = '%Y%m%d_%H%M%S_SDO_HMI_%(type).%(ext)'
TYPES      = ['Ic','Ld','Lw','M','V','S',
              'Ic_45s','Ld_45s','Lw_45s','M_45s','V_45s',
              'Ic_720s','Ld_720s','Lw_720s','M_720s','S_720s',
              'M_synoptic','continuum','magnetogram']
FORMATS = ['jp2','jpg_512','jpg_1024','jpg_4096','fits']

__all__ = ['get_path','request','download_fits']

def get_path(type,format,time=''):
    if not type in TYPES:
        raise TypeError("Invalid type : {}".format(type))
        
    dir_format  = dt.replace(DATA_DIR,time,type=type,format=format)
    ext = ''
    if format in FORMATS:
        ext = format.split('_')[0]
    else:
        raise TypeError("Invalid format : {}".format(format))
    
    file_format  = dt.replace(DATA_FILE,time,type=type,format=format,ext=ext)
    
    return dir_format + file_format

def request(type,format,start_datetime,end_datetime='',cadence=0):
    path_format = get_path(type,format)
        
    return fp.request_files(path_format,\
                            start_datetime,\
                            end_datetime=end_datetime,\
                            cadence=cadence)

def download_fits(type,start_datetime,end_datetime='',cadence=0,overwrite=False):
    '''
     Downloads hmi  files
    
    parameters:
        start_datetime - string
        type           - 'Ic_45s','Ld_45s','Lw_45s','M_45s','V_45s','Ic_720s','Ld_720s','Lw_720s','M_720s','S_720s'
        end_datetime   - string
        
    '''
       
    
    time_series = dt.series(start_datetime,end_datetime,seconds=cadence)
    kasi_series = kasi.request('fits', 'hmi', type, start_datetime, end_datetime, cadence)
    LOG.info('#(time), #(kasi) = %d, %d'%(len(time_series), len(kasi_series)))
    
    urls = [] 
    miss_series = []
    for t in time_series:
        #LOG.debug("%s - %s"%(str(t),str(kasi_series[i])))
        lower_time = t - dt.timedelta(seconds=cadence/2)
        upper_time = t + dt.timedelta(seconds=cadence/2)
        
        url = ''
        url_time = None
        for k in kasi_series:
            url_time = dt.parse(k)
            if lower_time <= url_time <= upper_time:
                url = k
                
                break
        
        if not url:
            miss_series.append(t)
            continue
              
        # download
        filepath = get_path(type, 'fits', url_time)
        dl.download_http_file(url, filepath,overwrite=overwrite)
    
    
    jsoc_files = []
    if len(miss_series) > 0:
        LOG.debug("# missing : %d"%(len(miss_series)))
        jsoc_files = jsoc.request('hmi', type, start_datetime, end_datetime,cadence)
        
    for t in miss_series:
        lower_time = t - dt.timedelta(seconds=cadence/2)
        upper_time = t + dt.timedelta(seconds=cadence/2)
        
        url = ''
        url_time = None
        for j in jsoc_files:
            url_time = dt.parse(j.split('/')[-1].encode())
            if lower_time <= url_time <= upper_time:
                url = j
                break
            
        if not url:
            continue
        
        filepath = get_path(type, 'fits', url_time)
        dl.download_http_file(url, filepath,overwrite=overwrite)
                