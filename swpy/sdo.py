'''
Created on 2013. 6. 19.

@author: kasi
'''
from math import modf
import utils.swdt as dt
import utils.download as dl
import re


hmi_images = ['magnetogram','continuum']
def datetime_from_filename_lmsal(filename):
    filename_regex = "(\d+)_(\d+)_(\d+)__(\d+)_(\d+)_(\d+)_(\d+)__\S+"
    res = re.search(filename_regex, filename)
    year,month,day,hour,minute,second,fsecond = [int(i) for i in res.groups()]
    second = second + (fsecond*1.)/10**len(str(fsecond))
    
    return dt.datetime_t(year,month,day,hour,minute,second)

def hmi_jp2_path_lmsal(datetime_t,image_string):
    #
    # datetime_t : datetime structure
    # image_string : 'continuum', 'magnetogram'
    
    
    continuum_start_time = [dt.datetime_t(2010,12,6,6,53,41.305),dt.datetime_t(2012,5,29,11,51,40.30)]
    magnetogram_start_time = [dt.datetime_t(2010,12,6,6,53,41.305),dt.datetime_t(2012,05,29,11,39,40.30)]
    
    #continuum_filename_changed_time = [dt.datetime_t(2010,12,7,16,44,41.00)]
    #magnetogram_filename_changed_time = [dt.datetime_t(2010,12,7,16,37,11.00)]
    
    year,month,day,hour,miniute,second = dt.datetime_tuple(datetime_t)
    
    
    host = "http://helioviewer.nascom.nasa.gov"
    
    dirname = ''
    print continuum_start_time
    print magnetogram_start_time
    print datetime_t
    if image_string == 'continuum':
        if continuum_start_time[0] <= datetime_t < continuum_start_time[1]:
            dirname = '/jp2/HMI/continuum/%4d/%02d/%02d'%(year,month,day)
        elif continuum_start_time[1] <= datetime_t:
            dirname = '/jp2/HMI/%4d/%02d/%02d/continuum'%(year,month,day)
    elif image_string == 'magnetogram':
        if magnetogram_start_time[0] <= datetime_t < magnetogram_start_time[1]:
            dirname = '/jp2/HMI/magnetogram/%4d/%02d/%02d'%(year,month,day)
        elif magnetogram_start_time[1] <= datetime_t:
            dirname = '/jp2/HMI/%4d/%02d/%02d/magnetogram'%(year,month,day)
    else:
        return None
    
    filename = None
    fsec,sec = modf(second)
    if (fsec*1e3)%10 == 0 :
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,fsec*1e3,image_string)
    else:
        filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,fsec*1e3,image_string)

#    if image_string is 'continuum':
#        if continuum_filename_changed_time[0] <= datetime_t:
#            filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,fsec*1e3,image_string)
#        else:
#            filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,fsec*1e2,image_string)
#    elif image_string is 'magnetogram':
#        if magnetogram_filename_changed_time[0] <= datetime_t:
#            filename = "%4d_%02d_%02d__%02d_%02d_%02d_%02d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,fsec*1e3,image_string)
#        else:
#            filename = "%4d_%02d_%02d__%02d_%02d_%02d_%03d__SDO_HMI_HMI_%s.jp2"%(year,month,day,hour,miniute,sec,fsec*1e2,image_string)
#    else:
#        return None
    
    
    
    return host + dirname + '/' + filename
       
    
def hmi_jp2_path_kasi():
    pass

def hmi_jp2_path_local(datetime_t,image_string):

    
    year,month,day,hour,miniute,second = dt.datetime_tuple(datetime_t) 
    
    fsec,sec = modf(second)
    local_path = '/sdo/hmi/%s/%04d/%04d%02d/%04d%02d%02d/sdo_hmi_%s_%4d_%02d_%02d_%02d_%02d_%02d_%03d.jp2'\
    %(image_string,year,year,month,year,month,day,image_string,year,month,day,hour,miniute,sec,round(fsec,4)*1e3)
    
    
    return local_path 
    

def hmi_jp2_list_lmsal(start_datetime_t,end_datetime_t,image_string):
    
    ret_list = []
    for datetime_t in dt.datetime_range(start_datetime_t, end_datetime_t, dt.timedelta(1)):
        dir_str,_ = dl.path.split(hmi_jp2_path_lmsal(datetime_t, image_string))
    
        
        contents = dl.load_http_file(dir_str + '/')
        list_files = dl.get_list_from_html(contents,'jp2')
        for f in list_files:
            if start_datetime_t <= datetime_from_filename_lmsal(f) <= end_datetime_t:
                ret_list.append(dir_str+'/'+f)
    
    return ret_list
    

def hmi_jp2_list_kasi():
    
    pass
