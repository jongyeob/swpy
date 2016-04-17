'''
Created on 2014. 9. 26.

@author: jongyeob
'''

from swpy import utils
from swpy.utils import date_time as dt, download as dl,filepath
import logging


LOG    = logging.getLogger(__name__)
DATETIME_REGEX = "%Y_%m_%d__%H_%M_%S_%f__\S+"
CADENCE = 45

def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)
            
def parse_time(path):
    return dt.parse_string(DATETIME_REGEX, path)
    
def get_path(type,datetime):
    '''
    return hmi jp2 url from nasa data server
    
    parameters:
        type : Ic, M
        datetime
    returns:
        path (string)
    '''
    from math import modf
    
    t = dt.parse(datetime)
     
    continuum_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,5,29,11,51,40.30)]
    magnetogram_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,05,29,11,39,40.30)]
     
     
    year,month,day,hour,miniute,second = dt.tuples(t,fsecond=True)
     
    host = "http://helioviewer.org"
     
    dirname = ''
     
    image_name = {'Ic':'continuum','M':'magnetogram'}
    image_string = image_name[type]
 
    if image_string == 'continuum':
        if continuum_start_time[0] <= t < continuum_start_time[1]:
            dirname = '/jp2/HMI/continuum/%4d/%02d/%02d'%(year,month,day)
        elif continuum_start_time[1] <= t:
            dirname = '/jp2/HMI/%4d/%02d/%02d/continuum'%(year,month,day)
    elif image_string == 'magnetogram':
        if magnetogram_start_time[0] <= t < magnetogram_start_time[1]:
            dirname = '/jp2/HMI/magnetogram/%4d/%02d/%02d'%(year,month,day)
        elif magnetogram_start_time[1] <= t:
            dirname = '/jp2/HMI/%4d/%02d/%02d/magnetogram'%(year,month,day)
    
     
    filename = None
    fsec,sec = modf(second)
    if int(round(fsec*1e3))%10 == 0 :
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e2),image_string)
    else:
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e3),image_string)
     
     
    return host + dirname + '/' + filename
    
def request(start_datetime,type,end_datetime='',cadence=0):
    '''
    retrieve files from nasa data server (jp2).

    returns: file path
    '''
            
    files = []
              
    start = dt.parse(start_datetime)
    end = start
    if end_datetime != '':
        end = dt.parse(end_datetime)
        
    if cadence == 0 : 
        cadence = CADENCE
        
    
    for t in dt.series(start, end, days=1):
        remote_path = get_path(type,t)
        dir_str,_ = filepath.path.split(remote_path)
     
        contents = dl.download_http_file(dir_str + '/',None)
        if contents == '':
            continue
     
        list_files = dl.get_list_from_html(contents,'jp2')
        records = dt.filter(list_files, start_datetime, end_datetime, cadence, time_parser=parse_time)
         
        files.extend([dir_str + '/' + f[0] for f in records])
           
    return files


