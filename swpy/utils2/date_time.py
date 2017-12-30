'''
Created on 2016. 10. 20.

@author: jongyeob
'''

from calendar import monthrange
from datetime import datetime, timedelta, date, time


import logging
import re
import threading
import random 
import math


locking_in_re = threading.Lock()

LOG = logging.getLogger('date_time')

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
    
  
    with locking_in_re:
        r = re.search(f, datetime_string)

    if not r:
        return None
    
    rd = r.groupdict()
    if not rd :
        return None
    
    if rd.has_key('y'):
        rd['Y'] = 1900 + int(rd['y'])
        
    if rd.has_key('b'):
        rd['m'] = MONTH_NUMBERS[rd['b'].title()]
    
    if rd.has_key('f'):
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
            if parsed: break
        
        if parsed: break
        
    if parsed:
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
            if parsed: break
    
            #LOG.debug('Find time : ',parsed_time,' with ',  fs,'[%d:%d]'%(r.start(),r.end()))
            
        
        if parsed: break

    if parsed:
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
    
    if parsed1:
        start,end  = index1
        offset = end
        
    parsed2 = parse2(datetime_string[offset:],index=index2)
    
    if parsed2:
        end = index2[-1] + offset
    

    index.append(start)
    index.append(end)       
           
    if prior == 'time':
        parsed1, parsed2 = parsed2, parsed1
        
#     start,end = 0, 0
    if parsed1 and parsed2:
        parsed = datetime.combine(parsed1,parsed2)
    elif parsed1:
        parsed = datetime.combine(parsed1,time())
    elif parsed2:
        parsed = datetime.combine(date(1,1,1),parsed2)
        
        
    #print "Found at (%d,%d) "%(start,end), datetime_string[start:end]
    
    
    return parsed

def series(start,end,step, jitter=0, drop_rate=0.0):
    '''
    @param - start_datetime
    @param - end_datetime
    @param - time frequency
    '''
    
    start_in = parse(start)
    end_in = parse(end)
        
    t = start_in
    if not step:
        raise ValueError('Time step must be positive')
    
    jitter_sum = 0
    jitter_sqsum = 0
    
    t_list = []
    while t <= end_in:
        random_jitter = random.uniform( -jitter,jitter )
        
        t_list.append( t + timedelta( seconds=random_jitter ) )
                
        jitter_sum += random_jitter
        jitter_sqsum += random_jitter**2
        
        t = move(t,step)
        
    t_sample = t_list    
    sample_num = int( len(t_list)*(1-drop_rate) )
        
    if sample_num < len(t_list):
        t_sample = random.sample(t_list, sample_num)
        
        
    jitter_me = jitter_sum / sample_num
    jitter_rmse = math.sqrt( jitter_sqsum/sample_num )
        
    LOG.debug( "Total: {}, Select: {}, Jitter ME: {:.1f}, RMSE: {:.1f}".format(
        len(t_list),
        sample_num,
        jitter_me,
        jitter_rmse))
        
    return t_sample 
    
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
        elif(isinstance(args[0],basestring)):
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
        
    if not ret and buf:
        ret = init.replace(*buf)

    return ret

def move(current,step,start=''):
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
        
    delta = timedelta(seconds=step)
    while next_datetime <= current_datetime:
        next_datetime += delta
    
    return next_datetime
    
    
def to_tuple(datetime_info,trim='datetime',fsecond=False):
    '''
    Convert datetime tuples
    :param trim:        ['datetime','date','time']
    :param fsecond: True, False 
    :return: tuples
    '''
    dt = parse(datetime_info)
        
    ret = (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond)
    if fsecond:
        ret = (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second+dt.microsecond*1e-6)
    
    trim = trim.lower() 
    if trim in ['date']:
        return ret[:3]
    elif trim in ['time']:
        return ret[3:]
    elif trim in ['year']:
        return ret[:1]
    elif trim in ['month']:
        return ret[:2]
    elif trim in ['day']:
        return ret[:3]
    elif trim in ['hour']:
        return ret[:4]
    elif trim in ['minute']:
        return ret[:5]
    elif trim in ['second']:
        return ret[:6]
    
    
    return ret

def julian_day(time,reverse=False,modified=False):
        
    ret =   None
    if reverse == False:
        ret = _gc2jd(*tuple(time,fsecond=True))
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



def sample(datetime_list,sample_rate,ref_time=''):  
    
    datetime_list.sort()
    
    input_ref_time = datetime_list[0]
    if ref_time: 
        input_ref_time = parse(ref_time)
         
    margin = sample_rate/2.
    tx = datetime_list
    
    diff_tx = [(ty-input_ref_time).total_seconds() for ty in tx]
    dtx = zip(diff_tx,tx)
       
    
    t_list = []
    iter_num = 0
    for diff_time in dtx:
        diff,time = diff_time
        
        if -margin < (diff - iter_num*sample_rate) < margin:
            t_list.append(time)
            iter_num += 1

                
    LOG.debug("Number of filtered records : %d"%(len(t_list)))
    
    return t_list

def random_time(t1, t2):
    t1_in = parse(t1)
    t2_in = parse(t2)
    
    total_seconds = (t1_in - t2_in).total_seconds()
    
    random_t = t1_in - timedelta( seconds = random.random()*total_seconds )
    
    return random_t
