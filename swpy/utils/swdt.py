'''
Created on 2013. 5. 7.

@author: kasi
'''

from datetime import datetime, timedelta
from copy import deepcopy


def startdate(datetime_t):
    return  datetime_t.replace(hour=0,minute=0,second=0,microsecond=0)
def enddate(datetime_t):
    return  datetime_t.replace(hour=23,minute=59,second=59,microsecond=999999)
def time_t(datetime_t):
    return datetime_t.replace(1,1,1)  
def datetime_range(start_datetime_t,end_datetime_t,timedelta_t):
    print('Start/End : %s/%s'%(start_datetime_t,end_datetime_t))
    
    ret_list = []
    datetime_t = start_datetime_t
    while datetime_t <= end_datetime_t:
        ret_list.append(datetime_t)
        datetime_t = datetime_t + timedelta_t

        
    return ret_list 
def datetime_t(year,month=1,day=1,hour=0,minute=0,second=0.0):
    return datetime(year,month,day,hour,minute,int(second),int(round(second-int(second),6)*1e6))

def str_to_datetime(datetime_string,datetime_format):
    return datetime.strptime(datetime_string,datetime_format)
def datetime_to_str(datetime_format,datetime_t):
    return datetime.strftime(datetime_format,datetime_t)
          
def date_tuple(datetime_t):
    return (datetime_t.year,datetime_t.month,datetime_t.day)
def time_tuple(datetime_t):
    return (datetime_t.hour,datetime_t.minute,datetime_t.second)
def datetime_tuple(datetime_t):
    return (datetime_t.year,datetime_t.month,datetime_t.day,datetime_t.hour,datetime_t.minute,datetime_t.second+datetime_t.microsecond*1e-6)

def julian_date(datetime_string,datetime_format):
    t = datetime.strptime(datetime_string,datetime_format)
    return datetime_to_jd(t)

def datetime_to_jd(t):
    return gc_to_jd(t.year,t.month,t.day,t.hour,t.minute,t.second+t.microsecond*1e-6)

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

def jd_to_mjd(jd):
    mjd = jd - 2400000.5
    return (mjd,int(mjd),mjd-int(mjd))



