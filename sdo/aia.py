from swpy import utils
from swpy.utils import date_time as dt, download as dl
import logging

LOG    = logging.getLogger(__name__)
DATA_INFO = {'agency':'NASA','machine':'SDO','instrument':'AIA'}
DATA_DIR  = 'data/$(agency)/$(machine)/$(instrument)/$(wavelength)/$(format)/%Y/%Y%m%d/'
DATA_FILE = '%Y%m%d_%H%M%S_$(machine)_$(instrument)_$(wavelength).$(format)'
CADENCE   = 12

def get_path(wavelength,format,datetime=''):
    dir_format  = dt.replace(DATA_DIR,datetime,wavelength=wavelength,format=format,**DATA_INFO)
    file_format  = dt.replace(DATA_FILE,datetime,wavelength=wavelength,format=format,**DATA_INFO)
   
    return dir_format + file_format

def request(start_datetime,wavelength,format,end_datetime='',cadence=0):
    path_format = get_path(wavelength,format)
    
    if cadence == 0:
        cadence = CADENCE
        
    return utils.request_files(path_format,\
                               start_datetime,\
                               end_datetime=end_datetime,\
                              cadence=cadence)
def download_synoptic(start,wave,end='',cadence=0,**kwargs):
def download_fits(start_datetime,wavelength,end_datetime='',cadence=0,**kwargs):
    '''
     Downloads hmi  files
    
    parameters:
        start_datetime - string
        wavelength     - 
        end_datetime   - string
        
    '''
    import kasi, jsoc
       
    time_series = dt.series(start_datetime,end_datetime,seconds=cadence)
    kasi_series = kasi.request('fits', 'aia', wavelength, start_datetime, end_datetime, cadence)
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
        filepath = get_path(wavelength, 'fits', url_time)
        dl.download_http_file(url, filepath,overwrite=overwrite)
    
    
    jsoc_files = []
    if len(miss_series) > 0:
        LOG.debug("# missing : %d"%(len(miss_series)))
        jsoc_files = jsoc.request('aia', wavelength, start_datetime, end_datetime,cadence)
        
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
        
        filepath = get_path(wavelength, 'fits', url_time)
        dl.download_http_file(url, filepath,overwrite=overwrite)
            