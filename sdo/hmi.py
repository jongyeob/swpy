import logging

from swpy import utils
from swpy.utils import date_time as dt, download as dl

LOG    = logging.getLogger(__name__)
DATA_INFO = {'agency':'NASA','machine':'SDO','instrument':'HMI'}
DATA_DIR  = 'data/%(agency)/%(machine)/%(instrument)/%(type)/%(format)/%Y/%Y%m%d/'
DATA_FILE = '%Y%m%d_%H%M%S_%(machine)_%(instrument)_%(type).%(format)'
CADENCE   = 45

def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)

def get_path(type,format,datetime=''):
    dir_format  = dt.replace(DATA_DIR,datetime,type=type,format=format,**DATA_INFO)
    file_format  = dt.replace(DATA_FILE,datetime,type=type,format=format,**DATA_INFO)
    
    return dir_format + file_format

def request(start_datetime,type,format,end_datetime='',cadence=0):
    path_format = get_path(type,format)
    
    if cadence == 0:
        cadence = CADENCE
        
    return utils.filepath.request_files(path_format,\
                               start_datetime,\
                               end_datetime=end_datetime,\
                               cadence=cadence)

def download_fits(start_datetime,type,end_datetime='',cadence=0,overwrite=False):
    '''
     Downloads hmi  files
    
    parameters:
        start_datetime - string
        type           - 'Ic_45s','Ld_45s','Lw_45s','M_45s','V_45s','Ic_720s','Ld_720s','Lw_720s','M_720s','S_720s'
        end_datetime   - string
        
    '''
    import kasi, jsoc
       
    
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
                
