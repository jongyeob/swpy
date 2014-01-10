##
##
## Real-tme Dst index : 1967 - 2008
## Final Dst index :2009 - current
##

# standard library
import os

# SpaeWeatherPy library
import swpy
import utils
import utils.datetime as dt
import utils.download as dl



#noaa_url = "ftp://ftp.swpc.noaa.gov/pub/warehouse/"
NOAA_URL = "http://www.swpc.noaa.gov/ftpdir/"
NOAA_DIR = swpy.data_dir + "/noaa";

COLOR_LIST = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']


def download_template(suffix, begindate, enddate=""):
    

    begin_dt, end_dt = dt.trim(begindate,3,'start'), dt.trim(enddate,3,'end')
    downloaded_files = []
    for now_dt in dt.datetime_range(begin_dt, end_dt, days=1):

        src = "%(url)swarehouse/%(yyyy)04d"%{"url":NOAA_URL, "yyyy":now_dt.year}        
        tar_file = "/%(yyyy)04d_%(suffix)s.tar.gz"%{"yyyy":now_dt.year,"suffix":suffix}
        
        tmp = "%(tmp)s/%(yyyy)04d_%(suffix)s.tar.gz"%{"tmp":swpy.temp_dir, "yyyy":now_dt.year, "suffix":suffix}
        
        dst_dir = "%(dir)s/%(suffix)s/%(yyyy)04d"%{"dir":NOAA_DIR, "yyyy":now_dt.year, "suffix":suffix}
        txt_file = "/%(yyyy)04d%(mm)02d%(dd)02d%(suffix)s.txt"%{"suffix":suffix,"yyyy":now_dt.year,"mm":now_dt.month,"dd":now_dt.day}
        
        # check src
        dst_path = dl.download_url_file(src+'/'+suffix+txt_file,utils.with_dirs(dst_dir + txt_file),overwrite=True)

        if dst_path == None:
            tar_path = dl.download_url_file(src+tar_file,utils.with_dirs(tmp),overwrite=True)
            if tar_path == None:
                print "No tar..."
                continue
                
            
            # Extract a gz file.
            print "Extract it to the temp directory, %s."%(swpy.temp_dir)
    
            import tarfile
            tf = tarfile.open(tar_path, 'r:gz')
            _,filename = os.path.split(tar_path)
            filename,_ = os.path.splitext(filename)
            tf.extractall(utils.with_dirs(swpy.temp_dir+'/'+filename))
            tf.close()
        
        
            # Move extracted files to a data directory.
            tmp_dir = swpy.temp_dir + '/' + filename
            
            try:
            
                import shutil
        
                for filepath in utils.get_files(tmp_dir+'/*.txt'):
                    _,filename = os.path.split(filepath)
                    if (os.path.exists(dst_dir +'/'+ filename) == True):
                        shutil.copyfile(filepath, utils.with_dirs(dst_dir+'/'+filename))
                        os.remove(filepath)
                    else:                        
                        shutil.move(filepath, utils.with_dirs(dst_dir+'/'+filename))
            
                # Remove a temp directory and a temp file.
                shutil.rmtree(tmp_dir)
                os.remove(tmp)
                
            except Exception as err:
                print err
            
            # retry
            dst_path = dl.download_url_file(src+txt_file, dst_dir + txt_file)
        
        if dst_path != None:
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
    
    if (type != "DSD" and type != "DPD" and type != "DGD"):
        return False
    
    
    # Yearly Loop
    year_dt = begin_dt
    while ( year_dt <= end_dt ):
        #
        year_dt = year_dt.replace(month=1, day=1);
        
        #
        file_name = "%(y)04d_%(type)s.txt"%{
            "y":year_dt.year,
            "type":type}
        
        src = "%(url)sindices/old_indices/%(fn)s"%{
            "url":NOAA_URL,
                "fn":file_name}
        
        dst = "%(dir)sindices/%(type)s/%(fn)s"%{
            "dir":NOAA_DIR,
            "type":type,
            "fn":file_name}
        
        # Download a file.
        utils.alert_message("Download %s."%(src))
        rv = dl.download_url_file(src, dst)
        if (rv == False):
            continue
        
        #
        year_dt = year_dt + dt.timedelta(days=367)
    
    return True

def download_dsd(begindate, enddate=""):
    return download_index(begindate, enddate, "DSD");

def download_dpd(begindate, enddate=""):
    return download_index(begindate, enddate, "DPD");

def download_dgd(begindate, enddate=""):
    return download_index(begindate, enddate, "DGD");



def load_dpd(begindate, enddate=""):
    begin_dt, end_dt = dt.trim(begindate,3,'start'), dt.trim(enddate,3,'end')
    
    t0 = []
    t1 = []
    mev1  = []
    mev10 = []
    mev100 = []
    
    mev06 = []
    mev20 = []

    neutron = []
    
    
    # Yearly Loop
    year_dt = begin_dt
    while ( year_dt <= end_dt ):
        #
        year_dt = year_dt.replace(month=1, day=1);

        #
        file_name = "%(y)04d_DPD.txt"%{"y":year_dt.year}
        
        file_path = "%(dir)sindices/DPD/%(fn)s"%{
                    "dir":NOAA_DIR,
                    "fn":file_name}
        
        f = open(file_path, "r")
    
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
            
            #
            dt = dt.datetime.strptime("%s %s %s"%(column[0], column[1], column[2]), "%d %b %y")
    
            if (dt < begin_dt or end_dt < dt):
                continue
    
            t0.append(dt)

            if (dt.year <= 1996):
                mev1.append(float(column[3]))
                mev10.append(float(column[4]))
                mev100.append(float(column[5]))

                mev06.append("")
                mev20.append(column[6])
                
                if (column[7][0] == "*"):
                    neutron.append("")
                else:
                    neutron.append(column[7])

        f.close()
        
        #
        year_dt = year_dt + dt.timedelta(days=367)
    
    return {"t0":t0, "mev1":mev1, "mev10":mev10, "mev100":mev100, "mev06":mev06, "mev20":mev20, "neutron":neutron}

