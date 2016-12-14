#!/usr/bin/python

from __future__ import absolute_import

import logging
from .. import utils
from ..utils import datetime as dt
from ..utils import download as dl
from . import aia

LOG    = logging.getLogger(__name__)
HOST   = 'jsoc.stanford.edu'
WAVELENGTHS   = ['131','1600','1700','171','193','211','304','335','4500','94']

def make_url(wavelength,time):
    
    
    dirpath = "data/aia/images/{:%Y/%m/%d}/{}/".format(time,wavelength)
    url = "http://{}/{}".format(HOST,dirpath)
    
    return url

def irequest(wavelength,start,end='',cadence=0):
    
    begintime = dt.parse(start)
    endtime   = begintime
    if end:
        endtime = dt.parse(end)
        
    time_parser = lambda s:dt.parse_string('%Y_%m_%d__%H_%M_%S_%f',s)
    for time in dt.series(begintime, endtime, days=1 ):
        
        url = make_url(wavelength,time)
        contents = dl.download_http_file(url)
        
        if not contents:
            continue
        
        files = dl.get_list_from_html(contents, "jp2")
        if not files:
            continue
        
        index = map(time_parser,files)
        files = dt.filter(zip(index,files), begintime, endtime,cadence=cadence)
        
        for f in files:
            yield f
    
def request(wavelength,start,end='',cadence=0):
    return irequest(wavelength, start, end=end, cadence=cadence)


def download(wavelength,start,end='',cadence=0,overwrite=False):
   
    conn = dl.get_http_conn(HOST)
    
    for t,file_name in irequest(wavelength,start,end=end,cadence=cadence):

        remote_url = make_url(wavelength,t) + file_name
        jp2_file_path = aia.get_path(wavelength,'jp2',t)
        
    
        dl.download_http_file(remote_url, jp2_file_path, overwrite=overwrite,conn=conn)
                
    
    conn.close()
    