'''
Created on 2013. 6. 19.

@author: kasi
'''
from math import modf
import re

import utils as utl
import utils.datetime as dt
import utils.download as dl


hmi_images = ['magnetogram','continuum']
aia_images = ['94','131','171','193','211','304','335','1600','1700','4500']



def datetime_from_filename_nasa(filename):
    filename_regex = "(\d+)_(\d+)_(\d+)__(\d+)_(\d+)_(\d+)_(\d+)__\S+"
    res = re.search(filename_regex, filename)
    year,month,day,hour,minute,second,fsecond = [int(i) for i in res.groups()]
    second = second + (fsecond*1.)/10**len(str(fsecond))
    
    return dt.parsing(year,month,day,hour,minute,second)

def hmi_jp2_path_nasa(datetime,image_string):
    '''
    return hmi jp2 url from nasa data server
    @param datetime_t : datetime_info
    @param image_string : [continuum, magnetogram]
    @return: return string
    '''
    t = dt.parsing(datetime)
    
    continuum_start_time = [dt.parsing(2010,12,6,6,53,41.305),dt.parsing(2012,5,29,11,51,40.30)]
    magnetogram_start_time = [dt.parsing(2010,12,6,6,53,41.305),dt.parsing(2012,05,29,11,39,40.30)]
    
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
    fsec,sec = modf(second)
    if int(round(fsec*1e3))%10 == 0 :
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e2),image_string)
    else:
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,round(fsec*1e3),image_string)
    
    
    return host + dirname + '/' + filename
       
    
def hmi_jp2_path_kasi():
    '''
    @summary: return hmi jp2 path from kasi data center
    @note: NOT IMPLEMENTED
    '''
    pass

def datetime_from_filename_local(filename):
    filename_regex = '(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{3})_\S+'
    res = re.search(filename_regex, filename)
    year,month,day,hour,minute,second,fsecond = [int(i) for i in res.groups()]
    
    return dt.datetime(year,month,day,hour,minute,second,int(fsecond*1e3))

def hmi_jp2_path_local(datetime_t,image_string):
    '''
    @summary: return local path
    '''
    year,month,day,hour,miniute,second,fsecond = dt.tuples(datetime_t) 
    
    local_path = '/sdo/hmi/%s/%04d/%04d%02d%02d/jp2/%4d%02d%02d_%02d%02d%02d%03d_sdo_hmi_%s.jp2'\
    %(image_string,year,year,month,day,year,month,day,hour,miniute,second,fsecond*1e-3,image_string)
    
    return local_path 
    

def hmi_jp2_iter_nasa(start_datetime,end_datetime,image_string):
    '''
    summary: retrieve files from nasa data server (jp2).
    
    @return: generator return
    '''
    start_datetime = dt.parsing(start_datetime)
    end_datetime = dt.parsing(end_datetime)
    
    for t in dt.datetime_range(start_datetime, end_datetime, days=1):
        dir_str,_ = dl.path.split(hmi_jp2_path_nasa(t, image_string))
    
        contents = dl.load_http_file(dir_str + '/')
        if contents is None:
            continue
    
        list_files = dl.get_list_from_html(contents,'jp2')
        for f in list_files:
            if start_datetime <= datetime_from_filename_nasa(f) <= end_datetime:     
                yield dir_str+'/'+f
          
    return 
    
def hmi_jp2_list_nasa(start_datetime,end_datetime,image_string):
    '''
    @summary: return files list from nasa data server (jp2)
    @return: list
    '''
    return [i for i in hmi_jp2_iter_nasa(start_datetime, end_datetime, image_string)]

def hmi_jp2_iter_local(start_datetime,end_datetime,image_string,base_dir='.'):
    '''
    @summary:     real filepaths from local
    @param start_datetime:     datetime
    @param end_datetime:       datetime
    @param image_string:       'continuum'|'magnetogram'                
    @return :                 (generator) paths
    @change:      2013-12-30 / Jongyeob Park(pjystar@gmail.com)
                  New created
    '''

    for t in dt.datetime_range(start_datetime, end_datetime, days=1):
        
        dir_str,_ = dl.path.split(hmi_jp2_path_local(t, image_string))
    
        list_files = utl.get_files(base_dir + dir_str+'/*.jp2')
        for f in sorted(list_files):
            if start_datetime <= datetime_from_filename_local(f) <= end_datetime:
                yield f
        
    return
    
    
def hmi_jp2_list_local(start_datetime,end_datetime,image_string,base_dir='.'):
    '''
    @summary:     real filepaths from local
    @param start_datetime:     datetime
    @param end_datetime:       datetime
    @param image_string:       'continuum'|'magnetogram'                
    @return :                 (list) paths
    '''
    return [i for i in hmi_jp2_iter_local(start_datetime, end_datetime, image_string, base_dir)]
    

def hmi_jp2_list_kasi():
    '''
    '''
    pass

