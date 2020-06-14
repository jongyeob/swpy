'''
Created on 2013. 5. 7.

@author: kasi
'''
from __future__ import absolute_import

from calendar import monthrange
from datetime import datetime, timedelta, date, time
import logging
import re
import threading

from . import utils


__all__ = ['datetime''date','time','timedelta',
           'parse_string','parse_date','parse_time','parse_datetime',
           'trim','iseries','series','parse','move','tuples','replace','sample'
           'julian_day','filter','total_seconds']



MONTH_NUMBERS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
RE_FORMATS = {'%Y': '\d{4}',
              '%y': '\d{2}',
              '%m': '\d{1,2}',
              '%d': '\d{1,2}',
              '%H': '\d{1,2}',
              '%M': '\d{1,2}',
              '%S': '\d{1,2}',
              '%f': '\d{1,6}',
              '%b': '[a-zA-Z]+'}
RE_NAMES = {'%Y': '?P<Y>',
            '%y': '?P<y>',
            '%m': '?P<m>',
            '%d': '?P<d>',
            '%H': '?P<H>',
            '%M': '?P<M>',
            '%S': '?P<S>',
            '%f': '?P<f>',
            '%b': '?P<b>'}
DIC_NAMES = {'%Y': '%(Y)04d',
             '%y': '%(y)02d',
             '%m': '%(m)02d',
             '%d': '%(d)02d',
             '%H': '%(H)02d',
             '%M': '%(M)02d',
             '%S': '%(S)02d',
             '%f': '%(f)06d',
             '%b': '%(b)s'}

DATE_FORMATS = [ "%Y-%m-%d","%d-%b-%Y","%d-%b-%y","%Y-%m","%Y"]
TIME_FORMATS = [ "%H:%M:%S\.%f","%H:%M:%S","%H:%M","%H"]
SEPS = ['_',' ','T']
DATE_SEPS = ['','_','/',' ']
TIME_SEPS = ['','_',' ']

LOG = logging.getLogger(__name__)

lock_parsing = threading.Lock()

def least_delta(format_string):
    '''
    return least datetime index 
    '''
    key = ''
    ret = {}
    if format_string.find('%Y') != -1 : key ='years'
    if format_string.find('%y') != -1 : key ='years'
    if format_string.find('%m') != -1 : key ='months'
    if format_string.find('%b') != -1 : key ='months'
    if format_string.find('%d') != -1 : key ='days'
    if format_string.find('%H') != -1 : key ='hours'
    if format_string.find('%M') != -1 : key ='minutes'
    if format_string.find('%S') != -1 : key ='seconds'
    if format_string.find('%f') != -1 : key ='fseconds'
    
    if key:
        ret[key] = 1
    
    return ret
     

def parse_string(format_string,datetime_string,index=[]):
    '''
    parsing datetime string with format

    :param str format_string : string of format
    :param str datetime_string: string of datetime
    
    :return: datetime or None
    '''    
    
    f = format_string
    
    for k in RE_FORMATS.iterkeys():
            
        i = f.find(k) # i : index
        
        if i != -1:
            v = '('+RE_NAMES[k]+RE_FORMATS[k]+')'
            f = f[:i] + v + f[i+2:]
        
        f = f.replace(k,RE_FORMATS[k])
    
  
    with lock_parsing:
        r = re.search(f, datetime_string)

    if r == None:
        return None
    
    rd = r.groupdict()
    if len(rd) <= 0 :
        return None
    
    if rd.has_key('y') == True:
        rd['Y'] = 1900 + int(rd['y'])
        
    if rd.has_key('b') == True:
        rd['m'] = MONTH_NUMBERS[rd['b'].title()]
    
    if rd.has_key('f') == True:
        rd['f'] = int(rd['f'].ljust(6,'0'))
    
    year  = int(rd.setdefault('Y',1))
    month = int(rd.setdefault('m',1))
    day   = int(rd.setdefault('d',1))
    hour  = int(rd.setdefault('H',0))
    minute = int(rd.setdefault('M',0))
    second = int(rd.setdefault('S',0))
    fsecond = int(rd.setdefault('f',0))

    
    parsed = None
    try:    
        parsed = datetime(year,month,day,hour,minute,second,fsecond)
        index.append(r.start())
        index.append(r.end())
    except: pass
        
    return parsed 

def parse_date(date_string,index=[]):
    
    parsed = None
    
    # date searching
    for fmt in DATE_FORMATS:
        fs = fmt
        for sep in DATE_SEPS:            
            parsed = parse_string(fs,date_string,index = index)
            
            fs = fmt.replace('-',sep)
            if parsed  is not None: break
        
        if parsed is not None: break
        
    if parsed is not None:
        parsed = parsed.date()
   
    
    return parsed

def parse_time(time_string,index=[]):

    parsed = None
    
    # time searching
                    
    for fmt in TIME_FORMATS:
        fs = fmt
        for sep in TIME_SEPS:
            
            parsed = parse_string(fs,time_string,index = index)
            
            fs = fmt.replace(':',sep)
            if parsed is not None: break
    
            #LOG.debug('Find time : ',parsed_time,' with ',  fs,'[%d:%d]'%(r.start(),r.end()))
            
        
        if parsed is not None: break

    if parsed is not None:
        parsed = parsed.time()
    
    
    return parsed
    
def parse_datetime(datetime_string,prior='date',index=[]):
    '''
    parse datetime from string

    :param str datetime_string: string of datetime
    :return: datetime or None
    '''
    parsed = None
    
    parsed1 = None
    parsed2 = None
    
    offset = 0
    start, end = 0, 0
    
    index1 = []
    index2 = []
    
    parse1 = parse_date
    parse2 = parse_time
    
    if prior == 'time':
        parse1,parse2 = parse2,parse1
        
    parsed1 = parse1(datetime_string,index=index1)
    
    if parsed1 is not None:
        start,end  = index1
        offset = end
        
    parsed2 = parse2(datetime_string[offset:],index=index2)
    
    if parsed2 is not None:
        end = index2[-1] + offset
    

    index.append(start)
    index.append(end)       
           
    if prior == 'time':
        parsed1, parsed2 = parsed2, parsed1
        
#     start,end = 0, 0
    if parsed1 is not None and parsed2 is not None:
        parsed = datetime.combine(parsed1,parsed2)
    elif parsed1 is not None:
        parsed = datetime.combine(parsed1,time())
    elif parsed2 is not None:
        parsed = datetime.combine(date(1,1,1),parsed2)
        
        
    #print "Found at (%d,%d) "%(start,end), datetime_string[start:end]
    
    
    return parsed

def trim(datetime_info,pos,init):
    '''
    @summary: Trim after number [year :1,month:2,day:3,hour:4,min:5,second:6,microsecond:7]
    @param num: can not exceed microseconds
    @parma init: can be string or iterable obj which is same number of num ['start','end']
    '''
       
    dt = parse(datetime_info)
    if not dt:
        return None
    
    _pos = pos
    if isinstance(pos, str):
        pos_ = pos.lower()
        
        if pos_ in ['date']:
            _pos = 3
        elif pos_ in ['hour']:
            _pos = 4
        elif pos_ in ['minute']:
            _pos = 5
        elif pos_ in ['second']:
            _pos = 6
            
    if _pos < 1 :
        return datetime_info
    
    if _pos > 6:
        return dt

    max_len = 7
    start =[1,1,1,0,0,0,0]
    end = [9999,12,31,23,59,59,999999]
    
        
    if isinstance(init, str):
        s = init.lower()
        if s == 'start':
            init = start[_pos:max_len]
        elif s == 'end':
            init = end[_pos:max_len]
        else:
            return dt
        
    
    replaces = list(tuples(dt))
    
    for i in range(_pos,max_len):
        replaces[i] = init[i-_pos]
    
    
    return dt.replace(*replaces)

def iseries(start_datetime,end_datetime,years=0,months=0,weeks=0,days=0,hours=0,minutes=0,seconds=0,milliseconds=0,microseconds=0):
    '''
    @param - start_datetime
    @param - end_datetime
    @param - time frequency
    '''
    start_datetime = parse(start_datetime)
    end_datetime = parse(end_datetime)
    
    assert start_datetime or end_datetime,"Datetime parsing error!"
        
    init_i = 0
    for i,td in zip([1,2,3,3,4,6],[years,months,weeks,days,hours,seconds]):
        if td != 0: init_i = i
    
    t = start_datetime
    while trim(t,init_i,'start') <= end_datetime :
        yield t 
        
        t1 = t + timedelta(weeks=weeks,days=days,hours=hours,minutes=minutes,seconds=seconds,milliseconds=milliseconds,microseconds=microseconds)
        
        
        m = t1.month + months
        #print datetime_t.month,m,m%12
        m1,m2 = int(m/12),m%12
        m1,m2 = [(m1,m2),(m1-1,12)][m2==0]
    
        
        t1 = t1.replace(year=t1.year + years + m1, month=m2)
        
        if t1 == t:
            break
        else:
            t = t1
                     
def series(start_datetime,end_datetime,years=0,months=0,weeks=0,days=0,hours=0,minutes=0,seconds=0,milliseconds=0,microseconds=0):
    '''
    @param - start_datetime
    @param - end_datetime
    @param - time frequency
    '''
    return [t for t in iseries(start_datetime,end_datetime,
                               years=years,months=months,weeks=weeks,days=days,
                               hours=hours,minutes=minutes,seconds=seconds,
                               milliseconds=milliseconds,microseconds=microseconds)]
    
def parse(*args,**kargs):
    '''
    Make datatime object with args
    input : int sequence,list,tuple,string
    keywords : type - datetime, date, time
               format - format
    
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
            ret = parse_datetime(args[0])
        elif(isinstance(args[0],tuple) or isinstance(args[0],list)):
            buf.extend(args[0])
        elif(isinstance(args[0],int)): # for year only
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
            print(err)
    

    return ret
def move(current,period,start=''):
    '''
    return move datetime from current with the period
    :param current: current datetime
    :param period: timedelta
    :param start: start datetime
    :return: datetime 
    '''
    
    current_datetime = parse(current)
    next_datetime =  current
    if start:
        next_datetime = parse(start)
        
    
    while next_datetime <= current_datetime:
        next_datetime += period
    
    return next_datetime
    
    

def tuples(datetime_info,trim=None,fsecond=None):
    '''
    Convert datetime tuples
    :param trim:        ['date','time']
    :param second: None | integer 
    :return: tuples | None
    '''
    dt = parse(datetime_info)
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

def replace(format_string,datetime_info=None,**kwargs):
    '''
    Replace datetime format to a filled string with datetime
    :param string format:
    :param datetime datetime_info: 
    '''
            
    dt = parse(datetime_info)
    f = format_string
    
    if dt != None:
        
        for k in RE_FORMATS.iterkeys():
            i = 0
            while(i != -1): 
                i = f.find(k) # i : index
            
                if i != -1: 
                    f = f[:i] + dt.strftime(k) + f[i+2:]   
        
    f = utils.replace(f,**kwargs)
        
    return f    
    
    
    
def julian_day(time,reverse=False,modified=False):
        
    ret =   None
    if reverse == False:
        ret = _gc2jd(*tuples(time,fsecond=True))
        if modified:
            ret += 2400000.5

    else:
        time = float(time)
        if modified:
            time += 2400000.5
        ret = _jd2gc(float(time))            
        
    return ret

JD_19000101_120000 = 2415021.0

def julian_centuries(t):
    DAYS_IN_YEAR = 36525.0
    jc = (julian_day(t) - JD_19000101_120000)/DAYS_IN_YEAR
    return jc
    
def _gc2jd(year,month=1,day=1,hour=0,minute=0,second=0.0):
    a = (14-month)/12
    y = year + 4800 - a
    m = month + 12*a - 3
    jdn = day + (153*m + 2)/5 + 365*y + y/4 - y/100 + y/400 -32045
    
    time = (hour-12)/24. + minute/1440.+ second/86400.

    return jdn+time

def _jd2gc(jd):
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



def filter(datetime_list,start_datetime,end_datetime,sample_rate=0,cadence=0):
    '''
    filter list containing datetime.
    
    parameters:
        datetime_list - iterable object, but 0th elements are date time string or object. 
        start_datetime - string
        end_datetime   - string
    optional:
        cadence        - number, seconds
    returns:
        list
    '''
    if cadence and not sample_rate:
        sample_rate = cadence
    
    ret = []

    start   = parse(start_datetime)
    end     = parse(end_datetime) 
        
    
    LOG.debug("Time filter : %s, %s, %d"%(str(start),str(end),sample_rate))
    
    records = [rec for rec in datetime_list if rec[0] and start <= rec[0] <= end]
    records.sort()
    
    if sample_rate:
        records = sample(records,sample_rate,ref_time=start)
        
    return records
       
    

def sample(datetime_list,sample_rate,ref_time=''):  
    
    datetime_list.sort()
    
    input_ref_time = datetime_list[0]
    if ref_time: 
        input_ref_time = parse(ref_time)
         
    margin = timedelta(seconds=sample_rate/2.)
    tx = datetime_list
    
    diff_tx = [(ty[0]-input_ref_time).total_seconds() for ty in tx]
    dtx = zip(diff_tx,tx)
       
    
    ret = []
    iter_num = 0  
    while dtx:
        diff_ty,ty = dtx.pop(0)
        
        if 0<= diff_ty - iter_num*sample_rate + margin <= sample_rate:
            ret.append(ty)

        iter_num += 1      
                
    LOG.debug("Number of filtered records : %d"%(len(ret)))
    
    return ret

def total_seconds(days=0,hours=0,minutes=0,seconds=0,milliseconds=0,microseconds=0):
    total = days*86400 + hours*3600 + minutes*60 + seconds + milliseconds*1e-3 + microseconds*1e-6
    return total
 
# For compatibility
parsing = parse 
datetime_range = series
get_least_delta = least_delta
