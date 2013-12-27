'''
Created on 2013. 10. 31.

@author: jongyeob
'''
import re
from swpy import data_dir
from swpy.utils import download as dl, swdt as dt


srs_dir = '/noaa/solar_region_summary'

def load_srs(filepath):
    
    text = []
    
    with open(filepath) as f:
        lines = f.readlines()
    
    name = ['NMBR','LOC','L0','AREA','Z','LL','NN','MAG']
    fmt = '(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)'
    total_var =  8
    
#    lines = text.splitlines()
    
#    root = dbms.new_dics('FILE',{'TYPE':'SRS'})
           
#    idx = 0
    item = {'date':'','regions':[] }
    
    for line in lines:
        region = {}
        
        if item['date'] == '':
            date =  re.match(':Issued: (\d+) (\S+) (\d+) 0030 UTC',line)
            if(date is not None):
                item['date'] = '%s-%02d-%s'%(date.group(1),dt.month_number[date.group(2)],date.group(3))
       
            
        data = re.match(fmt,line)
        if data is not None:
            
            for i in range(total_var):
                region[name[i]] = data.group(i+1)
 
            item['regions'].append(region)

    return item

def download_srs(date_t,filepath=None):
   
    f = srs_path_swpc(date_t)    
    r = dl.download(f,dst=filepath,overwrite=True)
    print(r.dst_path+'\n')
    
    return r.dst_path
                    

def srs_list_swpc(begindate_t,enddate_t): # Real data list
    ret_list = []
    
    for year_t in dt.datetime_range(begindate_t, enddate_t, dt.timedelta(days=365)):
        dir_str,_ = dl.path.split(srs_path_swpc(year_t))

        contents = dl.load_http_file(dir_str + '/')
        if contents is None:
            return ret_list
    
        list_files = dl.get_list_from_html(contents,'txt')
        
        for f in list_files:
            if begindate_t <= date_from_srs_fn(f) < enddate_t:
                ret_list.append(dir_str+'/'+f)
        
    return ret_list   
    

def srs_list_local(begindate_t,enddate_t): # Real data list
    
    pass

def srs_path_swpc(date_t): # File name string
    host  = 'http://www.swpc.noaa.gov'
    loc       = '/ftpdir/warehouse'
    
    yyyy,mm,dd = dt.date_tuple(date_t)
    
    filepath = '/%04d/SRS/%04d%02d%02dSRS.txt'%(yyyy,yyyy,mm,dd)
    path = host + loc+  filepath
    
    return path

def srs_path_local(date_t): # File name string
    
    yyyy,mm,dd = dt.date_tuple(date_t)
    filepath = '/%04d/%04d%02d%02dSRS.txt'%(yyyy,yyyy,mm,dd)
    
    path = data_dir + srs_dir + filepath
    
    return path
    
def date_from_srs_fn(filepath):
    filename_regex = '(\d{4})(\d{2})(\d{2})SRS.txt'
    res = re.search(filename_regex, filepath)
    year,month,day = [int(i) for i in res.groups()]
            
    return dt.datetime_t(year,month,day)

def loc(text):
    #print text
    rv = re.match("([NnSs])(\d+)([EeWw])(\d+)",text)
    
    if rv is None:
        return None
    
    data = rv.groups()
    
    lat = int(data[1])
    lon = int(data[3]) 
    if data[0].capitalize() == 'S':
        lat = -1*int(data[1])
    if data[2].capitalize() == 'E':
        lon = -1*int(data[3])
    
    return (lon,lat)
# test code
#ret = srs_list_swpc(dt.datetime_t(2013, 10, 1),dt.datetime_t(2013,10,5))
#print(dl.download(ret[0]))