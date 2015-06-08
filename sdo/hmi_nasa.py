'''
Created on 2014. 9. 26.

@author: jongyeob
'''

from swpy.utils import date_time as dt, download as dl
import logging


LOG    = logging.getLogger(__name__)
DATETIME_REGEX = "%Y_%m_%d__%H_%M_%S_%f__\S+"
CADENCE = 45

def initialize(**kwargs):
    for key in kwargs:
        if globals().has_key(key) == True:
            globals()[key] = kwargs[key]
        else:
            raise KeyError(key)
            
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
        dir_str,_ = dl.path.split(remote_path)
     
        contents = dl.download_http_file(dir_str + '/',None)
        if contents == '':
            continue
     
        list_files = dl.get_list_from_html(contents,'jp2')
        records = dt.filter(list_files, start_datetime, end_datetime, cadence, time_parser=parse_time)
         
        files.extend([dir_str + '/' + f[0] for f in records])
           
    return files

    
# 
# import logging
# from swpy import utils
# from swpy.utils import date_time as dt,\
#                        download as dl,\
#                        Config
# 
# 
# LOG = utils.get_logger(__name__)
# LOG_LEVEL = logging.DEBUG
# DATA_DIR  = 'data/'
# HMI_M  = 'm'
# HMI_IC = 'ic'
# HMI_M_DIR = 'sdo/hmi/%(HMI_M)s/jp2/%Y/%Y%m%d/'
# HMI_IC_DIR = 'sdo/hmi/%(HMI_IC)s/jp2/%Y/%Y%m%d/'
# HMI_M_FILE =  '%Y%m%d_%H%M%S_sdo_hmi_%(HMI_M)s.jp2'
# HMI_IC_FILE =  '%Y%m%d_%H%M%S_sdo_hmi_%(HMI_IC)s.jp2'
# HMI_DATETIME_REGEX = '%Y%m%d_%H%M%S_\S+'
# PACKAGES    = 'hmi_jp2_kasi'
# 
# _list_inst = ['M','Ic']
# _remote_datetime_regex = "%Y_%m_%d__%H_%M_%S_%f__\S+"
# 
# def initialize(config=Config()):
#     global DATA_DIR,HMI_M_DIR,HMI_IC_DIR,HMI_M_FILE,HMI_IC_FILE,HMI_M,HMI_IC,LOG,LOG_LEVEL,PACKAGES
#     
#     
#     config.set_section(__name__)
#         
#     DATA_DIR         = config.load('DATA_DIR', DATA_DIR)
#     HMI_M            = config.load('HMI_M', HMI_M)
#     HMI_IC           = config.load('HMI_IC', HMI_IC)
#     HMI_M_DIR        = config.load('HMI_M_DIR', HMI_M_DIR)
#     HMI_M_FILE       = config.load('HMI_M_FILE', HMI_M_FILE)
#     HMI_IC_DIR       = config.load('HMI_IC_DIR', HMI_IC_DIR)
#     HMI_IC_FILE      = config.load('HMI_IC_FILE', HMI_IC_FILE)
#     LOG_LEVEL        = config.load('LOG_LEVEL', LOG_LEVEL)
#     PACKAGES         = config.load('PACKAGES',PACKAGES)
#     
#     LOG = utils.get_logger(__name__, int(LOG_LEVEL))
#     
#     for pkg in PACKAGES.split():
#         rv = utils.import_all(pkg,globals())
#         if rv == False:
#             LOG.error("Import failed : %s"%(pkg))
#        
# 
#     
# 
#          
#     
# def remote_datetime(path):
#     _,fn = utils.path.split(path)
#     return dt.parse_string(_remote_datetime_regex,fn)
# 
# def remote_path(datetime,image_string):
#     '''
#     return hmi jp2 url from nasa data server
#     :param datetime datetime obj
#     :param string image_string
#     '''
#     from math import modf
#     
#     t = dt.parse(datetime)
#     
#     
#     continuum_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,5,29,11,51,40.30)]
#     magnetogram_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,05,29,11,39,40.30)]
#     
#     #continuum_filename_changed_time = [dt.datetime_t(2010,12,7,16,44,41.00)]
#     #magnetogram_filename_changed_time = [dt.datetime_t(2010,12,7,16,37,11.00)]
#     
#     year,month,day,hour,miniute,second = dt.tuples(t,fsecond=True)
#     
#     host = "http://www2.helioviewer.org"
#     
#     dirname = ''
#     
#     image_name = {'IC':'continuum','M':'magnetogram'}
#     image_string = image_name[image_string.upper()]
# 
#     if image_string == 'continuum':
#         if continuum_start_time[0] <= t < continuum_start_time[1]:
#             dirname = '/jp2/HMI/continuum/%4d/%02d/%02d'%(year,month,day)
#         elif continuum_start_time[1] <= t:
#             dirname = '/jp2/HMI/%4d/%02d/%02d/continuum'%(year,month,day)
#     elif image_string == 'magnetogram':
#         if magnetogram_start_time[0] <= t < magnetogram_start_time[1]:
#             dirname = '/jp2/HMI/magnetogram/%4d/%02d/%02d'%(year,month,day)
#         elif magnetogram_start_time[1] <= t:
#             dirname = '/jp2/HMI/%4d/%02d/%02d/magnetogram'%(year,month,day)
#     else:
#         return None
#     
#     filename = None
#     fsec,sec = modf(second)
#     if int(round(fsec*1e3))%10 == 0 :
#         filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e2),image_string)
#     else:
#         filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e3),image_string)
#     
#     
#     return host + dirname + '/' + filename
# 
# def remote_list(start_datetime,end_datetime,image_string,iter_call=False):
#     '''
#     return files list from nasa data server (jp2)
#     :param bool it: iterator call
#     :return: list
#     '''
#     if iter_call == True:
#         return _remote_list(start_datetime,end_datetime,image_string)
#     
#     return [i for i in _remote_list(start_datetime, end_datetime, image_string)]
# 
# def _remote_list(start_datetime,end_datetime,image_string):
#     '''
#     retrieve files from nasa data server (jp2).
#     
#     :return: generator return
#     '''
#     
#     
#     start_datetime = dt.parse(start_datetime)
#     end_datetime = dt.parse(end_datetime)
#     
#     for t in dt.series(start_datetime, end_datetime, days=1):
#         dir_str,_ = dl.path.split(remote_path(t, image_string))
#     
#         contents = dl.download_http_file(dir_str + '/',None)
#         if contents == '':
#             continue
#     
#         list_files = dl.get_list_from_html(contents,'jp2')
#         #print "Found files : %d"%(len(list_files))
#         for f in list_files:
#             if start_datetime <= remote_datetime(f) <= end_datetime:     
#                 yield dir_str+'/'+f
#         
#         #print "End iteration"  
#           
#     return
#  

 
       
