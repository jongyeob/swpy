'''
Created on 2015. 6. 8.

@author: jongyeob
'''
from __future__ import absolute_import

import logging
import os

from ..utils import datetime as dt
from ..utils import download as dl

from . import hmi


LOG    = logging.getLogger(__name__)

REMOTE_DATA_DIR = 'http://jsoc.stanford.edu/data/hmi/fits/%Y/%m/%d/'
REMOTE_DATA_FILE = 'hmi.M_720s.%Y%m%d_%H0000_TAI.fits'
REMOTE_NRT_FILE = 'hmi.M_720s_nrt.%Y%m%d_%H0000_TAI.fits' 
REMOTE_TIME_URL = 'http://jsoc.stanford.edu/data/hmi/fits/latest_fits_time'

def download(start,end='',cadence=0,overwrite=False):
    '''
    downloads hmi fits from JSOCs
    '''
    
    ret = []
    
    starttime = dt.parse(start)
    endtime = starttime
    if end != '':
        endtime = dt.parse(end) 

    recent_time = dl.download_http_file(REMOTE_TIME_URL)
    recent_time = recent_time.split()[1]
    recent_time = os.path.split(recent_time)[1]
    
    recent_time = dt.parse(recent_time)
    
    dir_cadence = 86400
    
    archive_series = []
    
    starttime_archive = starttime
    endtime_archive   = endtime
    
    if endtime_archive > recent_time:
        endtime_archive = recent_time
        
    for t in dt.series(starttime_archive,endtime_archive,seconds=dir_cadence):
        url = dt.replace(REMOTE_DATA_DIR, t)
        LOG.debug(url)
        
        text = dl.download_http_file(url)
        files = dl.get_list_from_html(text, 'fits')
        archive_series.extend(files)
        
    LOG.info('%d files are found'%(len(archive_series)))
    if len(archive_series) > 0:
        LOG.debug(archive_series[0] + ' ...')
    
    time_format = dt.replace(REMOTE_NRT_FILE)
    time_parser = lambda s:dt.parse_string(time_format,s)
    index = map(time_parser,archive_series)
    archive_series = dt.filter(zip(index,archive_series),start,end_datetime=end,cadence=cadence)

    
    for t,f in archive_series:
        dstpath = hmi.get_path('M','fits_synoptic',t)
        url = dt.replace(REMOTE_DATA_DIR, t) + f
        
        ret.append((t,url,dstpath))
        if download:
            dl.download_http_file(url, dstpath,overwrite=overwrite)
    
    
    return ret
