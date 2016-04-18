'''
Created on 2015. 7. 29.

@author: jongyeob
'''
from __future__ import absolute_import

import logging
from . import utils
from .utils import datetime as dt
from .utils import download as dl


LOG    = logging.getLogger(__name__)
DATA_INFO = {'agency':'ICCON','machine':'NOBEYAMA','instrument':'NoRH'}
DATA_DIR  = 'data/%(agency)/%(machine)/%(instrument)/%Y/%Y%m%d/'
DATA_FILE = '%Y%m%d_%H%M%S_%(instrument).fits'

def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)
def get_path(datetime=''):
    dir_format  = dt.replace(DATA_DIR,datetime,**DATA_INFO)
    file_format  = dt.replace(DATA_FILE,datetime,**DATA_INFO)
    
    return dir_format + file_format

def request(start,end='',cadence=0):
    path_format = get_path()
        
    return utils.filepath.request_files(path_format,\
                               start,\
                               end_datetime=end,\
                               cadence=cadence)

def download(start,end='',cadence=0,overwrite=False,download=True):
    '''
    start, end : UT
    '''
    ret = []
    
    begintime = dt.parse(start)
    endtime   = begintime
    if end:
        endtime = dt.parse(end)
    
    
    beginlt = begintime + dt.timedelta(hours=9)
    endlt   = endtime   + dt.timedelta(hours=9)
    
    host = 'solar-pub.nao.ac.jp'
    conn = dl.get_ftp_conn(host)
    
    for now in dt.series(beginlt,endlt,days=1):

        dir  = 'pub/nsro/norh/fits/10min/{:%Y/%m/%d}'.format(now)
        url = "ftp://{}/{}/".format(host,dir)
        
        files,sizes = dl.get_list_from_ftp(url,conn=conn)
        if not files:
            continue
        
        def time_parser(s):
            t = dt.parse_string('ifa%y%m%d_%H%M%S',s)
            if t:
                t = t.replace(year=t.year+100)
            return t
        
        index = map(time_parser,files)
        files = dt.filter(zip(index,files), begintime, endtime,cadence=cadence)
        for ti,file_name in files:
            remote_url = url + file_name
            localfile = get_path(ti)
            ret.append((ti,remote_url,localfile)) 
            
            if download:
                dl.download_ftp_file(remote_url, localfile, overwrite=overwrite,conn=conn)
                    
        
    conn.close()
    
    return ret