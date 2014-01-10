'''
Created on 2013. 12. 18.

@author: jongyeob
'''
import swpy
from re import match

from utils.datetime import datetime_range, parsing
from noaa import download_sgas


SGAS_DIR = '/noaa/sgas'
DAYLY_INDICES_KEYS = ['10cm','ssn','3h_K_Boulder','3h_K_Planetary']

def loads(startdate):
    start_dt = parsing(startdate)
    
    filepath = swpy.data_dir+ SGAS_DIR + '/%s'%(start_dt.strftime("%Y/%Y%m%dSGAS.txt"))
    
    data = None
    try:
        data = load(filepath)
             
    except IOError as err:
        print err
        files = download_sgas(start_dt,start_dt)
        
        for afile in files:
            data = load(afile)
        
        
    return data
        
    
def load(filepath):
    
    with open(filepath) as f:
        contents = f.read()
    
    if len(contents) == 0:
        print ("File not exist!")
        return None
    
    #print contents
    
    
    fmt_daily_indices = "10 cm\s+(\d+)\s+SSN\s+(\d+)\s+Afr/Ap\s+(\d+)/(\d+)\s+X-ray Background\s+(\S+)"
    fmt_3hr_kindices = "Boulder\s+(.+)\s+Planetary\s+(.+)\s+"
    
     
    ee = energetic_events = {}
    
    pe = proton_events = {}
    
    di = daily_indices = {} 
    
    
    for line in contents.splitlines():
        print line
        record = match(fmt_daily_indices, line)
        if record != None:
            print record.groups()
            di['10cm'],di['ssn'],_,_,_=record.groups()            
        
        record = match(fmt_3hr_kindices,line)
        if record != None:
            print record.groups()
            di['3h_K_Boulder'],di['3h_K_Planetary']=record.groups()

            
    return energetic_events,proton_events,daily_indices
            