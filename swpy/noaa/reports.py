import os
import re
import shutil
from swpy import utils 
from swpy.utils import config
from swpy.utils import datetime as dt
from swpy.utils import download as dl, data as da
from swpy.utils import filepath
import tarfile
import tempfile


DATA_DIR  = 'data/noaa/reports/%(suffix)/%Y/'
DATA_FILE = '%Y%m%d_%(suffix).txt'


LOG = utils.get_logger(__name__)

EVENTS_KEYS = ['date','event:no','event:flag','begin:flag','begin:time',\
               'max:flag','max:time','end:flag','end:time','obs','quality',\
               'type','loc/frq','property:1','property:2','region']
SRS_KEYS = ['date','nmbr','loc','l0','area','z','ll','nn','mag']


_FIRST_DATA = {'events':dt.parse(1996,07,31),\
               'SRS':dt.parse(1996,02,01)}



def initialize(**kwargs):
    config.set(globals(),**kwargs)

def get_path(suffix,date=None):
    return dt.replace(DATA_DIR + DATA_FILE,date,suffix=suffix)
    
def request(suffix,begin='',end=''):
    
    path = get_path(suffix)
    files = filepath.request_files(path, begin, end_datetime=end)
    
    return files
    
   
def download_events(begin, end="",overwrite=False):
    begin = dt.parse(begin)
    if begin < _FIRST_DATA['events']:
        begin = _FIRST_DATA['events']

    _download_template("events", begin, end,overwrite)
    

def download_srs(begin, end="",overwrite=False):
    begin = dt.parse(begin)
    if begin < _FIRST_DATA['SRS']:
        begin = _FIRST_DATA['SRS']
    
    _download_template("SRS", begin, end,overwrite)
    

def download_sgas(begin, end="",overwrite=False):
    _download_template("SGAS", begin, end,overwrite)
    

def download_rsga(begin, end="",overwrite=False):
    _download_template("RSGA", begin, end,overwrite)
    

def download_geoa(begin, end="",overwrite=False):
    _download_template("GEOA", begin, end,overwrite)
    


def load_events(begin,end=''):
    
    begin_dt = dt.trim(begin,3,'start')
    if begin_dt < _FIRST_DATA['events']:
        begin_dt = _FIRST_DATA['events']
    
    if end == '':
        end = begin
        
    end_dt = dt.trim(end,3,'end')
    
    vl = []
    
    for t in dt.series(begin_dt, end_dt, days=1):
             
        file_path = get_path('events',t)
        
        if not os.path.exists(file_path):
            LOG.info("File is not exist. %s",file_path)
            continue
        
        with open(file_path,'rt') as fr:
            lines = fr.readlines()
            
        for line in lines:
            
            if ':#'.find(line[0]) != -1:
                continue
            
            v  = ['' for _ in range(16)]
                          
            
            try:
                v[0] = str(t.date())
                v[1] = int(line[0:4].replace(' ',''))
                v[2] = line[5]
                
                v[3] = line[10]
                strt = dt.parse_string("%H%M", line[11:15])
                if strt == None:    strt = ''
                else :    strt = str(strt.time())
                v[4] = strt
                
                v[5] = line[17]
                strt = dt.parse_string("%H%M", line[18:22])
                if strt == None:    strt = ''
                else :    strt = str(strt.time())
                v[6] = strt
                
                v[7] = line[27]
                strt = dt.parse_string("%H%M", line[28:32])
                if strt == None:    strt = ''
                else :    strt = str(strt.time())
                v[8] = strt
                
                v[9] = line[34:38].replace(' ','')
                v[10] = line[39]
                v[11] = line[43:47].replace(' ','')
                v[12] = line[47:58].replace(' ' ,'')
                
                i = 0      
                for l in line[58:76].split():
                    v[13+i] = l
                    i       += 1
                    
                v[15] = line[76:80]
                
            except:
                continue

            vl.append(v)
            
        
    return vl   

def load_srs(begin,end=''):
    
    begin_dt = dt.trim(begin,3,'start')
    if end == '':
        end = begin
        
    end_dt = dt.trim(end,3,'end')
        
    fmt = re.compile('(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)')
    
    
    data = []
    
    for now in dt.series(begin_dt, end_dt,days=1):
        filepath = get_path('SRS', now)
                
                
        text = ''
        if os.path.exists(filepath) == False:
            LOG.warn("File is not exist - %s"%(filepath))
            continue
        
        with open(filepath,'rt') as f:
            text = f.read()
             
        
        for line in text.splitlines():
            match = re.match(fmt,line)
            
            if match:
                row = [now.strftime('%Y%m%d')]
                for _m in match.groups():
                    row.append(_m)
                    
                data.append(row)
     

    return data 
    
def _download_template(suffix, begin, end="",overwrite=False):
    
    if end == "":
        end = begin
        
    begin_dt, end_dt = dt.trim(begin,3,'start'), dt.trim(end,3,'end')
            
    host = 'ftp://ftp.swpc.noaa.gov/'
    src_dir  = "pub/warehouse/%Y/"
    src_dir2 = "%(suffix)/"
    txt_file = '%Y%m%d%(suffix).txt'
    tar_file = "%Y_%(suffix).tar.gz" 
    
    for now_dt in dt.datetime_range(begin_dt, end_dt, days=1):
        _suffix   = suffix
        _src_dir  = src_dir
        _src_dir2 = src_dir2
        _txt_file = txt_file
        _tar_file = tar_file 
        
        if suffix == 'events':
            _src_dir  = dt.replace(src_dir,now_dt)
            _src_dir2 = dt.replace(src_dir2,\
                                  suffix="{year}_{suffix}".format(year=now_dt.year,suffix=suffix))
        
        if suffix in ('SRS','GEOA','RSGA','SGAS') and now_dt.year in (2006,2007):
            _tar_file = '%s.tar.gz'%(suffix)
            
            
        src_path = dt.replace(host + _src_dir + _src_dir2 + _txt_file, now_dt, suffix=_suffix)
        tar_path = dt.replace(host + _src_dir + _tar_file, now_dt, suffix=_suffix)  
        dst_path = get_path(suffix,now_dt)
        
        filepath.make_path(dst_path)
        
        rv = dl.download_ftp_file(src_path, dst_path ,overwrite=overwrite)
        if rv == False:
            tmp_dir = tempfile.mkdtemp()
             
            dst_tarpath = tempfile.mktemp(dir=tmp_dir) 
            rv =  dl.download_ftp_file(tar_path,dst_tarpath)
            if rv == False:
                LOG.info("No tar... %s"%(tar_path))
                continue
            
            
            with tarfile.open(dst_tarpath, 'r:gz') as tf:
                tf.extractall(tmp_dir)
                
            for filepath in filepath.get_files(tmp_dir+'/*.txt'):
                fmt  = dt.replace(_txt_file,suffix=_suffix)
                _,filename = os.path.split(filepath)
                time = dt.parse_string(fmt,filename)              
                dst_path = get_path(suffix,time)
                
                filepath.make_path(dst_path)
                if os.path.exists(dst_path) == True and overwrite == True:
                    continue
                                        
                shutil.copyfile(filepath, dst_path)
        
            # Remove a temp directory and a temp file.
            shutil.rmtree(tmp_dir)
