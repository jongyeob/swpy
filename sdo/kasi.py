'''
HMI FITS at KASI

Created by Jongyeob (parkjy@kasi.re.kr)
'''

from swpy import utils
from swpy.utils import date_time as dt, download as dl
import logging

LOG    = logging.getLogger(__name__)

META_DIR = 'http://metadata.kasi.re.kr/metadata/nasa/sdo/$(format)/$(instrument)/$(type)/%Y/'
META_FILE = '%Y%m%d_$(format)_$(type).txt'
DATA_HOST = 'http://swc4.kasi.re.kr'

TYPES = ['Ic_45s','Ld_45s','Lw_45s','M_45s','V_45s','Ic_720s','Ld_720s','Lw_720s','M_720s','S_720s']

def initialize(**kwargs):
    for key in kwargs:
        if globals().has_key(key) == True:
            globals()[key] = kwargs[key]
        else:
            raise KeyError(key)
            
def request(format,instrument,type,start_datetime,end_datetime='',cadence=0,**kwargs):
    '''
    format : fits  jp2  jpg
    instrument : aia  hmi
    type : fits|jp2|jpg;aia = 131  1600  1700  171  193  211  304  335  4500  94 
           jp2;hmi  = continuum  magnetogram
           jpg;hmi  = Ic  Ic_flat  M  M_color
           fits;hmi = Ic_45s   Ld_45s   Lw_45s   M_45s   V_45s   
                      Ic_720s  Ld_720s  Lw_720s  M_720s  V_720s  S_720s
    jpg_size : default = 1024
               aia = 512 1024 2048
               hmi = 512 1024 2048 4096     
    '''
    jpg_size_text = ''
    replaced_text = ''
    if   format == 'fits' : replaced_text = '/NAS/emc01'
    elif format == 'jp2' and instrument == 'aia' : replaced_text = '/NAS/hp01'
    elif format == 'jp2' and instrument == 'hmi' : replaced_text = '/NAS/hp03'
    elif format == 'jpg'  : 
        replaced_text = '/NAS/hp02'
        jpg_size_text = '_'+str(kwargs['jpg_size'])
        
    
    assert replaced_text != '', 'Keywords wrong'
    
    meta_time_list = dt.series(start_datetime,end_datetime,days=1)
    records = []
    for t in meta_time_list:
        url = dt.replace(META_DIR + META_FILE,t,instrument=instrument,format=format,type=type)
        LOG.debug(url)
        url = url[:-4] + jpg_size_text + url[-4:]
            
        list = dl.download_http_file(url)
        for line in list.split('\n'):
            if len(line) > 0:
                records.append(line.split())
      
    
    LOG.debug('Number of records : %d'%(len(records)))
    
    urls = []
    records = dt.filter(records, start_datetime, end_datetime, cadence,**kwargs)
    for r in records:
        data_path = r[1].replace(replaced_text,'')
        data_url = DATA_HOST + data_path  
        
        urls.append(data_url)
        
    
    return urls
    
# def request_fits(start_datetime,end_datetime='',cadence=0,**kwargs):
#     
#     type = kwargs['type']
#     
#     meta_time_list = dt.series(start_datetime,end_datetime,days=1)
#     records = []
#     for t in meta_time_list:
#         url = dt.replace(META_DIR + META_FILE,t,instrument='hmi',format='fits',type=type)
#         LOG.debug(url)
#         
#         list = dl.download_http_file(url)
#         for line in list.split('\n'):
#             if len(line) > 0:
#                 records.append(line.split())
#       
#     
#     LOG.debug('Number of records : %d'%(len(records)))
#     
#     urls = []
#     records = dt.filter(records, start_datetime, end_datetime, cadence)
#     for r in records:
#         data_path = r[1].replace('/NAS/emc01','')
#         data_url = DATA_HOST + data_path  
#         
#         urls.append(data_url)
#         
#     
#     return urls
    
        
        
        

    
    
    
    
    