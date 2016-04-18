'''
Created on 2015. 5. 26.

@author: jongyeob
'''
from __future__ import absolute_import

JSOC_REGISTERED_EMAIL = 'parkjy@kasi.re.kr'

import logging
from .. import utils
from .. import jsoc_api
LOG = logging.getLogger(__name__)


def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)

class _URLFetch():
    urls = []
    def download(self,url,**kwargs):
        LOG.debug(url)
        self.urls.append(url)
    def stop(self):
        pass
    
def request(instrument,type,start_datetime,end_datetime='',cadence=0,**kwargs):
    '''
        instrument : aia hmi
        type : aia = 131  1600  1700  171  193  211  304  335  4500  94
               hmi = Ic_45s   Ld_45s   Lw_45s   M_45s   V_45s   
                     Ic_720s  Ld_720s  Lw_720s  M_720s  V_720s  S_720s
    '''
    
    from sunpy.net import jsoc
    from astropy import units
            
    query_args = []
    
    if end_datetime == '':
        end_datetime = start_datetime
        
    query_args.append(jsoc.Time(start_datetime,end_datetime))
    
    default_cadence = 0
    if instrument == 'aia':
        query_args.append(jsoc.Compression('rice'))
        query_args.append(jsoc.Segment('image'))
        query_args.append(jsoc.Wavelength(int(type)*units.AA))
        if type in ['94','131','171','193','211','304','335']:
            query_args.append(jsoc.Series('aia.lev1_euv_12s'))
            default_cadence = 12
        elif type in ['1600','1700']:
            query_args.append(jsoc.Series('aia.lev1_uv_24s'))
            default_cadence = 24
        elif type in ['4500']:
            query_args.append(jsoc.Series('aia.lev1_vis_1h')) 
            default_cadence = 3600
        else:
            raise ValueError("Need exact aia wavelength")
        
    elif instrument == 'hmi':
        if type in ['Ic_45s','Ld_45s','Lw_45s','M_45s','V_45s']:
            query_args.append(jsoc.Series('hmi.'+type))
            default_cadence = 45
        elif type in ['Ic_720s','Ld_720s','Lw_720s','M_720s','V_720s','S_720s']:
            query_args.append(jsoc.Series('hmi.'+type))
            default_cadence = 720
        else:
            raise ValueError("Need exact hmi series")
    else:
        raise ValueError("Neither aia or hmi")
         
    if cadence == 0:
        cadence = default_cadence
        
    query_args.append(jsoc.Notify(JSOC_REGISTERED_EMAIL))
    query_args.append(jsoc.Sample(cadence*units.s))
                
    client = jsoc.JSOCClient()
    res = client.query(*query_args)
    downloader = _URLFetch()
    if len(res) > 0:
        client.get(res,downloader=downloader,overwrite=True)
        
    return downloader.urls

def download():
    pass
