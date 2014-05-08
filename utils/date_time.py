'''
Created on 2013. 5. 7.

@author: kasi
'''

from calendar import monthrange
from datetime import datetime, timedelta,date,time

import logging
import threading

import re

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
DATE_FORMATS = [ "%Y-%m-%d","%d-%b-%Y","%d-%b-%y","%Y-%m","%Y"]
TIME_FORMATS = [ "%H:%M:%S\.%f","%H:%M:%S","%H:%M","%H"]
SEPS = ['_',' ','T']
DATE_SEPS = ['','_','/',' ']
TIME_SEPS = ['','_',' ']

LOG = logging.getLogger(__name__)

NYEAR = 1; NMONTH = 2; NWEEK =3; NDAY = 3; NHOUR = 4; NMINUTE = 5; NSECOND = 6; NSECOND2 = 7

lock_parsing = threading.Lock()

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
        
        f.replace(k,RE_FORMATS[k])
    
    
    with lock_parsing:
        r = re.search(f, datetime_string)
        
    if r == None:
        return None
    
    rd = r.groupdict()
    
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
        print index1
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

def series(start_datetime,end_datetime,years=0,months=0,weeks=0,days=0,hours=0,minutes=0,seconds=0,milliseconds=0,microseconds=0):
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

# For compatibility
parsing = parse 
datetime_range = series

if __name__ == '__main__':
    print parse_string("%Y%m%d","20140201")
    print parse_string("%y%m%d %H%M%S.%f","990201 030201.3")
    print parse_string("%Y-%b-%d","2014-Jul-01")
    print parse_string("%H:%M:%S","20:01:03")
    index = []
    print parse_string("%H:%M:%S","20130103/20:01:03",index=index)
    print index
    
    index = []
    print parse_date("20130303",index=index)
    print index
    
    index = []
    print parse_time("130303",index=index)
    print index
    
    print parse_datetime('2013')
    print parse_datetime('2013',prior='time')
    print parse_datetime("asdf/20130101 010101")
    print parse_datetime("130303")
    print parse_datetime("130303",prior='time')
    print parse_datetime("20140101")
    print parse_datetime("010101 20140313")
    print parse_datetime("010101 20140401",prior='time')
       
    
    
    print "datetime_range()"
    print len(datetime_range((2000,01,01),(2002,02,28),years=1)) == 3
    print len(datetime_range((2000,01,01),(2001,02,28),months=1)) == 14
    
    
    print "parse()"
    print parse(2010) == datetime(2010,1,1)
    print datetime(2010,2,27) == parsing(2010,2,27)== \
                                 parsing((2010,2,27))== \
                                 parsing("20100227")
    print datetime(1999,12,31,11,22,33,444000)
    print parse(1999,12,31,11,22,33.444)
    print parse("19991231_112233.444")
    
    text = "abcd/abcdef/2013/20140202/2014-02-02_002233" # Multiple detect
    dt = parse(text)
    print dt
      
    text = '2-Jul-02'
    print parse('2-Jul-98')
