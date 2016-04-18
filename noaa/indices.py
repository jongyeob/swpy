import os
import re
import tempfile
import tarfile
import shutil


from swpy import utils 
from swpy.utils import config
from swpy.utils import filepath
from swpy.utils import download as dl,\
                       data as da, \
                       date_time as dt
                       


DATA_DIR  = 'data/noaa/indices/%(suffix)/'
DATA_FILE = '%Y_%(suffix).txt'

LOG = utils.get_logger(__name__)


DGD_KEYS = ['Datetime','Mid','High','Planetary']
DPD_KEYS = ['Date','P1','P10','P100','E.6','E.8','E2','Neutron']
DSD_KEYS = ['Date','10.7cm','SNumber','SArea','NewR','MeanF','XBkgd',\
            'C','M','X','S','1','2','3']

    
def initialize(**kwargs):
    config.set(globals(),**kwargs)

def get_path(suffix,date=None):
    return dt.replace(DATA_DIR + DATA_FILE,date,suffix=suffix)
    
def request(suffix,begindate,enddate=''):
    
    path = get_path(suffix)
    files = filepath.request_files(path, begindate, end_datetime=enddate)
    
    return files   
    
def download_dsd(begindate, enddate="",overwrite=False):
    return _download_index(begindate, enddate, "DSD",overwrite=overwrite);

def download_dpd(begindate, enddate="",overwrite=False):
    return _download_index(begindate, enddate, "DPD",overwrite=overwrite);

def download_dgd(begindate, enddate="",overwrite=False):
    return _download_index(begindate, enddate, "DGD",overwrite=overwrite);


def load_dgd(begindate,enddate=""):
    begin_dt =  dt.trim(begindate,3,'start')
    
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end')
    
    data_a = []
    data_k = []
    
    for t1 in dt.series(begin_dt, end_dt, years=1):       
        file_path = get_path('DGD', t1)
    
        if os.path.exists(file_path) == False:
            print "File is not exist!"
            continue
        
        with open(file_path, "r") as f:
            init = False
            for line in f:
                if init == False:        
                    mid_a           = float('nan')  # middle lat. A index
                    mid_k           = [float('nan') for _ in range(8)] # middle lat. K index
                    high_a          = float('nan')  # high lat. A index
                    high_k          = [float('nan') for _ in range(8)] # high lat. K index
                    ap              = float('nan')  # ap
                    kp              = [float('nan') for _ in range(8)] # kp
                    init = True
                
                if line[0] == ':' or line[0] == '#':
                    continue
                            
                dt1 = dt.parse('%s%s%s'%(line[0:4],line[5:7],line[8:10]))
                if dt1 is None:
                    #print "Wrong datetime"
                    continue
                
                if (dt1 < begin_dt or end_dt < dt1):
                    continue
                
                init = False
                
                try:
                    v =  int(line[10:16])
                    if v < 0: raise
                    mid_a = v
                except : pass
                
                for i in range(0,8,1):
                    try: 
                        v = int(line[2*i+17:2*i+19])
                        if v < 0: raise
                        mid_k[i] = v 
                    except : pass
                    
                try:
                    v =  int(line[33:39])
                    if v < 0: raise
                    high_a = v
                except : pass
                
                for i in range(0,8,1):
                    try: 
                        v = int(line[2*i+40:2*i+42])
                        if v < 0 : raise
                        high_k[i] = v
                    except : pass
                               
                try: 
                    v = int(line[56:62])
                    if v < 0 :raise
                    ap = v
                except : pass
                
                for i in range(0,8,1):
                    try: 
                        v = int(line[2*i+63:2*i+65])
                        if v < 0 : raise
                        kp[i] = v
                    except : pass
                    
                #'date','mid_a','mid_k','high_a','high_k','ap','kp'
               
                row_a = [dt1.strftime("%Y%m%d"),mid_a,high_a,ap]
                row_k = [[dt1.replace(hour=_i*3).strftime("%Y%m%d_%H%M%S"),_v[0],_v[1],_v[2]] for _i,_v in enumerate(zip(mid_k,high_k,kp))]
                
                data_a.append(row_a)
                data_k.extend(row_k)
 
              
    return data_a,data_k 
        
def load_dsd(begindate,enddate=""):
    begin_dt =  dt.trim(begindate,3,'start')
    
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end')
    
    
    data = []

    for t1 in dt.datetime_range(begin_dt, end_dt, years=1):
        file_path = get_path('DSD',t1)
                
        if os.path.exists(file_path) == False:
            print "File is not exist!"
            continue
        
        with  open(file_path, "r") as f:
            
            for line in f:
                                
                if line[0] == ':' or line[0] == '#':
                    continue
                
                cols = line.split()
                if len(cols) != 16:
                    #print "Wrong line"
                    continue
                
                dt1 = dt.parse('%s%s%s'%(cols[0],cols[1],cols[2]))
                if dt1 is None:
                    #print "Wrong datetime"
                    continue
                if (dt1 < begin_dt or end_dt < dt1):
                    continue
                
                v = [float('nan') for _ in range(13)]
                v[5] = '' # for xray background
                
                
                for i in range(0,13):
                    try:
                        if i == 5:
                            v[i] = cols[i+3]
                            continue
                        
                        n = int(cols[i+3])
                        if n < 0 :raise
                        v[i] = n
                    except:pass                                   
                

                row = [dt1.strftime("%Y%m%d")]
                row.extend(v)
                
                data.append(row)
                    
    return data


def load_dpd(begindate, enddate=""):
    
    begin_dt = dt.trim(begindate,3,'start')
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end') 

   
    data = []
    # Yearly Loop
    year_dt = begin_dt
    for year_dt in dt.series(begin_dt, end_dt, years=1):
        
        file_path = get_path("DPD",year_dt)
        
        if os.path.exists(file_path) == False:
            print "File is not exist!"
            continue    
        
        lines = []
        with open(file_path, "r") as f:
            lines = f.read().split('\n')
        
        # Skip header
        for line in lines:
            
            if line[0:5] == "#----" or line[0:7] == "   Date":
                continue
            
            column = line.split(' ')
            column = filter(None, column)
            
            if ((len(column) < 8 and year_dt.year <= 1996) or
                (len(column) != 9 and year_dt.year >= 1997)):
                continue

            dt1 = dt.parse("%s-%s-%s"%(column[0], column[1], column[2]))
            
            if dt1 is None:
                continue
                
            if (dt1 < begin_dt or end_dt < dt1):
                continue
    
            row = [dt1.strftime("%Y%m%d")]

            if (dt1.year <= 1996):
                row.append(column[3]) #mev1
                row.append(column[4]) #mev10
                row.append(column[5]) #mev100

                row.append('nan')     #mev06
                row.append('nan')     #mev08
                row.append(column[6]) #mev20
                
                #neutron
                if (column[7][0] == "*"):
                    row.append('nan')
                else:
                    row.append(column[7])
                    
            elif(dt1.year <= 2011):
                row.append(column[3])
                row.append(column[4])
                row.append(column[5])
                
                row.append('nan')
                row.append(column[6])
                row.append(column[7])
                
                if (column[8] == '-999.99'):
                    row.append('nan')
                else:
                    row.append(column[8])
            else:
                row.append(column[3])
                row.append(column[4])
                row.append(column[5])
                
                row.append(column[6])
                row.append('nan')
                row.append(column[7])
                
                if (column[8] == '-999.99'):
                    row.append('nan')
                else:
                    row.append(column[8])
                    
            data.append(row)   
    
    return data
    
def draw_dpd(coldata,days=0, file_path=""):
    import matplotlib.pyplot as plt
    #
    color = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']
    
    
    tindex = map(dt.parse,coldata[0])
    
    # Date list for X-Axis
    tick_dt = []
    if (days == 0):
        days = (max(tindex) - min(tindex)).days + 1

    #if (days > 7):
    #       days = 7
    
    for i in range(0, days+1):
        tick_dt.append(tindex[0].replace(hour=0, minute=0, second=0) + dt.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')

    plt.clf()
    
    # ticks
    plt.rc('xtick.major', pad=12);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);

    # Plot
    plt.plot(tindex, coldata[1], color=color[0], marker="o", label="Proton (> 1 MeV)")
    plt.plot(tindex, coldata[2], color=color[1], marker="*", label="Proton (> 10 MeV)")
    plt.plot(tindex, coldata[3], color=color[2], marker="^", label="Proton (>100 MeV)")

    plt.plot(tindex, coldata[4], color=color[3], marker="^", label="Electron (> .6 MeV)")
    plt.plot(tindex, coldata[5], color=color[3], marker="^", label="Electron (> .8 MeV)")
    plt.plot(tindex, coldata[6], color=color[4], marker="^", label="Electron (> 2 MeV)")

    plt.legend(loc='upper right')

    
    # Title
    plt.title("NOAA Daily Proton Data")
    
    # Scale
    plt.yscale('log')

    # Limitation
    plt.xlim(tick_dt[0], tick_dt[days-1])
    plt.ylim([1.0e2, 1.0e10])

    # Labels for X and Y axis 
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
               fontsize=14)
    
    plt.ylabel("Particles/cm$^{2}$ cm sr")

    
    # X-Axis tick
    tick_dt = []
    tick_str = []

    for i in range(0, days+1, 5):
        tick_dt.append(tindex[0].replace(hour=0, minute=0, second=0) + dt.timedelta(days=i))

    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))

    plt.xticks(tick_dt, tick_str)
    
    # Grid
    plt.grid(True)

    # Show or Save
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    return


def _download_index(begindate, enddate="", suffix="",overwrite=False):
    begin_dt, end_dt = dt.trim(begindate,3,'start'), dt.trim(enddate,3,'end')
    if end_dt == None:
        end_dt = begin_dt
    if suffix not in ["DSD","DPD","DGD"]:
        raise ValueError("not in DSD, DPD, DGD")
        
    quater = ['','Q1','Q2','Q3','Q4']
    host = 'ftp://ftp.swpc.noaa.gov/'
    src_dir  = "pub/indices/old_indices/"
    txt_file = '%Y%(quater)_%(suffix).txt'

    now = dt.datetime.utcnow()
    for year_dt in dt.series(begin_dt,end_dt,years=1):
        dst = get_path(suffix,date=year_dt)
            
        if filepath.path.exists(dst) and not overwrite:
            print "Already exists, %s"%(dst)
            continue
            
        if year_dt.year == end_dt.year == now.year:
            if end_dt.month <= 9:
                quater.pop(-1)
            if end_dt.month <= 6:
                quater.pop(-1)
            if end_dt.month <= 3:
                quater.pop(-1)
        
        text = ''
        for _i,_q in enumerate(quater):
            header = ''
            src = dt.replace(host + src_dir + txt_file,year_dt,suffix=suffix,quater=_q)

            data = dl.download_ftp_file(src)
            
            if not data:
                continue
            
            for line in data.splitlines():
                if not line:
                    continue
            
                if line[0] == ':' or line[0] =='#':
                    header += line + '\n'
                    continue
                if line != '':
                    text += line + '\n'
                    
            if _i == 0:
                break
        
        if text:
            filepath.make_path(dst) 
            with open(dst,'w') as f:
                f.write(header)
                f.write(text)
        else:
            return False
            
    return True
