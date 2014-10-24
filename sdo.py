'''
Created on 2013. 6. 19.

@author: kasi
'''
import logging
import math
import os
import re

import utils.date_time as dt
import utils.download as dl
import utils.utils as utl
from utils.config import Config 

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

HMI_IMAGES = ['magnetogram','continuum']
AIA_IMAGES = ['94','131','171','193','211','304','335','1600','1700','4500']
DATA_DIR = './data/'

def initialize():
    cnf = Config('swpy.ini',__name__)
    
    cnf.load('data_dir', DATA_DIR)
    
        
def download_hmi_jp2(start_datetime,end_datetime,image_string,threads=8):
    '''
    Downloads hmi jp2 files
    
    :param datetime start_datetime: start datetime
    :param datetime end_datetime: end datetime
    :param string image_string: continuum or magnetogram
    :return: downloaded file list
    '''
    
    dlist = []
    
       
    for f in hmi_jp2_iter_nasa(start_datetime, end_datetime,image_string):
     
        ft = get_datetime_nasa(f)
        if ft == None:
            LOG.error("Wrong file : %s"%(f))
            continue
    
        dst_filepath = DATA_DIR + hmi_jp2_path_local(ft,image_string)
        print("JP2 Path(local) : %s"%(dst_filepath))
                   
        rv = dl.download_http_file(f,dst_filepath)
                
        if rv == False:
            LOG.error("Download thread fail : %s->%s"%(f,dst_filepath))
            break
            
    return dlist    

def get_datetime_nasa(filename):
    filename_regex = "(\d+)_(\d+)_(\d+)__(\d+)_(\d+)_(\d+)_(\d+)__\S+"
    res = re.search(filename_regex, filename)
    if res == None:
        return None

    year,month,day,hour,minute,second,fsecond = [int(i) for i in res.groups()]
    second = second + (fsecond*1.)/10**len(str(fsecond))
    
    return dt.parsing(year,month,day,hour,minute,second)

def hmi_jp2_path_nasa(datetime,image_string):
    '''
    return hmi jp2 url from nasa data server
    :param datetime datetime_t : datetime
    :param string image_string : [continuum, magnetogram]
    '''
    t = dt.parse(datetime)
    
    continuum_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,5,29,11,51,40.30)]
    magnetogram_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,05,29,11,39,40.30)]
    
    #continuum_filename_changed_time = [dt.datetime_t(2010,12,7,16,44,41.00)]
    #magnetogram_filename_changed_time = [dt.datetime_t(2010,12,7,16,37,11.00)]
    
    year,month,day,hour,miniute,second = dt.tuples(t,fsecond=True)
    
    
    host = "http://helioviewer.nascom.nasa.gov"
    
    dirname = ''

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
    else:
        return None
    
    filename = None
    fsec,sec = math.modf(second)
    if int(round(fsec*1e3))%10 == 0 :
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e2),image_string)
    else:
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e3),image_string)
    
    
    return host + dirname + '/' + filename
       
    
def hmi_jp2_path_kasi():
    '''
    return hmi jp2 path from kasi data center
    NOT IMPLEMENTED
    '''
    pass

def get_datetime_local(filename):
    filename_regex = '(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{3})_\S+'
    res = re.search(filename_regex, filename)
    year,month,day,hour,minute,second,fsecond = [int(i) for i in res.groups()]
    
    return dt.datetime(year,month,day,hour,minute,second,int(fsecond*1e3))

def hmi_jp2_path_local(datetime_t,image_string):
    '''
    return local path
    '''
    year,month,day,hour,miniute,second,fsecond = dt.tuples(datetime_t) 
    
    #local_path = '/nasa/sdo/hmi/%s/%04d/%04d%02d%02d/jp2/%4d%02d%02d_%02d%02d%02d%03d_sdo_hmi_%s.jp2'\
    #For swpy-kasi : lib.sdo need override , import mechanism
    local_path = '/nasa/sdo/hmi/%s/jp2/%04d/%04d%02d%02d/%4d%02d%02d_%02d%02d%02d_sdo_hmi_%s.jp2'\
    %(image_string,year,year,month,day,year,month,day,hour,miniute,second,image_string)
    
    return local_path 
    

def hmi_jp2_iter_nasa(start_datetime,end_datetime,image_string):
    '''
    retrieve files from nasa data server (jp2).
    
    :return: generator return
    '''
    start_datetime = dt.parsing(start_datetime)
    end_datetime = dt.parsing(end_datetime)
    
    for t in dt.datetime_range(start_datetime, end_datetime, days=1):
        dir_str,_ = dl.path.split(hmi_jp2_path_nasa(t, image_string))
    
        contents = dl.download_http_file(dir_str + '/',None)
        if contents is False:
            continue
    
        list_files = dl.get_list_from_html(contents,'jp2')
        #print "Found files : %d"%(len(list_files))
        for f in list_files:
            if start_datetime <= get_datetime_nasa(f) <= end_datetime:     
                yield dir_str+'/'+f
        
        #print "End iteration"  
          
    return 
    
def hmi_jp2_list_nasa(start_datetime,end_datetime,image_string):
    '''
    return files list from nasa data server (jp2)
    :return: list
    '''
    return [i for i in hmi_jp2_iter_nasa(start_datetime, end_datetime, image_string)]

def hmi_jp2_iter_local(start_datetime,end_datetime,image_string,base_dir='.'):
    '''
    real filepaths from local
    :param datetime start_datetime: datetime
    :param datetime end_datetime: datetime
    :param string image_string: 'continuum'|'magnetogram'                
    :return: (generator) paths
    2013-12-30 / Jongyeob Park(pjystar@gmail.com)
                 New created
    '''

    for t in dt.series(start_datetime, end_datetime, days=1):
        
        dir_str,_ = dl.path.split(hmi_jp2_path_local(t, image_string))
    
        list_files = utl.get_files(base_dir + dir_str+'/*.jp2')
        for f in sorted(list_files):
            if start_datetime <= get_datetime_local(f) <= end_datetime:
                yield f
        
    return
    
    
def hmi_jp2_list_local(start_datetime,end_datetime,image_string,base_dir='.'):
    '''
    real filepaths from local
    :param datetime start_datetime: datetime
    :param datetime end_datetime: datetime
    :param string image_string: 'continuum'|'magnetogram'                
    :returns: (list) paths
    '''
    return [i for i in hmi_jp2_iter_local(start_datetime, end_datetime, image_string, base_dir)]
    

def hmi_jp2_list_kasi():
    '''
    Not implemented
    '''
    pass

