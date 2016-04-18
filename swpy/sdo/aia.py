from __future__ import absolute_import

import logging

from .. import utils
from ..utils import download as dl
from ..utils import datetime as dt


LOG    = logging.getLogger(__name__)

DATA_DIR      = 'data/NASA/SDO/AIA/%(wavelength)/%(format)/%Y/%Y%m%d/'
DATA_FILE     = '%Y%m%d_%H%M%S_SDO_AIA_%(wavelength).%(ext)'
WAVELENGTHS   = ['131','1600','1700','171','193','211','304','335','4500','94']
FORMATS       = ['jp2',
                 'jpg_512','jpg_1024','jpg_2048','jpg_4096',
                 'fits','fits_synoptic']


__all__ = ['get_path','request','download_fits']


def get_path(wavelength,format,time=''):
    if not wavelength in WAVELENGTHS:
        raise TypeError("Invalid wavelength : {}".format(wavelength))
    
    ext        = ''
    file_wavelength = wavelength
    dir_wavelength  = wavelength
    if format in FORMATS:
        ext = format.split('_')[0]
        if format == 'fits_synoptic':
            file_wavelength = wavelength + '_synoptic'
            dir_wavelength  = 'synoptic/'+wavelength
    else:
        raise TypeError("Invalid format : {}".format(format))
        
    dir_format  = dt.replace(DATA_DIR,time,
                             wavelength=dir_wavelength,
                             format=format)
    file_format  = dt.replace(DATA_FILE,time,
                              wavelength=file_wavelength,
                              format=format,ext=ext)
    
    return dir_format + file_format
    

def request(wavelength,format,start_datetime,end_datetime='',cadence=0):
    path_format = get_path(wavelength,format)
        
    return utils.filepath.request_files(path_format,\
                               start_datetime,\
                               end_datetime=end_datetime,\
                              cadence=cadence)

def download_fits(wavelength,start_datetime,end_datetime='',cadence=0,overwrite=False):
    '''
     Downloads hmi  files
    
    parameters:
        start_datetime - string
        wavelength     - 
        end_datetime   - string
        
    '''
    from . import kasi, jsoc
       
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
            