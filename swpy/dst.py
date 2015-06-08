'''
Author : Jongyeob Park (pjystar@gmail.com)
         Seonghwan Choi (shchoi@kasi.re.kr)
'''


##
##
## Real-tme Dst index : 1967 - 2008
## Final Dst index :2009 - current
##

from swpy import utils
from swpy.utils import Config,\
                       date_time as dt,\
                       download as dl
                       
DATA_DIR = 'data/kyoto/dst/'
DST_KEYS = ['datetime','version','dst']
LOG = utils.get_logger(__name__)
PACKAGES = ''

def initialize(config=Config()):
    global DATA_DIR,PACKAGES
    
    config.set_sections(__name__)
    
    DATA_DIR = config.load('DATA_DIR',DATA_DIR)
    PACKAGES = config.load('PACKAGES',PACKAGES)
    
    for pkg in PACKAGES.split():
        utils.import_all(pkg, globals())

    
def empty_data():
    return {'datetime':[],'dst':[],'version':[]}

def download_cgi(begindate, enddate=None,overwrite=False):
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
        file_path = DATA_DIR + "%(y)s/dst_%(ym)s.txt"%{"y":now_dt.year,"ym":now_dt.strftime("%Y%m")}
        
        
        rv = dl.download_http_file(url_cgi, utils.make_path(file_path),overwrite=overwrite)
        
        if (rv == False):
            print "Fail to download %s."%(file_path)
        else:
            print "Download %s."%(file_path)
            files.append(file_path)

        #
        mr = dt.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
        
    return files

def load(begindate, enddate=""):
    if enddate == "":
        enddate = begindate
        
    begin_dt,end_dt = dt.parsing(begindate),dt.parsing(enddate)
    data = empty_data()

    for t in dt.datetime_range(begin_dt, end_dt, months=1):

        file_path = DATA_DIR + "%(y)04d/dst_%(y)04d%(m)02d.txt"%{"y":t.year,"m":t.month}
        
        LOG.debug(file_path)
        
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
            data['datetime'].append(str(dt.datetime(y, m, d, h, 0, 0)))
            data['dst'].append( int(line[20+h*4:20+h*4+4]) )
            data['version'].append(version)
        
            
    return data

def download_web(begindate, enddate="",overwrite=False):
    '''
    Download from kyoto web pages
    '''
    begin_dt, end_dt = dt.trim(begindate,3,'start'),dt.trim(enddate,3,'end')

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
                       
        if (contents == ''):
            mr = dt.monthrange(now_dt.year, now_dt.month)
            now_dt = now_dt + dt.timedelta(days=mr[1])
            continue
        else:
            LOG.debug("Downloaded %s."%src)
    

        dst = DATA_DIR + "%(yyyy)04d/dst_%(yyyy)04d%(mm)02d.txt"%{"yyyy":now_dt.year, "mm":now_dt.month}
            
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

            fw = open(utils.make_path(dst), "w")
            fw.write(contents)
            fw.close()

        #
        mr = dt.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])


    return True

def draw_dst(data, file_path=""):
    from  matplotlib import pyplot as plt
    
    color = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']   
        
    # Date list for X-Axis
    tick_dt = []
    
    days = len(data['datetime'])
   
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
    plt.plot(data['dst'], color=color[0])

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


# def draw_dst(dt, v0, v1=0, v2=0, days=7, file_path="", color=""):
#     
#     #
#     global color_list
#     if (color == ""):
#         color = color_list
#     
#     # Date list for X-Axis
#     tick_dt = []
#     for i in range(0, days+1):
#         tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + datetime.timedelta(days=i))
#     
#     # Figure
#     fig = plt.figure(facecolor='white')
#     plt.clf()
#     #plt.rc('text', usetex=True)
#     
#     # Title
#     plt.title("Dst Index")
# 
#     # X-Axis
#     plt.xlim(tick_dt[0], tick_dt[days-1])
#     plt.xlabel("%s $\sim$ %s [UTC]"% \
#             (tick_dt[0].strftime("%Y.%m.%d."),
#              tick_dt[days-1].strftime("%Y.%m.%d.")),
#              fontsize=14)
#     
#     # Y-Axis
#     plt.ylim([-120, 50])
#     plt.yscale('linear')
#     plt.ylabel("Dst [nT]")
#     
#     
#     # ticks
#     plt.rc('xtick.major', pad=10);
#     plt.rc('xtick.major', size=6);
#     
#     plt.rc('ytick.major', pad=12);
#     plt.rc('ytick.major', size=8);
#     plt.rc('ytick.minor', size=4);
#     
#     # X-Axis Ticks
#     tick_str = []
#     for item in tick_dt:
#         tick_str.append(item.strftime("%b %d"))
#     plt.xticks(tick_dt, tick_str)
#     
#     
#     
#     # Grid
#     plt.grid(True)
# 
#     # Plot, and Show or Save
#     plt.plot(dt, v0, color=color[0])
#     
#     if (file_path == ""):
#         plt.show()
#     else:
#         fig.savefig(file_path)
#     
#     return

if __name__ == '__main__':
    
    
    print download_web("19991011", "20141114")
    print download_cgi("20130901", "20131010")
    
    data = load("20130901", "20130908")
    
    dt = [dt.datetime(2012, 01, 01, 0, 0, 0),
      dt.datetime(2012, 01, 02, 0, 0, 0),
      dt.datetime(2012, 01, 03, 0, 0, 0)]
    

    y = [-25, -32, -64]
    draw_dst(dt, y, days=7)
