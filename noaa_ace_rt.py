'''
Created on 2013. 11. 2.

@author: Daniel
'''
from swpy import data_dir
import sys


from utils import  download as dl
from utils import  datetime as dt

import re
from os.path import normpath
 
SRS_DIR = '/noaa/ace_realtime'
INST_NAME = ['mag','swepam','sis','loc']

MAG_KEYS = ['datetime','status','bx','by','bz','bt','latitude','longitude']
SWEPAM_KEYS = ['datetime','status','density','speed','temperature']
SIS_KEYS = []
LOC_KEYS = []
INST_KEYS = [MAG_KEYS,SWEPAM_KEYS,SIS_KEYS,LOC_KEYS]
  
def check_instrument(data):
    '''
    @summary     Check data dictionary
    @param data: Input data
    @return:     (list) INST_NAME
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
     
    pass


def empty_data(instrument):
    mag = {'datetime':[],'status':[],'bx':[],'by':[],'bz':[],'bt':[],'latitude':[],'longitude':[]}
    swepam = {'datetime':[],'status':[],'density':[],'speed':[],'temperature':[]}
    return [mag,swepam,None,None][INST_NAME.index(instrument)]

def download(start_date,instrument,end_date=None):
    '''
    Download files of instrument of ACE realtime, from start_datetime to end_datetime
    
    :param string|datetime start_date: start date for searching
    :param string|datetime end_date: end date for searching
    :param string instrument: Instrument name [swepam,mag]
    :return: file list
    :rtype: list
    '''
    start_dt = dt.parsing(start_date)
    end_dt = start_dt
    
    files = [] 
    if end_date is not None:
        end_dt = dt.parsing(end_date)
        
    for t in dt.datetime_range(start_dt, end_dt, months=1):
        localfile = data_dir + path_local(dt.tuples(t,'date'), instrument)
        print "local file : %s"%(localfile)
        try:
            afile = download_file(t, instrument, localfile)            
        except Exception as err:
            print err
            return None
        
        files.append(afile)
        
    return files
    
def load(start_date,instrument,end_date=None):
    '''
    Load files of instrument (mag,swepam) of ACE realtime, from start datetime to end datetime
    
    :param string|datetime start_date: start date for searching
    :param string|datetime end_date: end date for searching
    :param string instrument: Instrument name [swepam,mag]
    :return: dictionary for instrument
    :rtype: dict
    ''' 
    
    start_dt = dt.parsing(start_date)
    end_dt = start_dt 
    if end_date is not None:
        end_dt = dt.parsing(end_date)
        
    data_total = empty_data(instrument)
    
    for t in dt.datetime_range(start_dt, end_dt, months=1):
        localfile = data_dir + path_local(dt.tuples(t,'date'), instrument)
        print "local file : %s"%(localfile)
        
        try:
            data = load_file(localfile,instrument)
            
                
        except IOError as err:
            print err
            
            if download_file(t, instrument, localfile) == None:
                return None
            
            data = load_file(localfile,instrument)
            
        except Exception as err:
            print err
            return None
        
        if data is None:
            return None
        
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
    @summary: Load a file is magnetic parameters of 1hr averaged ACE realtime data
    @param filepath: (string) local filepath
    @return: (dict) mag dictionary
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
    @summary:          Load a file is solar wind parameters of 1hr averaged ACE realtime data
    @param filepath:   (string) local filepath
    @return:           (dict) swepam dictionary
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
        
    
def download_file(date,inst,filepath=None):
    '''
    @summary:     Download ACE Realtime 1h average data.
    @param date:  (datetime)    Datetime class
    @param inst:  (string)      Instrument name
    @return:      (string)      Downloaded path
    '''
    f = path_swpc(dt.tuples(date, 'date'), inst)
        
    if filepath is None :
        filepath =  data_dir + path_local(date, inst)
        
    dst_path = dl.download_url_file(f, filepath,overwrite=True)
    
    return dst_path
    
def path_swpc(date,inst):
    host  = 'http://www.swpc.noaa.gov'
    loc       = '/ftpdir/lists/ace2'
    
    yyyy,mm,_ = date
    return host + loc + '/%4d%02d_ace_%s_1h.txt'%(yyyy,mm,inst)    

def path_local(date,inst):
    '''
    @summary:     Return file path pattern string.
    @param date:  (tuple)    date
    @param inst:  (string)   instrument name
    @return:      (string)   file path 
    ''' 
    yyyy,mm,_ = date
    return normpath('/ace_rt1h/%04d/%4d%02d_ace_%s_1h.txt'%(yyyy,yyyy,mm,inst))
       
def date_from_filename():    
    pass
