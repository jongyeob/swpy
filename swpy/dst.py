'''
Author : Jongyeob Park (pjystar@gmail.com)
         Seonghwan Choi (shchoi@kasi.re.kr)
'''

import os
import re
from swpy import utils
from swpy.utils import config, download as dl
from swpy.utils import datetime as dt

DATA_DIR  = 'data/kyoto/dst/%Y/'
DATA_FILE = 'dst_%Y%m.txt'

DST_KEYS = ['datetime','dst']
LOG = utils.get_logger(__name__)

_RE_WEBFILE = ''
def initialize(**kwargs):
    utils.config.set(globals(),**kwargs)

def request(start,end=''):
    stime = dt.parse(start)
    etime = stime
    if not end:
        etime = dt.parse(end)
        
    utils.filepath.request_files(DATA_DIR + DATA_FILE, stime, etime)
    
def download(start,end='',overwrite=False):
    download_web(start,end,overwrite)
    
def download_web(begin, end="",overwrite=False):
    '''
    Download from kyoto web pages
    '''
    begin_dt = dt.trim(begin,3,'start')
    end_dt = begin_dt
    if end != '':
        end_dt =  dt.trim(end,3,'end')
        #
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        contents = ''
        
        suffix = "fnl"
        src = "http://wdc.kugi.kyoto-u.ac.jp/dst_final/%(yyyy)04d%(mm)02d/index.html"%{"yyyy":now_dt.year, "mm":now_dt.month}
        contents = dl.download_http_file(src,overwrite=overwrite)
        
        if contents == '':
            suffix = "prv";
            src = "http://wdc.kugi.kyoto-u.ac.jp/dst_provisional/%(yyyy)04d%(mm)02d/index.html"%{"yyyy":now_dt.year, "mm":now_dt.month}
            contents = dl.download_http_file(src,overwrite=overwrite)
        
        if contents == '':
            suffix = "rt";
            src = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/%(yyyy)04d%(mm)02d/index.html"%{"yyyy":now_dt.year, "mm":now_dt.month}
            contents = dl.download_http_file(src,overwrite=overwrite)
                       
        if contents == '':
            mr = dt.monthrange(now_dt.year, now_dt.month)
            now_dt = now_dt + dt.timedelta(days=mr[1])
            continue
        else:
            print ("Downloaded %s."%src)
    

        dstpath = dt.replace(DATA_DIR + DATA_FILE,now_dt)
            
        i1 = contents.find("<pre class=\"data\">")
        i1 = i1 + "<pre class=\"data\">".__len__()
        i1 = contents.find("-->", i1)
        i2 = contents.find("</pre>")
        i2 = contents.rfind("<!--", i1, i2)
        if (i1 != -1 and i2 != -1):
            i1 = i1+3
            i2 = i2-1
            contents = contents[i1:i2]
            contents = contents.lstrip("\r\n")
            
            # write a new dst
            utils.filepath.mkpath(dstpath)
            fw = open(dstpath, "wt")
            fw.write(contents)
            fw.close()

        #
        mr = dt.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])

def download_cgi(begin, end='',overwrite=False):
    '''
    Download dst data from cgi
    '''
    if not end:
        end = begin
        
    begin_dt, end_dt = dt.trim(begin,3,'start'),dt.trim(end,3,'end')
    
    now_dt = begin_dt
    
    
    while ( now_dt <= end_dt ):
        
        year = now_dt.strftime("%Y")
        url_cgi = "http://wdc.kugi.kyoto-u.ac.jp/cgi-bin/dstae-cgi?SCent=%(cent)s&STens=%(tens)s&SYear=%(year)s&SMonth=%(month)s&ECent=%(cent)s&ETens=%(tens)s&EYear=%(year)s&EMonth=%(month)s&Image+type=GIF&COLOR=COLOR&AE+Sensitivity=0&Dst+Sensitivity=0&Output=DST&Out+format=WDC&Email=code@swpy.org"%{
            "cent":year[0:2],
            "tens":year[2:3],
            "year":year[3:4],
            "month":now_dt.month}

        # download Dst file
        file_path = dt.replace(DATA_DIR + DATA_FILE,now_dt)
        utils.filepath.mkpath(file_path)
                 
        rv = dl.download_http_file(url_cgi, file_path,overwrite=overwrite)
        
        if (rv == False):
            print "Fail to download %s."%(file_path)
        else:
            print "Download %s."%(file_path)
            
        #
        mr = dt.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
        

def load(begin, end=""):
    if end == "":
        end = begin
        
    begin_dt,end_dt = dt.parse(begin),dt.parse(end)
    records = []
    for t in dt.datetime_range(begin_dt, end_dt, months=1):

        file_path = dt.replace(DATA_DIR + DATA_FILE,t)    
        if not os.path.exists(file_path):
            LOG.warn("File is not exist - {}".format(file_path))
            continue  
        record = load_webfile(file_path)
        
        records.extend(record)
        
    
    records = dt.filter(records, begin_dt,end_dt)
    
    
    return records

def load_webfile(file_path):
    '''
    Load dst file
    '''
    
    records = []
    
    with open(file_path, "r") as f:
        contents = f.read()           
    
    lines = contents.splitlines()
    
    m,y = lines[2].split()
    my = dt.datetime.strptime("{} {}".format(m,y),"%B %Y")
    if my is None:
        return records
    
    
    width  = 4
    
    for line in lines[6:]:
        if line == '' : #blank line
            continue
        
        cur = 2 # cursor
        day = int(line[0:cur])
        cur += 1
        
        for i in range(3):
            for j in range(8):
                
                ymdh = my.replace(day=day,hour=i*8 + j)
                val  = line[cur:cur+width]
                if val == '9999':
                    continue
                records.append([ymdh.strftime("%Y%m%d_%H%M%S"), float(val)])
                cur += width
            cur += 1
    
    return records        
        
def load_cgifile(file_path):
    '''
    Load dst file
    '''
    
    records = []
    
    with open(file_path, "r") as f:
        contents = f.read()           
    
    for line in contents.splitlines():
        # Index name
        if (line[0:3] != "DST"):
            continue

        # 3-4 : the last two digits of the year
        # 14-15 : top two digits of the year (19 or space for 19xx, 20 from 2000)
        y = int(line[14:16] + line[3:5])
        if (y < 100): y=y+1900

        m = int(line[5:7])   # month
        d = int(line[8:10])  # day

        version = int(line[13:14])
        
        for h in range(0, 24):
            v1 = dt.datetime(y, m, d, h, 0, 0).strftime('%Y%m%d_%H%M%S')
            v2 = version
            v3 = int(line[20+h*4:20+h*4+4]) 
            
            records.append([v1,v2,v3])
            
    return records

def draw(dstdata,file_path=""):
    from  matplotlib import pyplot as plt
    
    color = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']   
        
    # Figure
    fig = plt.figure(facecolor='white')
           
    # ticks
    plt.rc('xtick.major', pad=12);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);
    
    # Title
    plt.title("Dst Index")
    
    # Plot
    plt.plot(dstdata, color=color[0])

    # Scale
    plt.yscale('linear')

    # Limitation
    #plt.xlim(tick_dt[0], tick_dt[days-1])
    plt.ylim([-200, 50])

    # Labels for X and Y axis 
    #plt.xlabel("%s ~ %s [UTC]"% (tick_dt[0][0:10],tick_dt[days-1][0:10]),fontsize=14)
    plt.ylabel("Dst Index")
              
    # Grid
    plt.grid(True)

    # Show or Save
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)

    return fig
