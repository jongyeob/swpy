#!/usr/bin/python

##
#
# Developed by Seonghwan Choi (shchoi@kasi.re.kr, http://www.choi.pro)
# 
#
# SOHO LASCO CME url : ftp://ftp.ngdc.noaa.gov/STP/SOLAR_DATA/SOLAR_FLARES/FLARES_XRAY/2011/XRAY2011

# data : from 1975
#
##


__author__ = "Seonghwan Choi"
__copyright__ = "Copyright 2012, Korea Astronomy and Space Science"
__credits__ = ["Seonghwan Choi", "Jihye Baek"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Seonghwan Choi"
__email__ = "shchoi@kasi.re.kr"
__status__ = "Production"

# standard library
import calendar
import datetime
import os
import string

import time

from swpy import utils
from swpy.utils import Config,\
                       date_time as dt,\
                       download as dl

DATA_DIR = 'data/'
GOES_DIR = DATA_DIR + "noaa/goes/"
GOES_XRAY_DIR = DATA_DIR + "goes/xray/";
LOG = utils.get_logger(__name__)
# SpaeWeatherPy library
ERROR_INT = -99999

# GOES xray
goes_xray_url = "http://www.swpc.noaa.gov/ftpdir/lists/xray/";
goes_url = "http://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"



color_list = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']

def initialize(config=Config()):
    global DATA_DIR
    
    config.set_section(__name__)
    
    DATA_DIR = config.load('DATA_DIR',DATA_DIR)
    
    
    
def download_xray_csv(begindate, enddate=""):
    if enddate == '': enddate = begindate
    begin_dt, end_dt = dt.trim(enddate,3,'start'), dt.trim(enddate,3,'end')


    # Monthly Loop
    month_dt = begin_dt
    while ( month_dt <= end_dt ):
        #
        mr = calendar.monthrange(month_dt.year, month_dt.month)
        
        dt1 = month_dt.replace(day=1);
        dt2 = month_dt.replace(day = mr[1]);
        

        # GOES-08 ~ GOES-15
        goes_no = 15
        if (dt1 >= datetime.datetime(2010, 9, 1) ):
            goes_no = 15
        elif (dt1 >= datetime.datetime(2003, 1, 1) ):
            goes_no = 12
        elif (dt1 >= datetime.datetime(1998, 7, 1) ):
            goes_no = 10
        elif (dt1 >= datetime.datetime(1995, 1, 1) ):
            goes_no = 8

        #
        file_name = "g%(goes_no)02d_xrs_1m_%(y1)04d%(m1)02d%(d1)02d_%(y2)04d%(m2)02d%(d2)02d.csv"%{
            "goes_no":goes_no,
            "y1":dt1.year,
            "m1":dt1.month,
            "d1":dt1.day,
            "y2":dt2.year,
            "m2":dt2.month,
            "d2":dt2.day}
        
        src = "%(url)s%(y)04d/%(m)02d/goes%(goes_no)02d/csv/%(fn)s"%{"url":goes_url,
            "y":dt1.year,
            "m":dt1.month,
            "goes_no":goes_no,
            "fn":file_name}

        dst = "%(dir)sxray/csv/%(y)04d/%(fn)s"%{"dir":GOES_DIR, "y":dt1.year, "fn":file_name}

        print src

        # Download a file.
        LOG.debug("Download %s"%(src))
        rv = dl.download_http_file(src, dst)
        if (rv == False):
            continue

        # Open a file.
        f = open(dst, "r")
        contents = f.readlines()
        f.close()
                
        # Skip header.
        line_max = len(contents)
        line = 0
        for i in range(len(contents)):
            if (contents[i][0:5] == "data:"):
                line = i
                break;

        if (line == 0):
            LOG.debug("The file format is not correct.\nThere is no 'data:' line.")
            continue

        line += 2
        
        # Daily Loop
        day_dt = dt1
        while ( day_dt <= dt2 ):
            #
            date_str = day_dt.strftime("%Y-%m-%d")
            
            # Open a file.
            file_name = "%(yyyymmdd)s_xrs_1m.txt"%{"yyyymmdd":day_dt.strftime("%Y%m%d")}
            file_path = "%(dir)sxray/1min/%(y)04d/%(fn)s"%{"dir":GOES_DIR, "y":day_dt.year, "fn":file_name}

            utils.make_path(file_path)

            f = open(file_path, "w")

            # Write a header.
            f.write(":Data_list: %s\r\n"%(file_name))
            f.write(":Created: %s UTC\r\n"%(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            f.write("# Prepared by SpaceWeatherPy\r\n")
            f.write("# The data source is from NOAA, Space Weather Prediction Center.\r\n")
            f.write("# \r\n")
            f.write("# Label: Short = 0.05- 0.4 nanometer\r\n")
            f.write("# Label: Long  = 0.1 - 0.8 nanometer\r\n")
            f.write("# Units: Short = Watts per meter squared\r\n")
            f.write("# Units: Long  = Watts per meter squared\r\n")
            f.write("# Source: GOES-%02d\r\n"%(goes_no))
            f.write("# Location: W105\r\n")
            f.write("# Missing data: -1.00e+05\r\n")
            f.write("#\r\n")
            f.write("#                         GOES-%d Solar X-ray Flux\r\n"%(goes_no))
            f.write("# \r\n")
            f.write("#                 Modified Seconds\r\n")
            f.write("# UTC Date  Time   Julian  of the\r\n")
            f.write("# YR MO DA  HHMM    Day     Day       Short       Long        Ratio\r\n")
            f.write("#-------------------------------------------------------------------\r\n")

            # Write data.
            written_lines = 0
            for i in range(line, line_max):
                column = contents[i].split(',')
                
                if ( (len(column) < 6 and goes_no == 15) or
                    (len(column) < 3 and goes_no != 8)):
                    print contents[i]
                    continue
                
                if (date_str != column[0][0:10]):
                    line = i
                    break
                
                cur_dt = datetime.datetime.strptime(column[0], "%Y-%m-%d %H:%M:%S.000")

                jd = 0
                sd = (cur_dt - day_dt).seconds
                
                short_val = -1.00e+05
                long_val = -1.00e+05

                if (goes_no == 15):
                    short_val = float(column[3])
                    long_val = float(column[6])
                #elif (goes_no == 8):
                else:
                    short_val = float(column[1])
                    long_val = float(column[2])

                short_str = "%11.2e"%(short_val)
                long_str = "%11.2e"%(long_val)
                    

                row = "%(yyyy)s %(mm)s %(dd)s  %(HH)s%(MM)s  %(jd)6s %(sd)6s  %(short)11.2e %(long)11.2e %(ratio)s\r\n"% \
                        {"yyyy":column[0][0:4],
                        "mm":column[0][5:7],
                        "dd":column[0][8:10],
                        "HH":column[0][11:13],
                        "MM":column[0][14:16],
                        "jd":jd,
                        "sd": sd,
                        "short": short_val,
                        "long":long_val,
                        "ratio":"0"}
                f.write(row)
                written_lines += 1
                
            # Close the file.
            f.close()

            if (written_lines == 0):
                os.remove(file_path)
            else:
                print file_path
            
            #
            day_dt = day_dt + datetime.timedelta(days=1)


        #
        mr = calendar.monthrange(month_dt.year, month_dt.month)
        month_dt = month_dt + datetime.timedelta(days=mr[1])

def download_mag_csv(begindate, enddate=""):
    if enddate == '' : enddate = begindate
    begin_dt, end_dt = dt.trim(enddate,3,'start'), dt.trim(enddate,3,'end')
        
    # Monthly Loop
    month_dt = begin_dt
    while ( month_dt <= end_dt ):
        #
        mr = calendar.monthrange(month_dt.year, month_dt.month)
        
        dt1 = month_dt.replace(day=1);
        dt2 = month_dt.replace(day = mr[1]);
        
        
        # GOES-08 ~ GOES-15
        goes_no = 13
        if (dt1 >= datetime.datetime(2010, 5, 1) ):
            goes_no = 13
        elif (dt1 >= datetime.datetime(2003, 1, 1) ):
            goes_no = 12
        elif (dt1 >= datetime.datetime(1998, 7, 1) ):
            goes_no = 10
        elif (dt1 >= datetime.datetime(1995, 1, 1) ):
            goes_no = 8
        
        #
        file_name = "g%(goes_no)02d_magneto_1m_%(y1)04d%(m1)02d%(d1)02d_%(y2)04d%(m2)02d%(d2)02d.csv"%{
            "goes_no":goes_no,
            "y1":dt1.year,
            "m1":dt1.month,
            "d1":dt1.day,
            "y2":dt2.year,
            "m2":dt2.month,
            "d2":dt2.day}
        
        src = "%(url)s%(y)04d/%(m)02d/goes%(goes_no)02d/csv/%(fn)s"%{"url":goes_url,
            "y":dt1.year,
            "m":dt1.month,
            "goes_no":goes_no,
            "fn":file_name}
        
        dst = "%(dir)smagneto/csv/%(y)04d/%(fn)s"%{"dir":GOES_DIR, "y":dt1.year, "fn":file_name}
        
        print src
        
        # Download a file.
        LOG.debug("Download %s."%(src))
        rv = dl.download_http_file(src, dst)
        if (rv == False):
            continue
        
        # Open a file.
        f = open(dst, "r")
        contents = f.readlines()
        f.close()
        
        # Skip header.
        line_max = len(contents)
        line = 0
        for i in range(len(contents)):
            if (contents[i][0:5] == "data:"):
                line = i
                break;
        
        if (line == 0):
            LOG.debug("The file format is not correct.\nThere is no 'data:' line.");
            continue
        
        line += 2
        
        # Daily Loop
        day_dt = dt1
        while ( day_dt <= dt2 ):
            #
            date_str = day_dt.strftime("%Y-%m-%d")
            
            # Open a file.
            file_name = "%(yyyymmdd)s_magneto_1m.txt"%{"yyyymmdd":day_dt.strftime("%Y%m%d")}
            file_path = "%(dir)smagneto/1min/%(y)04d/%(fn)s"%{"dir":GOES_DIR, "y":day_dt.year, "fn":file_name}
            
            utils.make_path(file_path)
            
            f = open(file_path, "w")
            
            # Write a header.
            '''
            f.write(":Data_list: %s\r\n"%(file_name))
            f.write(":Created: %s UTC\r\n"%(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            f.write("# Prepared by SpaceWeatherPy\r\n")
            f.write("# The data source is from NOAA, Space Weather Prediction Center.\r\n")
            f.write("# \r\n")
            f.write("# Label: Short = 0.05- 0.4 nanometer\r\n")
            f.write("# Label: Long  = 0.1 - 0.8 nanometer\r\n")
            f.write("# Units: Short = Watts per meter squared\r\n")
            f.write("# Units: Long  = Watts per meter squared\r\n")
            f.write("# Source: GOES-%02d\r\n"%(goes_no))
            f.write("# Location: W105\r\n")
            f.write("# Missing data: -1.00e+05\r\n")
            f.write("#\r\n")
            f.write("#                         GOES-%d Solar X-ray Flux\r\n"%(goes_no))
            f.write("# \r\n")
            f.write("#                 Modified Seconds\r\n")
            f.write("# UTC Date  Time   Julian  of the\r\n")
            f.write("# YR MO DA  HHMM    Day     Day       Short       Long        Ratio\r\n")
            f.write("#-------------------------------------------------------------------\r\n")
            '''

            f.write(":Data_list: %s\r\n"%(file_name))
            f.write(":Created: %s UTC\r\n"%(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            f.write("# Prepared by SWPy.org\r\n")
            f.write("# The data source is from NOAA, Space Weather Prediction Center.\r\n")
            f.write("# \r\n")
            f.write("# Label: Hp component = perpendicular to the satellite orbital plane or\r\n")
            f.write("#           parallel to the Earth's spin axis\r\n")
            f.write("# Label: He component = perpendicular to Hp and directed earthwards\r\n")
            f.write("# Label: Hn component = perpendicular to both Hp and He, directed eastwards\r\n")
            f.write("# Label: Total Field  = \r\n")
            f.write("# Units: nanotesla (nT)\r\n")
            f.write("# Source: GOES-%02d\r\n"%(goes_no))
            f.write("# Location: W089\r\n")
            f.write("# Missing data: -1.00e+05\r\n")
            f.write("#\r\n")
            f.write("#         1-minute GOES-14 Geomagnetic Components and Total Field\r\n")
            f.write("#\r\n")
            f.write("#                 Modified Seconds\r\n")
            f.write("# UTC Date  Time   Julian  of the\r\n")
            f.write("# YR MO DA  HHMM    Day     Day        Hp          He          Hn    Total Field\r\n")
            f.write("#-------------------------------------------------------------------------------\r\n")
    
            # Write data.
            written_lines = 0
            for i in range(line, line_max):
                column = contents[i].split(',')
                
                if ( (len(column) < 67 and goes_no == 13) or
                    (len(column) < 5 and goes_no != 13)):
                    print contents[i]
                    continue
                
                if (date_str != column[0][0:10]):
                    line = i
                    break
                
                cur_dt = datetime.datetime.strptime(column[0], "%Y-%m-%d %H:%M:%S.000")
                
                jd = 0
                sd = (cur_dt - day_dt).seconds
                
                hp_val = -1.00e+05
                he_val = -1.00e+05
                hn_val = -1.00e+05
                ht_val = -1.00e+05
                
                if (goes_no == 13):
                    hp_val = float(column[45])
                    he_val = float(column[48])
                    hn_val = float(column[51])
                    ht_val = float(column[54])
                #elif (goes_no == 8):
                else:
                    hp_val = float(column[1])
                    he_val = float(column[2])
                    hn_val = float(column[3])
                    ht_val = float(column[4])
                
                row = "%(yyyy)s %(mm)s %(dd)s  %(HH)s%(MM)s  %(jd)6s %(sd)6s  %(hp)11.2e %(he)11.2e %(hn)11.2e %(ht)11.2e\r\n"% \
                    {"yyyy":column[0][0:4],
                    "mm":column[0][5:7],
                    "dd":column[0][8:10],
                    "HH":column[0][11:13],
                    "MM":column[0][14:16],
                    "jd":jd,
                    "sd": sd,
                    "hp": float(hp_val),
                    "he": float(he_val),
                    "hn": float(hn_val),
                    "ht": float(ht_val)}
                f.write(row)
                written_lines += 1
            
            # Close the file.
            f.close()
            
            if (written_lines == 0):
                os.remove(file_path)
            else:
                print file_path
            
            #
            day_dt = day_dt + datetime.timedelta(days=1)
        
        
        #
        mr = calendar.monthrange(month_dt.year, month_dt.month)
        month_dt = month_dt + datetime.timedelta(days=mr[1])

    return True


def download_xray(begindate, enddate=''):
    if enddate == '' : enddate = begindate
    begin_dt, end_dt = dt.trim(enddate,3,'start'), dt.trim(enddate,3,'end')
    
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        # 1min
        src = "%(url)s%(yyyy)04d%(mm)02d%(dd)02d_Gp_xr_1m.txt"% \
            {"url":goes_xray_url, "yyyy":now_dt.year, "mm":now_dt.month, "dd":now_dt.day}
        dst = "%(dir)s%(yyyy)04d/%(yyyy)04d%(mm)02d%(dd)02d_Gp_xr_1m.txt"% \
            {"dir":GOES_XRAY_DIR, "yyyy":now_dt.year, "mm":now_dt.month, "dd":now_dt.day}

        rv = dl.download_http_file(src, dst)
        if (rv == False):
            print ("Can not download %s."%src)
        else:
            print ("Downloaded %s."%src)

        # 5 min
        src = "%(url)s%(yyyy)04d%(mm)02d%(dd)02d_Gp_xr_5m.txt"% \
            {"url":goes_xray_url, "yyyy":now_dt.year, "mm":now_dt.month, "dd":now_dt.day}
        dst = "%(dir)s%(yyyy)04d/%(yyyy)04d%(mm)02d%(dd)02d_Gp_xr_5m.txt"% \
            {"dir":GOES_XRAY_DIR, "yyyy":now_dt.year, "mm":now_dt.month, "dd":now_dt.day}

        #
        now_dt = now_dt + datetime.timedelta(days=1)


def load_xray_1m(begindate, enddate=""):
    
    begin_dt, end_dt = dt.trim(enddate,3,'start'), dt.trim(enddate,3,'end')
    
    t0 = []
    t1 = []
    xshort  = []
    xlong = []

    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        # 1min : yyyymmdd_xrs_1m.txt
        file_path = "%(dir)sxray/1min/%(yyyy)04d/%(yyyy)04d%(mm)02d%(dd)02d_xrs_1m.txt"% \
            {"dir":GOES_DIR, "yyyy":now_dt.year, "mm":now_dt.month, "dd":now_dt.day}
        
        
        f = open(file_path, "r")
        
        # Skip header
        for line in f:
            if (line[0:5] == "#----"):
                break

        for line in f:
            column = line.split(' ')
            
            column = filter(None, column)
            
            if (len(column) != 9):
                break
                    
            #
            dt = datetime.datetime( int(column[0]), int(column[1]), int(column[2]), int(column[3][0:2]), int(column[3][2:4]))

            t0.append(dt)
            xshort.append(column[6])
            xlong.append(column[7])

        f.close()
        
        #
        now_dt = now_dt + datetime.timedelta(days=1)

    return {"t0":t0, "xshort":xshort, "xlong":xlong}

def draw_goes_xray(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    import matplotlib.pyplot as plt
        #
    global color_list
    if (color == ""):
        color = color_list

    # Date list for X-Axis
    tick_dt = []
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + datetime.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')
    plt.clf()
      
    # Plot
    plt.plot(dt, v0, color=color[0])
    if (v1 != 0):
        plt.plot(dt, v1, color=color[1])

    # Title
    plt.title("GOES X-ray Flux (1 minute data)")

    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
                fontsize=14)
    
    # Y-Axis
    plt.yscale('log')
    plt.ylim([1.0e-9, 1.0e-2])
    plt.ylabel("Watts/m$^{2}$")

    # ticks
    plt.rc('xtick.major', pad=10);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);
    
    # X-Axis tick
    tick_str = []
    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))
    plt.xticks(tick_dt, tick_str)

    # Grid
    plt.grid(True)

    # Text
    fig.text(0.91, 0.72, 'X', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.61, 'M', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.50, 'C', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.39, 'B', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.28, 'A', fontsize=11, ha='left', va='center')

    fig.text(0.93, 0.65, "GOES-15 0.5-4.0 $\AA$", fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.93, 0.35, "GOES-15 0.5-4.0 $\AA$", fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])

    # Show or Save
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)

    return

def draw_goes_mag(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    import matplotlib.pyplot as plt
    #
    global color_list
    if (color == ""):
        color = color_list
    
    # Date list for X-Axis
    tick_dt = []
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + datetime.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')
    plt.clf()
    #plt.rc('text', usetex=True)
    
    # Title
    plt.title("GOES Magnetometer (1 minute data)")
    
    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
                fontsize=14)

    # Y-Axis
    plt.ylim([0, 200])
    plt.yscale('linear')
    plt.ylabel("NanoTesla [nT]")
    
    
    # ticks
    plt.rc('xtick.major', pad=10);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);

    # X-Axis Ticks
    tick_str = []
    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))
    plt.xticks(tick_dt, tick_str)

    


    # Grid
    plt.grid(True)
    
    # Text
    fig.text(0.92, 0.5, 'GOES 13 Hp Long. W 75', fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.95, 0.5, 'GOES 15 Hp Long. W 134', fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])
    

    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    return

def draw_goes_proton(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    import matplotlib.pyplot as plt
    #
    global color_list
    if (color == ""):
        color = color_list
    
    # Date list for X-Axis
    tick_dt = []
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + datetime.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')
    plt.clf()
    #plt.rc('text', usetex=True)
    
    # Title
    plt.title("GOES Proton Flux (1 minute data)")
    
    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
                fontsize=14)    

    # Y-Axis
    plt.ylim([1.0e-2, 1.0e4])
    plt.yscale('log')
    plt.ylabel("Particles cm$^{-2}$s$^{-1}$sr$^{-1}$")
    
    
    # Style for Ticks
    plt.rc('xtick.major', pad=10);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);

    # X-Axis Ticks
    tick_str = []
    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))
    plt.xticks(tick_dt, tick_str)
    
    
    # Grid
    plt.grid(True)
    
    # Text
    fig.text(0.93, 0.65, '$\ge$10 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[2])
    fig.text(0.93, 0.50, '$\ge$50 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.93, 0.35, '$\ge$100 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])
    
    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)

    
    return


def draw_goes_electron(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    import matplotlib.pyplot as plt
    #
    global color_list
    if (color == ""):
        color = color_list
    
    # Date list for X-Axis
    tick_dt = []
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + datetime.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')
    plt.clf()
    #plt.rc('text', usetex=True)
    
    # Title
    plt.title("GOES Electron Flux (1 minute data)")
    
    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
               fontsize=14)    
    
    # Y-Axis
    plt.ylim([1.0e-1, 1.0e7])
    plt.yscale('log')
    plt.ylabel("Particles cm$^{-2}$s$^{-1}$sr$^{-1}$")
    
    
    # Style for Ticks
    plt.rc('xtick.major', pad=10);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);
    
    # X-Axis Ticks
    tick_str = []
    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))
    plt.xticks(tick_dt, tick_str)
    
    
    # Grid
    plt.grid(True)
    
    # Text
    fig.text(0.93, 0.65, '$\ge$10 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[2])
    fig.text(0.93, 0.50, '$\ge$50 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.93, 0.35, '$\ge$100 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])
    
    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    
    return

if __name__=='__main__':
    dt = [datetime.datetime(2012, 01, 01, 0, 0, 0),
          datetime.datetime(2012, 01, 02, 0, 0, 0),
          datetime.datetime(2012, 01, 03, 0, 0, 0)]
    
    
    y = [2.0e-5, 2.0e-5, 2.0e-5]
    draw_goes_xray(dt, y, days=3)
    #draw_goes_xray(dt, y, file_path='xray.png')
    
    y = [10, 20, 30]
    draw_goes_mag(dt, y, days=3)
    #draw_goes_mag(dt, y, file_path='mag.png')
    
    y = [2.0e2, 2.0e1, 2.0e3]
    draw_goes_proton(dt, y, days=3)
    #draw_goes_proton(dt, y, file_path='proton.png')
    
    y = [2.0e2, 2.0e1, 2.0e3]
    draw_goes_electron(dt, y, days=3)
    #draw_goes_proton(dt, y, file_path='proton.png')