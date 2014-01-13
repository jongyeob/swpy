'''
##
##
## Real-tme Dst index : 1967 - 2008
## Final Dst index :2009 - current
##
'''
import swpy

from utils import with_dirs, alert_message
import utils.datetime as dt
import utils.download as dl

import logging
LOG = logging.getLogger('dst')

DST_DIR = swpy.data_dir + "/kyoto/dst/";
DST_KEYS = ['datetime','version','dst'] 

def empty_data():
    return {'datetime':[],'dst':[],'version':[]}

def downloads_cgi(begindate, enddate=None):
    '''
    Download dst data from cgi
    
    :return: downloaded filepath
    '''
    if enddate == None:
        enddate = begindate
        
    begin_dt, end_dt = dt.trim(begindate,3,'start'),dt.trim(enddate,3,'end')
    
    now_dt = begin_dt
    
    files = []
    while ( now_dt <= end_dt ):
        
        year = now_dt.strftime("%Y")
        url_cgi = "http://wdc.kugi.kyoto-u.ac.jp/cgi-bin/dstae-cgi?SCent=%(cent)s&STens=%(tens)s&SYear=%(year)s&SMonth=%(month)s&ECent=%(cent)s&ETens=%(tens)s&EYear=%(year)s&EMonth=%(month)s&Image+type=GIF&COLOR=COLOR&AE+Sensitivity=0&Dst+Sensitivity=0&Output=DST&Out+format=WDC&Email=code@swpy.org"%{
            "cent":year[0:2],
            "tens":year[2:3],
            "year":year[3:4],
            "month":now_dt.month}

        # download Dst file
        file_path = "%(dir)s%(y)s/dst_%(ym)s.txt"%{
                        "dir":DST_DIR,
                        "y":now_dt.year,
                        "ym":now_dt.strftime("%Y%m")}
        
        
        rv = dl.download_url_file(url_cgi, with_dirs(file_path),overwrite=True)
        
        if (rv == None):
            print "Fail to download %s."%(file_path)
        else:
            print "Download %s."%(file_path)
            files.append(rv)

        #
        mr = dt.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
        
    return files

def load(begindate, enddate=""):
    
    begin_dt,end_dt = dt.parsing(begindate),dt.parsing(enddate)
    data = empty_data()

    for t in dt.datetime_range(begin_dt, end_dt, months=1):

        file_path = "%(dir)s%(y)04d/dst_%(y)04d%(m)02d.txt"%{
            "dir":DST_DIR,
            "y":t.year,
            "m":t.month}
        
        LOG.debug(file_path)
        
        temp = None
        try:
            temp = load_file(file_path)
        except IOError:
            file_path = downloads_cgi(t)
            temp = load_file(file_path)
        
        if temp == None:
            return None
            
    
        # time filtering
        i = 0
        for tt in temp["datetime"]:
            if (begin_dt <= dt.parsing(tt) <= end_dt):
                data["datetime"].append( temp["datetime"][i] )
                data["dst"].append( temp["dst"][i] )
                data["version"].append( temp["version"][i] )
            
            i += 1

    
    return data

    
def load_file(file_path):
    '''
    Load dst file
    '''
    
    
    data = empty_data()
    
    # Load a file.
    try:
        with open(file_path, "r") as f:
            contents = f.read()           
    except IOError as err:
        alert_message("Can not find file or read data, %s,in load_dst_file()."%file_path)
        raise err


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
            data['datetime'].append(str(dt.datetime(y, m, d, h, 0, 0)))
            data['dst'].append( int(line[20+h*4:20+h*4+4]) )
            data['version'].append(version)
        
            
    return data

def downloads_web(begindate, enddate=""):
    '''
    Download from kyoto web pages
    '''
    begin_dt, end_dt = dt.trim(begindate,3,'start'),dt.trim(enddate,3,'end')

    #
    now_dt = begin_dt
    while ( now_dt <= end_dt ):

        suffix = "fnl"
        if (now_dt.year < 2009):   # url for final (1957 ~ 2008)
            suffix = "fnl";
            src = "http://wdc.kugi.kyoto-u.ac.jp/dst_final/%(yyyy)04d%(mm)02d/index.html"%{"yyyy":now_dt.year, "mm":now_dt.month}
        elif (now_dt.year < 2012):   # url for provisional (2009 ~ 2011)
            suffix = "prv";
            src = "http://wdc.kugi.kyoto-u.ac.jp/dst_provisional/%(yyyy)04d%(mm)02d/index.html"%{"yyyy":now_dt.year, "mm":now_dt.month}
        else:   # url for realtime (2012 ~
            suffix = "rt";
            src = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/%(yyyy)04d%(mm)02d/index.html"%{"yyyy":now_dt.year, "mm":now_dt.month}

        dst = "%(dir)s%(yyyy)04d/dst_web_%(sf)s_%(yyyy)04d%(mm)02d.txt"%{"dir":DST_DIR, "sf":suffix, "yyyy":now_dt.year, "mm":now_dt.month}

    
        # download it to a tmp file
        tmp = dl.download_url_file(src,swpy.temp_dir+'/dst.tmp',overwrite=True)
        if (tmp == None):
            mr = dt.monthrange(now_dt.year, now_dt.month)
            now_dt = now_dt + dt.timedelta(days=mr[1])
            continue
        else:
            print ("Downloaded %s."%src)
    
        # extract data and save a dst file
        fr = open(tmp, "r")
        contents = fr.read()
        fr.close()

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

            fw = open(with_dirs(dst), "w")
            fw.write(contents)
            fw.close()

        #
        mr = dt.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])


    return True

