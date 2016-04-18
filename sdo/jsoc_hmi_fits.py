'''
Created on 2015. 6. 8.

@author: jongyeob
'''

import logging
import os
from swpy import utils
from swpy.utils import date_time as dt, download as dl

LOG    = logging.getLogger(__name__)
DATA_INFO = {'agency':'NASA','machine':'SDO','instrument':'HMI','type':'M_1k'}
DATA_DIR  = 'data/%(agency)/%(machine)/%(instrument)/%(type)/%Y/%Y%m%d/'
DATA_FILE = '%Y%m%d_%H%M%S_%(machine)_%(instrument)_%(type).fits'


REMOTE_DATA_DIR = 'http://jsoc.stanford.edu/data/hmi/fits/%Y/%m/%d/'
REMOTE_DATA_FILE = 'hmi.M_720s.Y%m%d_%H0000_TAI.fits'
REMOTE_NRT_FILE = 'hmi.M_720s_nrt.Y%m%d_%H0000_TAI.fits' 
REMOTE_TIME_URL = 'http://jsoc.stanford.edu/data/hmi/fits/latest_fits_time'

def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)
    
def get_path(datetime='',**kwargs):
    dir_format  = dt.replace(DATA_DIR,datetime,**DATA_INFO)
    file_format  = dt.replace(DATA_FILE,datetime,**DATA_INFO)
    
    return dir_format + file_format

def request(start_datetime,end_datetime='',cadence=0):
    path_format = get_path()
        
    return utils.filepath.request_files(path_format,\
                               start_datetime,\
                               end_datetime=end_datetime,\
                               cadence=cadence)

def download(start,end='',cadence=0,overwrite=False):
    '''
    downloads hmi fits from JSOCs
    '''
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
    
    time_format = dt.replace(REMOTE_DATA_FILE)
    time_parser = dt.parse
    archive_series = dt.filter(archive_series,start,end_datetime=end,cadence=cadence,time_parser=time_parser)

    
    for f in archive_series:
        t = time_parser(f[0])
        dstpath = get_path(t)
        url = dt.replace(REMOTE_DATA_DIR, t) + f[0]
              
        dl.download_http_file(url, dstpath,overwrite=overwrite)
    
