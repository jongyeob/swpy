
# standard library
import os
import re


from swpy.utils import utils
from swpy.utils import date_time as dt,\
                       download as dl,\
                       data as da,\
                       Config

# SpaeWeatherPy library
#noaa_url = "ftp://ftp.swpc.noaa.gov/pub/warehouse/"
LIB_NAME = 'NOAA'
DATA_DIR = 'data/noaa/'
TEMP_DIR = 'temp/'
NOAA_URL = "http://www.swpc.noaa.gov/ftpdir/"
PACKAGES = ''
LOG = utils.get_logger(LIB_NAME)

DGD_keys = ['date',\
            'mid_a', 'mid_k:0','mid_k:3','mid_k:6','mid_k:9','mid_k:12','mid_k:15','mid_k:18','mid_k:21',\
            'high_a','high_k:0','high_k:3','high_k:6','high_k:9','high_k:12','high_k:15','high_k:18','high_k:21',\
            'ap',    'kp:0','kp:3','kp:6','kp:9','kp:12','kp:15','kp:18','kp:21']
DPD_keys = ['date','mev1','mev10','mev100','mev06','mev08','mev20','neutron']
DSD_keys = ['date','radio_flux','sunspot_number','sunspot_area','new_regions','mean_field','xray_background',\
            'x-ray:C','x-ray:M','x-ray:X',\
            'optical:S','optical:1','optical:2','optical:3']
events_keys = ['date','event:no','event:flag','begin:flag','begin:time',\
               'max:flag','max:time','end:flag','end:time','obs','quality',\
               'type','loc/frq','property:1','property:2','region']
SRS_keys = ['date','nmbr','loc','l0','area','z','ll','nn','mag']


first_data = {'events':dt.parse(1996,07,31),\
              'SRS':dt.parse(1996,02,01)}
color_list = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']

def initialize(config=''):
    if isinstance(config,str):
        config = Config(config)
        
    config.set_section(LIB_NAME)
    config.load_ns('DATA_DIR',globals())
    config.load_ns('TEMP_DIR',globals())
    config.load_ns('PACKAGES',globals())
    
    for pkg in PACKAGES.split():
        utils.import_all(pkg, globals())

def get_path(suffix,dateobj):
    
    path = ''
    d = dt.parse(dateobj)
    if d == None:
        return path
        
    dirpath = DATA_DIR + "%(suffix)s/%(yyyy)04d/"%{"yyyy":d.year, "suffix":suffix}
    filename ="%(yyyy)04d%(mm)02d%(dd)02d%(suffix)s.txt"%{"suffix":suffix,"yyyy":d.year,"mm":d.month,"dd":d.day}
    
    path = utils.path.normpath(dirpath + filename)
    
    return path

def get_files(suffix,begindate='',enddate=''):
    
    if begindate != '':
        begindate = dt.parse(begindate)
    if enddate != '':
        enddate   = dt.parse(enddate)
            
    files = []
            
    dirpath = "%(suffix)s/"%{"suffix":suffix}
    file_pattern = "*%(suffix)s.txt"%{"suffix":suffix}
      
    filepath = DATA_DIR + dirpath + file_pattern
        
    for f  in utils.get_files(filepath):
        ft = dt.parse(f)
        if enddate != '' and enddate < ft:           
            continue
        
        if begindate != '' and begindate > ft:
            continue
        
        files.append(f)

    
    return files
    
   
def download_events(begindate, enddate="",overwrite=False):
    begindate = dt.parse(begindate)
    if begindate < first_data['events']:
        begindate = first_data['events']

    _download_template("events", begindate, enddate,overwrite)
    

def download_srs(begindate, enddate="",overwrite=False):
    begindate = dt.parse(begindate)
    if begindate < first_data['SRS']:
        begindate = first_data['SRS']
    
    _download_template("SRS", begindate, enddate,overwrite)
    

def download_sgas(begindate, enddate="",overwrite=False):
    _download_template("SGAS", begindate, enddate,overwrite)
    

def download_rsga(begindate, enddate="",overwrite=False):
    _download_template("RSGA", begindate, enddate,overwrite)
    

def download_geoa(begindate, enddate="",overwrite=False):
    _download_template("GEOA", begindate, enddate,overwrite)
    

def _download_template(suffix, begindate, enddate="",overwrite=False):
    
    if enddate == "":
        enddate = begindate
        
    begin_dt, end_dt = dt.trim(begindate,3,'start'), dt.trim(enddate,3,'end')
            
    
    for now_dt in dt.datetime_range(begin_dt, end_dt, days=1):

        
        src_dir = "%(url)swarehouse/%(yyyy)04d/"%{"url":NOAA_URL,"yyyy":now_dt.year}        
        dst_dir = DATA_DIR + "%(suffix)s/%(yyyy)04d/"%{"yyyy":now_dt.year, "suffix":suffix}
        
        txt_file = "%(yyyy)04d%(mm)02d%(dd)02d%(suffix)s.txt"%{"suffix":suffix,"yyyy":now_dt.year,"mm":now_dt.month,"dd":now_dt.day}
        tar_file = "%04d_%s.tar.gz"%(now_dt.year,suffix)
        
        dst_path = utils.make_path(dst_dir + txt_file)
        dst_tarpath = TEMP_DIR +  tar_file
        
        prefix_events = ''
        if suffix == 'events':
            prefix_events = str(now_dt.year)+'_'
            
        if suffix == 'SRS' and (2006<=now_dt.year<=2007):
            tar_file = tar_file[5:]
        
            
        src_path = src_dir + prefix_events+ suffix+'/'+txt_file
        src_tarpath = src_dir +  tar_file
        
        
        rv = dl.download_http_file(src_path, dst_path ,overwrite=overwrite)

        if rv == False: 
 
            rv =  dl.download_http_file(src_tarpath,dst_tarpath)
            if rv == False:
                LOG.info("No tar... %s"%(src_dir+tar_file))
                continue
            
            # Extract a gz file.
    
            import tarfile
            rv = False
            with tarfile.open(dst_tarpath, 'r:gz') as tf:
                _,filename = os.path.split(dst_tarpath)
                filename,_ = os.path.splitext(filename)
                
                
                for name in tf.getnames():
                    if name.find(txt_file) != -1:
                        break
                    name = ''
                    
                
                if name != '':
                    tmp_dir = utils.make_path(TEMP_DIR + filename)
                    
                    tf.extractall(tmp_dir)
                    
                    import shutil
                    for filepath in utils.get_files(tmp_dir+'/*.txt'):
                        _,filename = os.path.split(filepath)
                        
                        if os.path.exists(dst_dir + filename) == True and overwrite == True:
                            continue
                                                
                        shutil.copyfile(filepath, dst_dir + filename)
                
                    # Remove a temp directory and a temp file.
                    shutil.rmtree(tmp_dir)
                else:
                    LOG.info("There is not %s in tar"%(txt_file))       
            
        
        if rv != False:
            LOG.info("Donwloaded : %s"%(dst_path))
     

def download_dsd(begindate, enddate="",overwrite=False):
    return _download_index(begindate, enddate, "DSD",overwrite=overwrite);

def download_dpd(begindate, enddate="",overwrite=False):
    return _download_index(begindate, enddate, "DPD",overwrite=overwrite);

def download_dgd(begindate, enddate="",overwrite=False):
    return _download_index(begindate, enddate, "DGD",overwrite=overwrite);

def _download_index(begindate, enddate="", type="",overwrite=False):
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
        
        dst = DATA_DIR + "indices/%(type)s/%(fn)s"%{
            "type":type,
            "fn":file_name}
        
        
        # Download a file.
        utils.alert_message("Download %s."%(src))
        rv = dl.download_http_file(src, dst,overwrite=overwrite)
        
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


def load_dgd(begindate,enddate=""):
    begin_dt =  dt.trim(begindate,3,'start')
    
    end_dt = begin_dt
    if enddate != "":
        end_dt = dt.trim(enddate,3,'end')
    
    data = {}
    
    for t1 in dt.datetime_range(begin_dt, end_dt, years=1):
        
        file_name = "%(y)04d_DGD.txt"%{"y":t1.year}
        
        file_path = DATA_DIR + "indices/DGD/%(fn)s"%{"fn":file_name}
    
        if os.path.exists(file_path) == False:
            print "File is not exist!"
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
                    mid_k           = [float('nan') for _ in range(8)] # middle lat. K index
                    high_a          = float('nan')  # high lat. A index
                    high_k          = [float('nan') for _ in range(8)] # high lat. K index
                    ap              = float('nan')  # ap
                    kp              = [float('nan') for _ in range(8)] # kp
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
    
    
    data = None

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
        
        file_path = DATA_DIR + "indices/DSD/%(fn)s"%{"fn":file_name}
                
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
            data[key] = list(zip(*x_ray)[i])
        o = ['S','1','2','3']
        for i in range(4):
            key = 'optical:'+o[i]
            data[key] = list(zip(*optical)[i])
            
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
    
    data = None
    # Yearly Loop
    year_dt = begin_dt
    for year_dt in dt.series(begin_dt, end_dt, years=1):
        
        #
        file_name = "%(y)04d_DPD.txt"%{"y":year_dt.year}
        
        file_path = DATA_DIR + "indices/DPD/%(fn)s"%{"fn":file_name}
        
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

def load_events(begindate,enddate=''):
    
    begin_dt = dt.trim(begindate,3,'start')
    if begin_dt < first_data['events']:
        begin_dt = first_data['events']
    
    if enddate == '':
        enddate = begindate
        
    end_dt = dt.trim(enddate,3,'end')
    
    vl = [[] for _ in range(16)]
    
    for t in dt.series(begin_dt, end_dt, days=1):
        
        #
        file_name = "%(y)d%(m)02d%(d)02devents.txt"%{'y':t.year,'m':t.month,'d':t.day}
        
        file_path = DATA_DIR + "events/%(y)4d/%(fn)s"%{"y":t.year,"fn":file_name}
        
        try :
            f  = open(file_path,'r')
            for line in f.readlines():
                
                if ':#'.find(line[0]) != -1:
                    continue
                
                v  = ['' for _ in range(16)]
                              
                
                try:
                    v[0] = str(t.date())
                    v[1] = int(line[0:4].replace(' ',''))
                    v[2] = line[5]
                    
                    v[3] = line[10]
                    strt = dt.parse_string("%H%M", line[11:15])
                    if strt == None:    strt = ''
                    else :    strt = str(strt.time())
                    v[4] = strt
                    
                    v[5] = line[17]
                    strt = dt.parse_string("%H%M", line[18:22])
                    if strt == None:    strt = ''
                    else :    strt = str(strt.time())
                    v[6] = strt
                    
                    v[7] = line[27]
                    strt = dt.parse_string("%H%M", line[28:32])
                    if strt == None:    strt = ''
                    else :    strt = str(strt.time())
                    v[8] = strt
                    
                    v[9] = line[34:38].replace(' ','')
                    v[10] = line[39]
                    v[11] = line[43:47].replace(' ','')
                    v[12] = line[47:58].replace(' ' ,'')
                    
                    i = 0      
                    for l in line[58:76].split():
                        v[13+i] = l
                        i       += 1
                        
                    v[15] = line[76:80]
                    
                except:
                    continue
    
                for i in range(16):
                    vl[i].append(v[i])
            
        except IOError:
            LOG.info("File is not exist. %s",file_path)
            continue
        finally:
            f.close()
    
            
    data = {'date':vl[0],'event:no':vl[1],'event:flag':vl[2],'begin:flag':vl[3],'begin:time':vl[4],\
            'max:flag':vl[5],'max:time':vl[6],'end:flag':vl[7],'end:time':vl[8],'obs':vl[9],'quality':vl[10],\
            'type':vl[11],'loc/frq':vl[12],'property:1':vl[13],'property:2':vl[14],'region':vl[15]}
    return data   
def load_srs(begindate,enddate=''):
    
    begin_dt = dt.trim(begindate,3,'start')
    if enddate == '':
        enddate = begindate
        
    end_dt = dt.trim(enddate,3,'end')
    
    
    fmt = '(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)'
    
    total_var =  9
    vl = [[] for _ in range(total_var)]
    
    for now in dt.series(begin_dt, end_dt,days=1):
        
        filename = "%(yyyy)04d%(mm)02d%(dd)02dSRS.txt"%{"yyyy":now.year,"mm":now.month,"dd":now.day}
        dirpath = DATA_DIR + "SRS/%(yyyy)04d/"%{"yyyy":now.year}
        filepath = dirpath + filename
    
                
        text = ''
        if os.path.exists(filepath) == False:
            LOG.warn("File is not exist - %s"%(filepath))
            continue
        
        with open(filepath,'rt') as f:
            text = f.read()
             
        
        cfmt = re.compile(fmt)
        for line in text.splitlines():
    #        if date is None:
    #            date = match(':Issued: (\d+) (\S+) (\d+) 0030 UTC',line)
            
    #        if date is not None:
    #        if (date is not None) and (time_key['MJD'] is ''):
    #            jd = dbms.gc_to_jd(int(date.group(1)), int(dbms.month_number[date.group(2)]), int(date.group(3)), 0, 30, 0)
    #            mjd = dbms.jd_to_mjd(jd)
    #            time_key['MJD'] = str(mjd[0])
    #            time_key['DATE'] = str('%s-%02d-%s'%(date.group(1),dbms.month_number[date.group(2)],date.group(3)))
    #            root['ATTR']['DATE'] = str('%s-%02d-%s'%(date.group(1),dbms.month_number[date.group(2)],date.group(3)))
    #            root['ATTR']['FILEID'] = str('SRS%s%02d%s' %(date.group(1),dbms.month_number[date.group(2)],date.group(3)))
                
            data = re.match(cfmt,line)
            if data is not None:
                vl[0].append(str(now.date()))
                for i in range(1,total_var):
                    vl[i].append(data.group(i))
                    
                
    data = {'date':vl[0],'nmbr':vl[1],'loc':vl[2],'l0':vl[3],'area':vl[4],'z':vl[5],'ll':vl[6],'nn':vl[7],'mag':vl[8]}                
                                     
      

    return data 
    
def draw_dpd(data, days=0, file_path="", color=""):
    import matplotlib.pyplot as plt
    #
    if (color == ""):        color = color_list
    
    #
    dt = data["t0"]
    
    
    # Date list for X-Axis
    tick_dt = []
    if (days == 0):
        days = (max(dt) - min(dt)).days + 1

    #if (days > 7):
    #       days = 7
    
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + dt.timedelta(days=i))
    
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
    plt.plot(dt, data['mev1'], color=color[0], marker="o", label="Proton (> 1 MeV)")
    plt.plot(dt, data['mev10'], color=color[1], marker="*", label="Proton (> 10 MeV)")
    plt.plot(dt, data['mev100'], color=color[2], marker="^", label="Proton (>100 MeV)")

#plt.plot(dt, data['mev06'], color=color[3], marker="^", label="Electron (> .6 MeV)")
    plt.plot(dt, data['mev20'], color=color[4], marker="^", label="Electron (> 2 MeV)")

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
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + dt.timedelta(days=i))

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

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
       
    
    now = dt.datetime.now()
    
    now_date_str = now.strftime("%Y%m%d")

#     rv = download_events("1996",now_date_str)
#     #print rv
#     events = load_events("1996",now_date_str)
#     tevents = da.Table(data=events,keys=events_keys)
#     tevents.print_text()
    
    
    download_srs("1996", now_date_str)
    SRSs = load_srs("1996", now_date_str)
    tSRSs = da.Table(data=SRSs,keys=SRS_keys)
    tSRSs.print_text()

    
    # rv = download_dpd("1994",str(now.year))
    # print rv
    # data = load_dpd("1994",str(now.year))
    # for key in data.keys():
    #     sys.stdout.write(key+' ')
    # sys.stdout.write('\n')
    # 
    # for key in data.keys():
    #     sys.stdout.write(str(data[key][-1])+' ')
    # sys.stdout.write('\n')
    
    
            
            
    
    #rv = noaa.download_dsd("1994",str(now.year))
    #print rv
    #dsd = load_dsd("1994",str(now.year))
    #table = da.Table(data=dsd)
    #table.print_summary()
    
    #rv = noaa.download_dgd("1994",str(now.year))
    #print rv
    #dgd = load_dgd("1994",str(now.year))
    #table = da.Table(data=dgd)
    #table.print_summary()
    
    #download_events("1996", "2013")
    
    #download_sgas("1996", "2013")
    #download_rsga("1996", "2013")
    #download_geoa("1996", "2013")    
