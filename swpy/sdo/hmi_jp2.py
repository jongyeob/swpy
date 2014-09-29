'''
Created on 2014. 9. 26.

@author: jongyeob
'''
import logging
from swpy import utils
from swpy.utils import date_time as dt,\
                       download as dl,\
                       Config


LOG = utils.get_logger(__name__)
LOG_LEVEL = logging.DEBUG
DATA_DIR  = 'data/'
HMI_M  = 'm'
HMI_IC = 'ic'
HMI_M_DIR = 'sdo/hmi/%(HMI_M)s/jp2/%Y/%Y%m%d/'
HMI_IC_DIR = 'sdo/hmi/%(HMI_IC)s/jp2/%Y/%Y%m%d/'
HMI_M_FILE =  '%Y%m%d_%H%M%S_sdo_hmi_%(HMI_M)s.jp2'
HMI_IC_FILE =  '%Y%m%d_%H%M%S_sdo_hmi_%(HMI_IC)s.jp2'
HMI_DATETIME_REGEX = '%Y%m%d_%H%M%S_\S+'
PACKAGES    = 'hmi_jp2_kasi'

_list_inst = ['M','Ic']
_remote_datetime_regex = "%Y_%m_%d__%H_%M_%S_%f__\S+"

def initialize(config=Config()):
    global DATA_DIR,HMI_M_DIR,HMI_IC_DIR,HMI_M_FILE,HMI_IC_FILE,HMI_M,HMI_IC,LOG,LOG_LEVEL,PACKAGES
    
    
    config.set_section(__name__)
        
    DATA_DIR         = config.load('DATA_DIR', DATA_DIR)
    HMI_M            = config.load('HMI_M', HMI_M)
    HMI_IC           = config.load('HMI_IC', HMI_IC)
    HMI_M_DIR        = config.load('HMI_M_DIR', HMI_M_DIR)
    HMI_M_FILE       = config.load('HMI_M_FILE', HMI_M_FILE)
    HMI_IC_DIR       = config.load('HMI_IC_DIR', HMI_IC_DIR)
    HMI_IC_FILE      = config.load('HMI_IC_FILE', HMI_IC_FILE)
    LOG_LEVEL        = config.load('LOG_LEVEL', LOG_LEVEL)
    PACKAGES         = config.load('PACKAGES',PACKAGES)
    
    LOG = utils.get_logger(__name__, int(LOG_LEVEL))
    
    for pkg in PACKAGES.split():
        rv = utils.import_all(pkg,globals())
        if rv == False:
            LOG.error("Import failed : %s"%(pkg))
       

    
def local_path(datetime_t,image_string):
    '''
    return local path
    '''
    datetime_t = dt.parse(datetime_t)
    
    path = ''
    if image_string.upper() == 'M':
        path = DATA_DIR + HMI_M_DIR + HMI_M_FILE
    elif image_string.upper() == 'IC':
        path = DATA_DIR + HMI_IC_DIR + HMI_IC_FILE
    else:
        raise ValueError
    
    path = dt.replace(path,datetime_t,kw={'HMI_M':HMI_M,'HMI_IC':HMI_IC})
              
    return path

def local_datetime(path):
    _,fn = utils.path.split(path)
    return dt.parse_string(HMI_DATETIME_REGEX,fn)

def local_list(start_datetime,end_datetime,image_string,iter_call=False):
    '''
    real filepaths from local
    '''
    if iter_call == True:
        return _local_list(start_datetime,end_datetime,image_string)
    
    return [i for i in _local_list(start_datetime, end_datetime, image_string)]    
 
 
def _local_list(start_datetime,end_datetime,image_string):
    '''
    real filepaths from local
    :param datetime start_datetime: datetime
    :param datetime end_datetime: datetime
    :param string image_string: 'M | Ic'                
    :return: (generator) paths
    2013-12-30 / Jongyeob Park(pjystar@gmail.com)
                 New created
    '''
    
    fmt = ''
    if image_string.upper() == 'M':
        fmt = HMI_M_FILE
    elif image_string.upper() == "IC":
        fmt = HMI_IC_FILE
    else:
        raise ValueError
    
    start  = dt.parse(start_datetime)
    end    = dt.parse(end_datetime) 
    for t in dt.series(start, end, days=1):
         
        dir_str = dl.path.dirname(local_path(t, image_string))
     
        list_files = utils.get_files(dir_str+'/*.jp2')
        for f in sorted(list_files):
            if start <= dt.parse_string(fmt,f) <= end:
                yield f
         
    
def remote_datetime(path):
    _,fn = utils.path.split(path)
    return dt.parse_string(_remote_datetime_regex,fn)

def remote_path(datetime,image_string):
    '''
    return hmi jp2 url from nasa data server
    :param datetime datetime obj
    :param string image_string
    '''
    from math import modf
    
    t = dt.parse(datetime)
    
    
    continuum_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,5,29,11,51,40.30)]
    magnetogram_start_time = [dt.parse(2010,12,6,6,53,41.305),dt.parse(2012,05,29,11,39,40.30)]
    
    #continuum_filename_changed_time = [dt.datetime_t(2010,12,7,16,44,41.00)]
    #magnetogram_filename_changed_time = [dt.datetime_t(2010,12,7,16,37,11.00)]
    
    year,month,day,hour,miniute,second = dt.tuples(t,fsecond=True)
    
    host = "http://www2.helioviewer.org"
    
    dirname = ''
    
    image_name = {'IC':'continuum','M':'magnetogram'}
    image_string = image_name[image_string.upper()]

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
    fsec,sec = modf(second)
    if int(round(fsec*1e3))%10 == 0 :
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e2),image_string)
    else:
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e3),image_string)
    
    
    return host + dirname + '/' + filename

def remote_list(start_datetime,end_datetime,image_string,iter_call=False):
    '''
    return files list from nasa data server (jp2)
    :param bool it: iterator call
    :return: list
    '''
    if iter_call == True:
        return _remote_list(start_datetime,end_datetime,image_string)
    
    return [i for i in _remote_list(start_datetime, end_datetime, image_string)]

def _remote_list(start_datetime,end_datetime,image_string):
    '''
    retrieve files from nasa data server (jp2).
    
    :return: generator return
    '''
    
    
    start_datetime = dt.parse(start_datetime)
    end_datetime = dt.parse(end_datetime)
    
    for t in dt.series(start_datetime, end_datetime, days=1):
        dir_str,_ = dl.path.split(remote_path(t, image_string))
    
        contents = dl.download_http_file(dir_str + '/',None)
        if contents == '':
            continue
    
        list_files = dl.get_list_from_html(contents,'jp2')
        #print "Found files : %d"%(len(list_files))
        for f in list_files:
            if start_datetime <= remote_datetime(f) <= end_datetime:     
                yield dir_str+'/'+f
        
        #print "End iteration"  
          
    return
 
def download(start_datetime,end_datetime,image_string):
    '''
    Downloads hmi jp2 files
     
    :param datetime start_datetime: start datetime
    :param datetime end_datetime: end datetime
    :param string image_string: continuum or magnetogram
    '''
            
    for f in remote_list(start_datetime, end_datetime,image_string,iter_call=True):
  
        ft = remote_datetime(f)
        if ft == None:
            LOG.error("Wrong file : %s"%(f))
            continue
 
        dst_filepath = local_path(ft,image_string)
        LOG.debug("JP2 Path(local) : %s"%(dst_filepath))
                
    
        rv = dl.download_http_file(f,dst_filepath)
        if rv == False:
            LOG.error("Download fail : %s->%s"%(f,dst_filepath))
            continue
 
       
    
if __name__ == '__main__':
    initialize()
    logging.basicConfig()
         
    print local_path(dt.parse("20140323"),'M')
    print local_list("20140323", "20140324", 'M')
    
    
    
    print remote_path("2010-10-31 00:02:00.101", 'Ic')
    print remote_path("2010-10-31 00:02:00.10", 'Ic')
    print len(remote_list("20121003","20121005","Ic"))
    
    download("20121003","20121005",'Ic')