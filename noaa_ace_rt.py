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
 
def load_ace_rt1h_period(start_date,instrument,end_date=None):
    '''
    @summary:                 Load files of instrument (mag,swepam) of ACE realtime, from start datetime to end datetime
    @param start_date:    (String|Datetime) start date for searching
    @param end_date:      (String|datetime) end date for searching
    @param instrument:        (String) Instrument name [swepam,mag]
    @return:                  (dict) dictionary for instrument
    ''' 
    
    start_dt = dt.parsing(start_date)
    end_dt = start_dt 
    if end_date is not None:
        end_dt = dt.parsing(end_date)
        
    data_total = empty_data(instrument)
    
    for t in dt.datetime_range(start_dt, end_dt, months=1):
        localfile = data_dir + ace_rt1h_path_local(dt.tuples(t,'date'), instrument)
        print "local file : %s"%(localfile)
        
        try:
            data = load_ace_rt1h(localfile,instrument)
            
                
        except IOError as err:
            print err
            
            if download_ace_rt1h(t, instrument, localfile) == None:
                return None
            
            data = load_ace_rt1h(localfile,instrument)
            
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



def load_ace_rt1h(filepath,instrument):
    
    data = None
    if(instrument == 'mag'):
        data = load_ace_rt1h_mag(filepath)
    elif(instrument == 'swepam'):
        data = load_ace_rt1h_swepam(filepath)
    
    return data
def load_ace_rt1h_mag(filepath):
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
            
    print mag.keys()
    print zip(*mag.values())[0]
        
    return mag
            
        
def load_ace_rt1h_swepam(filepath):
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
                
            
            
    
    print swepam.keys()
    print zip(*swepam.values())[0]
    
    return(swepam)
        
    
def download_ace_rt1h(date,inst,filepath=None):
    '''
    @summary:     Download ACE Realtime 1h average data.
    @param date:  (datetime)    Datetime class
    @param inst:  (string)      Instrument name
    @return:      (string)      Downloaded path
    '''
    f = ace_rt1h_path_swpc(dt.tuples(date, 'date'), inst)
        
    if filepath is None :
        filepath =  data_dir + ace_rt1h_path_local(date, inst)
        
    dst_path = dl.download_url_file(f, filepath)
    
    return dst_path
    
def ace_rt1h_path_swpc(date,inst):
    host  = 'http://www.swpc.noaa.gov'
    loc       = '/ftpdir/lists/ace2'
    
    yyyy,mm,_ = date
    return host + loc + '/%4d%02d_ace_%s_1h.txt'%(yyyy,mm,inst)    

def ace_rt1h_path_local(date,inst):
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
