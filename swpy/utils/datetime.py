'''
Created on 2013. 5. 7.

@author: kasi
'''

from __future__ import absolute_import

from calendar import monthrange
from datetime import datetime, timedelta,date,time

import logging
import threading

import re

MONTH_NUMBERS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
RE_FORMATS = {'%Y': '(?P<Y>\d{4})',
              '%y': '(?P<y>\d{2})',
              '%m': '(?P<m>\d{1,2})',
              '%d': '(?P<d>\d{1,2})',
              '%H': '(?P<H>\d{1,2})',
              '%M': '(?P<M>\d{1,2})',
              '%S': '(?P<S>\d{1,2})',
              '%f': '(?P<f>\d{1,6})',
              '%b': '(?P<b>[a-zA-Z]+)',
                   }
DATE_FORMATS = [ "%Y-%m-%d","%d-%b-%Y","%d-%b-%y"]
TIME_FORMATS = [ "%H:%M:%S\.%f","%H:%M:%S"]
SEPS = ['_',' ','T']
DATE_SEPS = ['','_',' ']
TIME_SEPS = ['','_',' ']

LOG = logging.getLogger(__name__)

NYEAR = 1; NMONTH = 2; NWEEK =3; NDAY = 3; NHOUR = 4; NMINUTE = 5; NSECOND = 6; NSECOND2 = 7

lock_parsing = threading.Lock()

def parse_string(datetime_string,index=False):
    '''
    parsing datetime string

    :param str datetime_string: string of datetime
    :return: Datetime|None
    '''
    
    
    
    parsed_date = None
    parsed_time = None   
    
    time_offset = 0
    date_start,date_end = 0,len(datetime_string)
    time_start, time_end = 0,len(datetime_string)
    
    # date searching
    lock_parsing.acquire()
    for fmt in DATE_FORMATS:
        f = fmt
        for k,v in RE_FORMATS.iteritems():
            f = f.replace(k,v)
        fs = f
        for sep in DATE_SEPS:
                            
            r = re.search(fs, datetime_string)
            
            fs = f.replace('-',sep)
            if r is None: continue
            
            parsed_date = date(*[int(s) for s in r.groups()])
            date_start,date_end = r.start(),r.end()
            LOG.debug('Find date : ',parsed_date,' with ',  fs,'[%d:%d]'%(r.start(),r.end()))
            
            try:
                SEPS.index(datetime_string[r.end()])
                time_offset= r.end() + 1

            except:
                #print 'Not Find Time ',datetime_string[r.end():]
                time_offset= len(datetime_string)
                
            break
        
        if parsed_date is not None: break
                    
    # time searching        
    for fmt in TIME_FORMATS:
        f = fmt
        for k,v in RE_FORMATS.iteritems():
            f = f.replace(k,v)
        fs = f
        for sep in TIME_SEPS:
            if parsed_date is not None: fs = '^'+fs # excact match when date is parsed
            
            r = re.search(fs, datetime_string[time_offset:])
            
            fs = f.replace(':',sep)
            if r is None: continue
    
                
            parsed_time = time(*[int(s) for s in r.groups()])
            
            d = r.groupdict()
            if d.has_key('f') == True:
                parsed_time  = parsed_time.replace(microsecond=int(d['f'].ljust(6,'0')))
        
                
            time_start,time_end = r.start(),r.end()
            LOG.debug('Find time : ',parsed_time,' with ',  fs,'[%d:%d]'%(r.start(),r.end()))
            
            break
        
        if parsed_time is not None: break
    lock_parsing.release()
    
    ret = []
           
    parsed = None
    start,end = 0, 0
    if parsed_date is not None and parsed_time is not None:
        parsed = datetime.combine(parsed_date,parsed_time)
        start,end = date_start,time_end + time_offset
    elif parsed_date is not None:
        parsed = parsed_date
        start,end = date_start,date_end
    elif parsed_time is not None:
        parsed = parsed_time
        start,end = time_start + time_offset,time_end + time_offset
        
    #print "Found at (%d,%d) "%(start,end), datetime_string[start:end]
    
    
    ret.append(parsed)
          
    if index == True:
        ret.append((start,end))
    
    if len(ret) == 1: ret = ret[0]
    
    return ret
    
def trim(datetime_info,pos,init):
    '''
    @summary: Trim after number [year :1,month:2,day:3,hour:4,min:5,second:6,microsecond:7]
    @param num: can not exceed microseconds
    @parma init: can be string or iterable obj which is same number of num ['start','end']
    '''
    if pos < 1 :
        return None
    
    dt = parsing(datetime_info)
    if(dt == None):
        return None
    
    if pos > 6:
        return dt
    
    max_len = 7
    start =[1,1,1,0,0,0,0]
    end = [9999,12,31,23,59,59,999999]
    
        
    if isinstance(init, str):
        s = init.lower()
        if s == 'start':
            init = start[pos:max_len]
        elif s == 'end':
            init = end[pos:max_len]
        else:
            return dt
        
    
    replaces = list(tuples(dt))
    
    for i in range(pos,max_len):
        replaces[i] = init[i-pos]
    
    
    return dt.replace(*replaces)

def datetime_range(start_datetime,end_datetime,years=0,months=0,weeks=0,days=0,hours=0,minutes=0,seconds=0,milliseconds=0,microseconds=0):
    '''
    @param - start_datetime
    @param - end_datetime
    @param - time frequency
    '''
    start_datetime = parsing(start_datetime)
    end_datetime = parsing(end_datetime)
    if(start_datetime == None or end_datetime == None):
        return []
    
    #print 'Start/End : %s/%s'%(start_datetime,end_datetime)
    
    ret_list = []
    t = start_datetime

    if start_datetime > end_datetime:
        t = end_datetime
    
    init_i = 0
    for i,td in zip([NYEAR,NMONTH,NWEEK,NDAY,NHOUR,NSECOND],[years,months,weeks,days,hours,seconds]):
        if td != 0: init_i = i
      
    while trim(t,init_i,'start') <= end_datetime :
        ret_list.append(t) 
        
        t = t + timedelta(weeks=weeks,days=days,hours=hours,minutes=minutes,seconds=seconds,milliseconds=milliseconds,microseconds=microseconds)
        m = t.month + months
        #print datetime_t.month,m,m%12
        m1,m2 = int(m/12),m%12
        m1,m2 = [(m1,m2),(m1-1,12)][m2==0]
    
        
        t = t.replace(year=t.year + years + m1, month=m2)
                      
       
    return ret_list 

def parse(*args,**kargs):
    '''
    Make datatime object with args
    input : int sequence,list,tuple,string
    keywords : type - datetime, date, time
    
    Datetime object or None 
    '''
    
    ret = None
    num = len(args)
    init = datetime(1,1,1) 
       
    buf = []
    
    if num == 1:
        if(isinstance(args[0],datetime)):
            ret = args[0]
        elif(isinstance(args[0],str)):
            parsed = parse_string(args[0])
            if isinstance(parsed, datetime):
                ret = parsed
            elif isinstance(parsed,date):
                ret = datetime.combine(parsed,time())
            elif isinstance(parsed,time):
                ret = datetime.combine(date(1,1,1),parsed)
                 
        elif(isinstance(args[0],tuple) or isinstance(args[0],list)):
            buf.extend(args[0])
        elif(isinstance(args[0],int)):
            ret = init.replace(args[0])

    elif num > 1:
        
        for a in args:
            
            na = int(a)
            fa = float(a)
            buf.append(na)
            if(na-fa != 0 ):    
                buf.append(int(round(fa-na,6)*1e6))
                break
        
    if(ret == None and len(buf) > 0):
        
        try:
            ret = init.replace(*buf)
        except Exception as err:
            print err
    

    return ret
def move(current,period,start=None):
    '''
    @summary: return move datetime from current with the period
    @param current: current datetime
    @param period: timedelta
    @param start: start datetime
    @return: datetime 
    '''
    
    next_datetime =  None
    if start is not None:
        next_datetime = parsing(start)
    
    current_datetime = parsing(current)
    
    while next_datetime <= current_datetime:
        next_datetime += period
    
    return next_datetime
    
    

def tuples(datetime_info,trim=None,fsecond=None):
    '''
    @summary: Convert datetime tuples
    @param trim: ['date','time']
    @param second: None | integer 
    @return: tuples | None
    '''
    dt = parsing(datetime_info)
    if (dt == None):
        return None
    
    if(isinstance(trim,str)):
        trim = trim.lower()
       
        
    ret = (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond)
    if fsecond != None:
        ret = (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second+dt.microsecond*1e-6)
     
    if trim == 'date':
        return ret[:3]
    elif trim == 'time':
        return ret[3:]
    
    return ret    
    
    
def julian_day(datetime_info,reverse=False):
        
    ret =   None
    if reverse == False:
        
        dt = parsing(datetime_info)
        if dt != None:
            ret = gc_to_jd(*tuples(dt, 'datetimef'))
            
    else:
        try:
            datetime = float(dt)
        
            ret = jd_to_gc(dt)
            ret = datetime(ret)
            
            
        except Exception as err:
            print err
        
    return ret

def gc_to_jd(year,month=1,day=1,hour=0,minute=0,second=0.0):
    a = (14-month)/12
    y = year + 4800 - a
    m = month + 12*a - 3
    jdn = day + (153*m + 2)/5 + 365*y + y/4 - y/100 + y/400 -32045
    
    time = (hour-12)/24. + minute/1440.+ second/86400.

    return jdn+time

def jd_to_gc(jd):
    jj = jd + 0.5
    j = int(jj) + 32044
    g = divmod(j,146097)
    c = divmod((divmod(g[1],36524)[0] + 1) * 3 ,4)[0]
    dc = g[1] - c*36524
    b = divmod(dc,1461)
    a = divmod((divmod(b[1],365)[0] + 1) * 3,4)[0]
    da = b[1] - a*365
    y = g[0]*400 + c *100 + b[0] *4 + a
    m = divmod((da*5+308),153)[0] - 2
    d = da - divmod((m+4)*153,5)[0] + 122
    yy = y - 4800 +divmod(m + 2, 12)[0]
    mm = divmod(m+2,12)[1] + 1
    dd = d+1
    
    time = jj - int(jj)
    time = time*24
    hour  = int(time)
    time = (time - hour)*60
    minute  = int(time)
    sec = (time - minute)*60
       
    return (int(yy),int(mm),int(dd),hour,minute,sec)

def modified_julian_day(jd,reverse=False):
    '''
    Modified Julian Day
    @param    (float)jd : Julian day
    @return   (float) : Modified Julian Day
    '''
    if reverse == False:
        mjd = jd - 2400000.5
    else:
        mjd = jd + 2400000.5
        
    return mjd


parsing = parse # For compatibility