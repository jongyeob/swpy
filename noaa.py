##
##
## Real-tme Dst index : 1967 - 2008
## Final Dst index :2009 - current
##

# standard library
import os

import swpy

from swpy.utils import utils
from swpy.utils import date_time as dt
from swpy.utils import download as dl
from swpy.utils import data as da


# SpaeWeatherPy library
#noaa_url = "ftp://ftp.swpc.noaa.gov/pub/warehouse/"
NOAA_URL = "http://www.swpc.noaa.gov/ftpdir/"
NOAA_DIR = swpy.DATA_DIR + "/noaa";

DATA_DIR = swpy.DATA_DIR
TEMP_DIR = swpy.TEMP_DIR

COLOR_LIST = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']

DGD_keys = ['date',\
            'mid_a', 'mid_k:0','mid_k:3','mid_k:6','mid_k:9','mid_k:12','mid_k:15','mid_k:18','mid_k:21',\
            'high_a','high_k:0','high_k:3','high_k:6','high_k:9','high_k:12','high_k:15','high_k:18','high_k:21',\
            'ap',    'kp:0','kp:3','kp:6','kp:9','kp:12','kp:15','kp:18','kp:21']
DPD_keys = ['date','mev1','mev10','mev100','mev06','mev08','mev20','neutron']
DSD_keys = ['date','radio','sunspot_number','sunspot_area','new_regions','mean_field','xray_background',\
            'x-ray:C','x-ray:M','x-ray:X',\
            'optical:S','optical:1','optical:2','optical:3']

def initialize():
    pass

def download_template(suffix, begindate, enddate=""):
    
    if enddate == "":
        enddate = begindate
        
    begin_dt, end_dt = dt.trim(begindate,3,'start'), dt.trim(enddate,3,'end')
    downloaded_files = []
    for now_dt in dt.datetime_range(begin_dt, end_dt, days=1):

        src = "%(url)swarehouse/%(yyyy)04d"%{"url":NOAA_URL, "yyyy":now_dt.year}        
        tar_file = "/%(yyyy)04d_%(suffix)s.tar.gz"%{"yyyy":now_dt.year,"suffix":suffix}
        
        tmp = "%(tmp)s/%(yyyy)04d_%(suffix)s.tar.gz"%{"tmp":TEMP_DIR, "yyyy":now_dt.year, "suffix":suffix}
        
        dst_dir = "%(dir)s/%(suffix)s/%(yyyy)04d"%{"dir":NOAA_DIR, "yyyy":now_dt.year, "suffix":suffix}
        txt_file = "/%(yyyy)04d%(mm)02d%(dd)02d%(suffix)s.txt"%{"suffix":suffix,"yyyy":now_dt.year,"mm":now_dt.month,"dd":now_dt.day}
        
        # check src
        src_path = src +'/'+suffix+txt_file
        dst_path = utils.make_path(dst_dir + txt_file)
        rv = dl.download_http_file(src_path, dst_path ,overwrite=True)

        if rv == False:
            tar_path = dl.download_http_file(src+tar_file,overwrite=True)
            if tar_path == None:
                print "No tar..."
                continue
            
            # Extract a gz file.
            print "Extract it to the temp directory, %s."%(TEMP_DIR)
    
            import tarfile
            tf = tarfile.open(tar_path, 'r:gz')
            _,filename = os.path.split(tar_path)
            filename,_ = os.path.splitext(filename)
            tf.extractall(utils.make_path(TEMP_DIR+'/'+filename))
            tf.close()
        
        
            # Move extracted files to a data directory.
            tmp_dir = TEMP_DIR + '/' + filename
            
            try:
            
                import shutil
        
                for filepath in utils.get_files(tmp_dir+'/*.txt'):
                    _,filename = os.path.split(filepath)
                    if (os.path.exists(dst_dir +'/'+ filename) == True):
                        shutil.copyfile(filepath, utils.make_path(dst_dir+'/'+filename))
                        os.remove(filepath)
                    else:                        
                        shutil.move(filepath, utils.make_path(dst_dir+'/'+filename))
            
                # Remove a temp directory and a temp file.
                shutil.rmtree(tmp_dir)
                os.remove(tmp)
                
            except Exception as err:
                print err
            
            # retry
            rv = dl.download_http_file(src+txt_file, dst_dir + txt_file)
        
        if rv != False:
            print "Donwloaded : %s"%(dst_path)
            downloaded_files.append(dst_path)
                    

    return downloaded_files


def download_se(begindate, enddate=""):
    download_template("events", begindate, enddate)

def download_srs(begindate, enddate=""):
    download_template("SRS", begindate, enddate)

def download_sgas(begindate, enddate=""):
    files = download_template("SGAS", begindate, enddate)
    return files

def download_rsga(begindate, enddate=""):
    download_template("RSGA", begindate, enddate)

def download_geoa(begindate, enddate=""):
    download_template("GEOA", begindate, enddate)


def download_index(begindate, enddate="", type=""):
    begin_dt, end_dt = dt.trim(begindate,3,'start'), dt.trim(enddate,3,'end')
    if end_dt == None:
        end_dt = begin_dt
    if (type != "DSD" and type != "DPD" and type != "DGD"):
        return False
    
    
    quater = ['','Q1','Q2','Q3','Q4']
    
    for year_dt in dt.datetime_range(begin_dt,end_dt,years=1):
        
        if year_dt.year == end_dt.year:
            if end_dt.month <= 9:
                quater.pop(-1)
            if end_dt.month <= 6:
                quater.pop(-1)
            if end_dt.month <= 3:
                quater.pop(-1)
        
        #
        file_name = "%(y)04d_%(type)s.txt"%{
            "y":year_dt.year,
            "type":type}
        
        src = "%(url)sindices/old_indices/%(fn)s"%{
            "url":NOAA_URL,
                "fn":file_name}
        
        dst = "%(dir)s/indices/%(type)s/%(fn)s"%{
            "dir":NOAA_DIR,
            "type":type,
            "fn":file_name}
        
        # Download a file.
        utils.alert_message("Download %s."%(src))
        rv = dl.download_http_file(src, dst)
        
        # start parsing quater data
        if (rv == False):
            text = ''
            for i in range(1,len(quater)):
                file_name = "%(y)04d%(q)s_%(type)s.txt"%{"y":year_dt.year,"q":quater[i],"type":type}
                src = "%(url)sindices/old_indices/%(fn)s"%{"url":NOAA_URL,"fn":file_name}
                data = dl.download_http_file(src)
                if data == '':
                    continue
                
                for line in data.splitlines():
                    if line[0] == ':' or line[0] =='#':
                        continue
                    if line != '':
                        text += line + '\n'
            
            if text != '':
                with open(dst,'w') as f: f.write(text)
            else:
                return False
            
    return True

def download_dsd(begindate, enddate=""):
    return download_index(begindate, enddate, "DSD");

def download_dpd(begindate, enddate=""):
    return download_index(begindate, enddate, "DPD");

def download_dgd(begindate, enddate=""):
    return download_index(begindate, enddate, "DGD");


def load_dgd(begindate,enddate=""):
    begin_dt =  dt.trim(begindate,3,'start')
    
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end')
    
    data = {}
    
    for t1 in dt.datetime_range(begin_dt, end_dt, years=1):
        
        file_name = "%(y)04d_DGD.txt"%{"y":t1.year}
        
        file_path = "%(dir)s/indices/DGD/%(fn)s"%{
                    "dir":NOAA_DIR,
                    "fn":file_name}
        
        if os.path.exists(file_path) == False:
            print "File is not exist!"
            rv = download_dgd(t1)
            if rv == False:
                print "Download Failed!"
                continue
        ldt1    = []
        lmid_a  = []
        lmid_k  = []
        lhigh_a = []
        lhigh_k = []
        lap     = []
        lkp     = []
        
        with open(file_path, "r") as f:
            init = False
            for line in f:
                if init == False:        
                    mid_a           = float('nan')  # middle lat. A index
                    mid_k           = [float('nan')]*8 # middle lat. K index
                    high_a          = float('nan')  # high lat. A index
                    high_k          = [float('nan')]*8 # high lat. K index
                    ap              = float('nan')  # ap
                    kp              = [float('nan')]*8 # kp
                    init = True
                
                if line[0] == ':' or line[0] == '#':
                    continue
                            
                dt1 = dt.parsing('%s%s%s'%(line[0:4],line[5:7],line[8:10]))
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
               
                
                ldt1.append(dt1)
                lmid_a.append(mid_a)
                lhigh_a.append(high_a)
                lap.append(ap)
                lmid_k.append(mid_k)
                lhigh_k.append(high_k)
                lkp.append(kp)


    data = {'date':ldt1, 'mid_a':lmid_a, 'high_a':lhigh_a, 'ap':lap}
    for i in range(8):
        ii = i*3
        key  = 'mid_k:%d'%(ii)
        key2 = 'high_k:%d'%(ii)
        key3 = 'kp:%d'%(ii) 
        data[key] = list(zip(*lmid_k)[i])
        data[key2] = list(zip(*lhigh_k)[i])
        data[key3] = list(zip(*lkp)[i])
          
    return data 
        
def load_dsd(begindate,enddate=""):
    begin_dt =  dt.trim(begindate,3,'start')
    
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end')


    d              = []
    radio_flux     = []
    sunspot_number = []
    sunspot_area   = []
    new_regions    = []
    mean_field     = []
    xray_background= []
    x_ray          = [] 
    optical        = [] 
    
    for t1 in dt.datetime_range(begin_dt, end_dt, years=1):
        file_name = "%(y)04d_DSD.txt"%{"y":t1.year}
        
        file_path = "%(dir)s/indices/DSD/%(fn)s"%{
                    "dir":NOAA_DIR,
                    "fn":file_name}
        
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
                
                dt1 = dt.parsing('%s%s%s'%(cols[0],cols[1],cols[2]))
                if dt1 is None:
                    #print "Wrong datetime"
                    continue
                if (dt1 < begin_dt or end_dt < dt1):
                    continue
                
                v = [float('nan')]*13
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
                
           #['date','radio_flux','sunspot_number','sunspot_area','new_regions','mean_field','xray_background','x-ray','optical']
                
                d.append(dt1)
                radio_flux.append(v[0])
                sunspot_number.append(v[1])
                sunspot_area.append(v[2])
                new_regions.append(v[3])
                mean_field.append(v[4])
                xray_background.append(v[5])
                x_ray.append(v[6:9])
                optical.append(v[9:])
        
        
        data = {'date':d,'radio_flux':radio_flux,'sunspot_number':sunspot_number,'sunspot_area':sunspot_area,\
                'new_regions':new_regions,'mean_field':mean_field,'xray_background':xray_background}
        
        x = ['C','M','X'] 
        for i in range(3):
            key = 'x-ray:'+x[i]                
            data[key].append(list(zip(*x_ray)[i]))
        o = ['S','1','2','3']
        for i in range(4):
            key = 'optical'+o[i] 
            data[key].append(list(zip(*optical)[i]))
            
    return data


def load_dpd(begindate, enddate=""):
    
    begin_dt = dt.trim(begindate,3,'start')
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end') 

    
    t0 = []
    t1 = []
    mev1  = []
    mev10 = []
    mev100 = []
    
    mev06 = []
    mev08 = []
    mev20 = []

    neutron = []
    
    
    # Yearly Loop
    year_dt = begin_dt
    for year_dt in dt.datetime_range(begin_dt, end_dt, years=1):
        
        #
        file_name = "%(y)04d_DPD.txt"%{"y":year_dt.year}
        
        file_path = "%(dir)s/indices/DPD/%(fn)s"%{
                    "dir":NOAA_DIR,
                    "fn":file_name}
        
        if os.path.exists(file_path) == False:
            print "File is not exist!"
            continue    
        
        with open(file_path, "r") as f:
    
        # Skip header
            for line in f:
                if (len(line) < 10):
                    continue
    
                if (line[0:5] == "#----" or line[0:7] == "   Date"):
                    break
    
            for line in f:
                column = line.split(' ')
    
                column = filter(None, column)
                
                if ( (len(column) < 8 and year_dt.year <= 1996) or
                    (len(column) != 9 and year_dt.year >= 1997)):
                    continue
    
                dt1 = dt.parsing("%s-%s-%s"%(column[0], column[1], column[2]))
                
                if dt1 is None:
                    continue
                    
                if (dt1 < begin_dt or end_dt < dt1):
                    continue
        
                t0.append(dt1.strftime("%Y%m%d"))
    
                if (dt1.year <= 1996):
                    mev1.append(float(column[3]))
                    mev10.append(float(column[4]))
                    mev100.append(float(column[5]))
    
                    mev06.append(float('nan'))
                    mev08.append(float('nan'))
                    mev20.append(float(column[6]))
                    
                    if (column[7][0] == "*"):
                        neutron.append(float('nan'))
                    else:
                        neutron.append(float(column[7]))
                elif(dt1.year <= 2011):
                    mev1.append(float(column[3]))
                    mev10.append(float(column[4]))
                    mev100.append(float(column[5]))
                    
                    mev06.append(float('nan'))
                    mev08.append(float(column[6]))
                    mev20.append(float(column[7]))
                    
                    if (float(column[7]) < 0):
                        neutron.append(float('nan'))
                    else:
                        neutron.append(float(column[7]))
                        
                         
        data = {"date":t0, "mev1":mev1, "mev10":mev10, "mev100":mev100, "mev06":mev06, "mev08":mev08,"mev20":mev20, "neutron":neutron} 
    
    return data
                        