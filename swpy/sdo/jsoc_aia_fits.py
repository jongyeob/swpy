'''
Created on 2015. 6. 8.

@author: jongyeob
'''

import logging

from swpy import utils
from swpy.utils import datetime as dt, download as dl

LOG    = logging.getLogger(__name__)
DATA_INFO = {'agency':'NASA','machine':'SDO','instrument':'AIA'}
DATA_DIR  = 'data/%(agency)/%(machine)/%(instrument)/synoptic/%(wavelength)/%Y/%Y%m%d/'
DATA_FILE = '%Y%m%d_%H%M%S_%(machine)_%(instrument)_%(wavelength)_synoptic.fits'

REMOTE_DATA_DIR = 'http://jsoc.stanford.edu/data/aia/synoptic/%Y/%m/%d/H%H00/'
REMOTE_DATA_FILE = 'AIA%Y%m%d_%H%M_%(wavelength).fits'
REMOTE_TIME_URL = 'http://jsoc.stanford.edu/data/aia/synoptic/image_times'

NRT_DATA_DIR = 'http://jsoc.stanford.edu/data/aia/synoptic/nrt/%Y/%m/%d/H%H00/'
NRT_DATA_FILE = 'AIA%Y%m%d_%H%M%S_%(wavelength).fits'
NRT_TIME_URL = 'http://jsoc.stanford.edu/data/aia/synoptic/nrt/image_times'

def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)
def get_path(wavelength,datetime=''):
    dir_format  = dt.replace(DATA_DIR,datetime,wavelength=wavelength,**DATA_INFO)
    file_format  = dt.replace(DATA_FILE,datetime,wavelength=wavelength,**DATA_INFO)
    
    return dir_format + file_format

def request(start_datetime,wavelength,end_datetime='',cadence=0):
    path_format = get_path(wavelength)
        
    return utils.filepath.request_files(path_format,\
                               start_datetime,\
                               end_datetime=end_datetime,\
                               cadence=cadence)

def download(start,wavelength,end='',cadence=0,overwrite=False):
    '''
    downloads aia synotic from JSOCs
    
    parameters:
        start          - string
        wavelength     - string
        end            - string
    '''
    starttime = dt.parse(start)
    endtime = starttime
    if end != '':
       endtime = dt.parse(end) 

    recent_time = dl.download_http_file(REMOTE_TIME_URL)
    recent_time = recent_time.split()[1]
    recent_time = dt.parse(recent_time)

    time_series = dt.series(starttime,endtime,seconds=cadence)
    archive_series = []
    nrt_series = []
    
    starttime_archive = starttime
    endtime_archive   = endtime
    starttime_recent  = None
    endtime_recent = None
    
    if endtime_archive > recent_time:
        endtime_archive = recent_time
        endtime_recent = endtime
        starttime_recent = recent_time
        if starttime > recent_time:
            starttime_recent = starttime
        
    wave = str(wavelength).zfill(4)
    
    dir_cadence = 3600
    if cadence > 3600:
        dir_cadence = cadence
                 
    for t in dt.series(starttime_archive,endtime_archive,seconds=dir_cadence):
        url = dt.replace(REMOTE_DATA_DIR, t,wavelength=wave)
        LOG.debug(url)
        
        text = dl.download_http_file(url)
        files = dl.get_list_from_html(text, 'fits')
        archive_series.extend(files)
        
    LOG.info('%d files are found'%(len(archive_series)))
    if len(archive_series) > 0:
        LOG.debug(archive_series[0] + ' ...')
    
    time_format = dt.replace(REMOTE_DATA_FILE,wavelength=wave)
    time_parser = lambda s:dt.parse_string(time_format, s)
    index = [(i,) for i in map(time_parser,archive_series) if i]
    indexf = dt.filter(index,start,end_datetime=end,cadence=cadence)
    
    LOG.info('#(time), #(archive) = %d, %d'%(len(time_series), len(indexf)))
    
    for i, in indexf:
        dstpath = get_path(wavelength,i)
        url = dt.replace(REMOTE_DATA_DIR+REMOTE_DATA_FILE, i,wavelength=wave)
              
        dl.download_http_file(url, dstpath,overwrite=overwrite)
    
            
    if starttime_recent is not None:
        LOG.debug("Append data in nrt archive")
        for t in dt.series(starttime_recent,endtime_recent,seconds=dir_cadence):
            url = dt.replace(NRT_DATA_DIR, t,wavelength=wave)
            LOG.debug(url)
        
            text = dl.download_http_file(url)
            files = dl.get_list_from_html(text, 'fits')
            nrt_series.extend(files)
        
       
        LOG.info('%d files are found'%(len(nrt_series)))
        if len(nrt_series) > 0:
            LOG.debug(nrt_series[0] + ' ...')
        
        time_format = dt.replace(NRT_DATA_FILE,wavelength=wave)
        time_parser = lambda s:dt.parse_string(time_format, s)
        index  = [(i,) for i in map(time_parser,nrt_series) if i]
        indexf  = dt.filter(index,start,end_datetime=end,cadence=cadence)
        
        LOG.info('#(time), #(nrt) = %d, %d'%(len(time_series), len(indexf)))
        
        for i, in indexf:
            dstpath = get_path(wavelength,i)
            url = dt.replace(NRT_DATA_DIR+NRT_DATA_FILE, i,wavelength=wave)
                  
            dl.download_http_file(url, dstpath,overwrite=overwrite)
