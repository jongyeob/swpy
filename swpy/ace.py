'''
Created on 2014. 9. 26.

@author: jongyeob
'''
import re
import sys
import logging

from swpy import utils
from swpy.utils import date_time as dt,\
                       download as dl,\
                       Config

DATA_DIR = 'data/'
LOG = logging.getLogger(__name__); LOG.setLevel(0)
PACKAGES = ''


INST_NAME = ['mag','swepam','sis','loc']
MAG_KEYS = ['datetime','status','bx','by','bz','bt','latitude','longitude']
SWEPAM_KEYS = ['datetime','status','density','speed','temperature']
SIS_KEYS = []
LOC_KEYS = []
INST_KEYS = [MAG_KEYS,SWEPAM_KEYS,SIS_KEYS,LOC_KEYS]


def initialize(config=Config()):
    global DATA_DIR,PACKAGES
    
    config.set_section(__name__)
    config.load_ns('DATA_DIR',globals())
    config.load_ns('PACKAGES',globals())
    
    LOG = utils.get_logger()
    for pkg in PACKAGES.split():
        utils.import_all(pkg, globals())
        

def empty_data(instrument):
    mag = {'datetime':[],'status':[],'bx':[],'by':[],'bz':[],'bt':[],'latitude':[],'longitude':[]}
    swepam = {'datetime':[],'status':[],'density':[],'speed':[],'temperature':[]}
    return [mag,swepam,None,None][INST_NAME.index(instrument)]
  
def check_instrument(data):
    '''
    Check data dictionary
    :param dict data: Input data
    :return:     (list) INST_NAME
    '''
    inst = INST_NAME[:]
    i = 0
    for keys in INST_KEYS:
        if len(keys) == 0:
            inst.remove(INST_NAME[i])
    
        
        for key in keys:
            if data.has_key(key)  == False:
                inst.remove(INST_NAME[i])
                break
                  
        i += 1
    
    return inst

    
def load(start_date,instrument,end_date=''):
    '''
    Load files of instrument (mag,swepam) of ACE realtime, from start datetime to end datetime
    
    :param string|datetime start_date: start date for searching
    :param string|datetime end_date: end date for searching
    :param string instrument: Instrument name [swepam,mag]
    :return: dictionary for instrument
    :rtype: dict
    ''' 
    start_dt = dt.parse(start_date)
    end_dt = start_dt 
    if end_date is not None:
        end_dt = dt.parse(end_date)
        
    data_total = empty_data(instrument)
    
    for t in dt.datetime_range(start_dt, end_dt, months=1):
        localfile = local_path(dt.tuples(t,'date'), instrument)
        
        try:
            data = load_file(localfile,instrument)
        except:
            LOG.error("Data can not read - %s"%(localfile))
            continue
        
        
        for i in range(len(data['datetime'])):
            if start_dt <= dt.parsing(data['datetime'][i]) <= end_dt:
                for key in data_total.keys():
                    data_total[key].append(data[key][i])
    
        
    return data_total

def load_file(filepath,instrument):    
    
    data = None
    
    if(instrument == 'mag'):
        data = load_mag(filepath)
    elif(instrument == 'swepam'):
        data = load_swepam(filepath)  
        
    return data

def load_mag(filepath):
    '''
    Load a file is magnetic parameters of 1hr averaged ACE realtime data
    :param string filepath: local filepath
    :return: (dict) mag data
    '''
    
    lines = []
    with open(filepath) as f:
        lines = f.readlines()
    
    
    mag = empty_data('mag')
    for line in lines:
                
###          
#         if mag['date'] is None:
#             date =  re.match(':Product: (\d+)_ace_(\S+)_1h.txt',line)
#             if(date is not None):
#                 mag['date'] = date.group(1)[:4]+'-'+date.group(1)[-2:]
#                 continue
###        
            
        data = re.match('\A(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\d+\s+\d+\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+',line)
                
        if(data is not None):
            datetime_string = "%4s-%02s-%02s"%data.groups()[0:3] + " %2s:%2s:00"%(data.group(4)[0:2],data.group(4)[2:4])
            mag['datetime'].append(datetime_string)
            
            i = 5
            for key in MAG_KEYS[1:]:
                mag[key].append(data.group(i))
                i = i + 1
            
  
    return mag
            
        
def load_swepam(filepath):
    '''
    Load a file is solar wind parameters of 1hr averaged ACE realtime data
    :param string filepath: local filepath
    :return: (dict) swepam data 
    '''
      
    lines = []
    with open(filepath) as f:
        lines = f.readlines()
    
    swepam = empty_data('swepam')
    for line in lines:

###    
#         if item['date'] is None:
#             date =  re.match(':Product: (\d+)_ace_(\S+)_1h.txt',line)
#             if(date is not None):
#                 item['date'] = date.group(1)[:4]+'-'+date.group(1)[-2:]
#                 continue
###
        
        data = re.match('\A(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\d+\s+\d+\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)',line)
        
        
        if(data is not None):
            datetime_string = "%4s-%2s-%2s"%data.groups()[0:3] + " %2s:%2s:00"%(data.group(4)[0:2],data.group(4)[2:4])
            swepam['datetime'].append(datetime_string)
            
            i = 5
            for key in SWEPAM_KEYS[1:]:
                swepam[key].append(data.group(i))
                i = i + 1
                

    return(swepam)

def local_path(date,inst):
    '''
    Return file path pattern string.
    :param tuple  date:   date
    :param string inst:   instrument name
    :return:              file path 
    '''
     
    yyyy,mm,_ = date
    localfile = DATA_DIR + 'ace_rt1h/%04d/%4d%02d_ace_%s_1h.txt'%(yyyy,yyyy,mm,inst)
    LOG.debug("local file : %s"%(localfile))
    
    return localfile

def remote_path(date,inst):
    host  = 'http://www.swpc.noaa.gov'
    loc       = '/ftpdir/lists/ace2'
    
    yyyy,mm,_ = date
    return host + loc + '/%4d%02d_ace_%s_1h.txt'%(yyyy,mm,inst)

def download_file(date,inst,filepath='',overwrite=False):
    '''
    Download ACE Realtime 1h average data.
    :param datetime date:         Datetime
    :param string   inst:         Instrument name
    :return:                      Downloaded path
    '''
    f = remote_path(dt.tuples(date, 'date'), inst)
        
    if filepath == '' :
        filepath =  local_path(date, inst)
        
    LOG.debug("Download start : %s"%(f))
    rv = dl.download_http_file(f, filepath,overwrite=overwrite)
    
    return rv

def download(start_date,instrument,end_date=None,overwrite=False):
    '''
    Download files of instrument of ACE realtime, from start_datetime to end_datetime
    
    :param string instrument: Instrument name [swepam,mag]
    :param string|datetime start_date: start date for searching
    :param string|datetime end_date: end date for searching
    
    :return: (list) file list
    '''
    start_dt = dt.parse(start_date)
    end_dt = start_dt
     
    if end_date is not None:
        end_dt = dt.parse(end_date)
        
    for t in dt.datetime_range(start_dt, end_dt, months=1):
        localfile = local_path(dt.tuples(t,'date'), instrument)
        
        try:
            rv = download_file(t, instrument, localfile,overwrite=overwrite)            
        except Exception as err:
            LOG.error(str(err))
            
        
        if rv == False:
            LOG.error("Download failed : %s"%(localfile))
            

if __name__ == '__main__':
    logging.basicConfig(level=0)
    from swpy.utils import data as da
    
    start = (2014,01,01)
    end = (2014,01,02)
    
    print  local_path(start, 'mag')
    print  local_path(start, 'mag')
    download(start, 'mag',end_date = end)
    download(start, 'swepam',end_date = end)
    
    print load(start,'mag',end_date=end)
    print load(start,'swepam',end_date=end)
