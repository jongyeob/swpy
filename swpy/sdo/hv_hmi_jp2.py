'''
Created on 2014. 9. 26.

@author: jongyeob
'''
from __future__ import absolute_import

import logging

from . import hmi
from ..utils import datetime as dt
from ..utils import download as dl


LOG    = logging.getLogger(__name__)
HOST   = 'helioviewer.org'
TYPES = {'continuum':'Ic',
         'magnetogram':'M'}

_continuum_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,5,29,11,51,40.30)]
_magnetogram_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,05,29,11,39,40.30)]

__all__ = ['request','download']

def make_url(type,datetime):
    '''
    return hmi jp2 url from nasa data server
    
    parameters:
        type : Ic, M
        datetime
    returns:
        path (string)
    '''
    
    image_string = ''
    if type in TYPES:
        image_string = type
    else:
        for k in TYPES:
            if type in TYPES[k]:
                image_string = k
    
    if not image_string:
        raise ValueError("Invalid type : {}".format(type))
    
    t = dt.parse(datetime)
     
    year,month,day,hour,miniute,second = dt.tuples(t,fsecond=True)
          
    dirname = ''

    if image_string == 'continuum':
        if _continuum_start_time[0] <= t < _continuum_start_time[1]:
            dirname = '/jp2/HMI/continuum/%4d/%02d/%02d'%(year,month,day)
        elif _continuum_start_time[1] <= t:
            dirname = '/jp2/HMI/%4d/%02d/%02d/continuum'%(year,month,day)
    elif image_string == 'magnetogram':
        if _magnetogram_start_time[0] <= t < _magnetogram_start_time[1]:
            dirname = '/jp2/HMI/magnetogram/%4d/%02d/%02d'%(year,month,day)
        elif _magnetogram_start_time[1] <= t:
            dirname = '/jp2/HMI/%4d/%02d/%02d/magnetogram'%(year,month,day)
    
          
    return 'http://{}/{}'.format(HOST,dirname)    

def irequest(type,start,end='',cadence=0):
    _start = dt.parse(start)
    _end = _start
    if end:
        _end = dt.parse(end)
    
    time_parser = lambda s:dt.parse_string("%Y_%m_%d__%H_%M_%S_%f__\S+", s)
    
    for t in dt.iseries(_start, _end, days=1):
        
        url = make_url(type,t)
        contents = dl.download_http_file(url)
        if not contents:
            continue
     
        list_files = dl.get_list_from_html(contents,'jp2')
        index = map(time_parser,list_files)
        records = dt.filter(zip(index,list_files), _start, _end, cadence)
        for rec in records:
            yield rec
            
            
def request(type,start,end='',cadence=0):
    return [ f for f in irequest(type,start,end=end,cadence=cadence)]


def download(type,start,end='',cadence=0,overwrite=False):
    '''
    retrieve files from nasa data server (jp2).

    returns: file path
    '''
    conn = dl.get_http_conn(HOST)
    
    for i,filename in irequest(type,start,end=end,cadence=cadence):
        url  = make_url(type, i) + filename
        dstpath = hmi.get_path(type,'jp2',i)
        dl.download_http_file(url, dstpath,overwrite=overwrite, conn=conn)
            
    conn.close()
