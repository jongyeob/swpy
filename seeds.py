##
##
## Real-tme Dst index : 1967 - 2008
## Final Dst index :2009 - current
##

# standard library
import calendar
import datetime
import os
import string
import swpy
import time

import matplotlib.pyplot as plt
import swgraph as swg
import utilities as util


# SpaeWeatherPy library
seeds_url = "http://spaceweather.gmu.edu/seeds/"
seeds_dir = swpy.data_dir + "gmu/seeds/"; 


def download_cme(begindate, enddate=""):
    begin_dt, end_dt = util.str2dt(begindate, enddate)
    
    
    
    #
    last_dt_file = "http://spaceweather.gmu.edu/seeds/detection/lastdet.check"
    contents = util.download_http_file(last_dt_file)
    last_dt = datetime.datetime.strptime(contents[0:19], "%Y/%m/%d %H:%M:%S")
    
    
    #
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        #
        file_url = "http://spaceweather.gmu.edu/seeds/detection/%(yyyy)s/%(mm)s/monthly.txt"%{
            "yyyy":now_dt.strftime("%Y"),
            "mm":now_dt.strftime("%m")}

        file_path = "%(dir)s%(yyyy)s/%(yyyy)s%(mm)s/%(yyyy)s%(mm)s_seeds_cme.txt"%{
            "dir":seeds_dir,
            "yyyy":now_dt.strftime("%Y"),
            "mm":now_dt.strftime("%m")}
        
        # Quick Look
        if (now_dt > last_dt):
            file_url = "http://spaceweather.gmu.edu/seeds/realtime/%(yyyy)s/%(mm)s/monthly.txt"%{
                "yyyy":now_dt.strftime("%Y"),
                "mm":now_dt.strftime("%m")}

            file_path = "%(dir)s%(yyyy)s/%(yyyy)s%(mm)s/%(yyyy)s%(mm)s_seeds_cme_ql.txt"%{
                "dir":seeds_dir,
                "yyyy":now_dt.strftime("%Y"),
                "mm":now_dt.strftime("%m")}
            

        # Download a file.
        downloaded = True
        rv = util.download_http_file(file_url, file_path, overwrite=True)
        if (rv == True):
            print "Download %s."%(file_path)

            # Remove a file, if there is a problem.
            f = open(file_path, "r");
            line = f.readlines();
            f.close();
            if (line[0][0:4] != now_dt.strftime("%Y") ):
                print "Remove %s."%(file_path)
                os.remove(file_path)
                downloaded = False
        else:
            print "Fail to download %s."%(file_path)
            downloaded = False

        #
        if (downloaded == True):
            f = open(file_path, "r")
            lines = f.readlines()
            f.close()
            
            for line in lines:
                yyyymmdd  = line[0:4] + line[5:7] + line[8:10]
                hh = line[11:13]
                mm = line[14:16]
                ss = line[17:19]
                p = line[24:27]
                w = line[28:31]
                v = line[32:37]

                # 20130101.002406.w009.v0344.p058.txt
                cme_file_name = "%(yyyymmdd)s.%(hh)s%(mm)s%(ss)s.w%(w)03d.v%(v)04d.p%(p)03d.txt"%{
                        "yyyymmdd":yyyymmdd,
                        "hh":hh,
                        "mm":mm,
                        "ss":ss,
                        "w":int(w),
                        "v":int(v),
                        "p":int(p)}
                
                file_url = "http://spaceweather.gmu.edu/seeds/detection/%(yyyy)s/%(mm)s/%(fn)s"%{
                        "yyyy":yyyymmdd[0:4],
                        "mm":yyyymmdd[4:6],
                        "fn":cme_file_name}

                file_path = "%(dir)s%(yyyy)s/%(yyyy)s%(mm)s/%(fn)s"%{
                    "dir":seeds_dir,
                    "yyyy":yyyymmdd[0:4],
                    "mm":yyyymmdd[4:6],
                    "fn":cme_file_name}

                # Quick Look
                if (now_dt > last_dt):
                    cme_ql_file_name = "%(yyyymmdd)s.%(hh)s%(mm)s%(ss)s.w%(w)03d.v%(v)04d.p%(p)03d_ql.txt"%{
                        "yyyymmdd":yyyymmdd,
                        "hh":hh,
                        "mm":mm,
                        "ss":ss,
                        "w":int(w),
                        "v":int(v),
                        "p":int(p)}

                    file_url = "http://spaceweather.gmu.edu/seeds/realtime/%(yyyy)s/%(mm)s/%(fn)s"%{
                        "yyyy":yyyymmdd[0:4],
                        "mm":yyyymmdd[4:6],
                        "fn":cme_file_name}

                    file_path = "%(dir)s%(yyyy)s/%(yyyy)s%(mm)s/%(fn)s"%{
                        "dir":seeds_dir,
                        "yyyy":yyyymmdd[0:4],
                        "mm":yyyymmdd[4:6],
                        "fn":cme_ql_file_name}
    
                # Download CME
                rv = util.download_http_file(file_url, file_path, overwrite=True)
                if (rv == True):
                    print "Download %s."%(file_path)
                    
                    # Remove a file, if there is a problem.
                    f = open(file_path, "r");
                    line = f.readlines();
                    f.close();
                    if (line[0][0] == "<" ):    # if html code
                        print "Remove %s."%(file_path)
                        os.remove(file_path)
                        downloaded = False
                else:
                    print "Fail to download %s."%(file_path)


                    

        #
        mr = calendar.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + datetime.timedelta(days=mr[1])

    return True

def load_cme(begindate, enddate=""):
    #
    begin_dt, end_dt = util.str2dt(begindate, enddate)
    
    #
    data = {"t0":[], "cpa":[], "w":[], "v":[], "a":[]}
    

    #
    now_dt = begin_dt.replace(day=1)
    while ( now_dt <= end_dt ):

        file_path = "%(dir)s%(yyyy)s/%(yyyy)s%(mm)s/%(yyyy)s%(mm)s_seeds_cme.txt"%{
            "dir":seeds_dir,
            "yyyy":now_dt.strftime("%Y"),
            "mm":now_dt.strftime("%m")}
        
        # Quick Look
        if (os.path.exists(file_path) == False):
            file_path = "%(dir)s%(yyyy)s/%(yyyy)s%(mm)s/%(yyyy)s%(mm)s_seeds_cme_ql.txt"%{
                "dir":seeds_dir,
                "yyyy":now_dt.strftime("%Y"),
                "mm":now_dt.strftime("%m")}

        if (os.path.exists(file_path) == True):
            f = open(file_path, "r")
            lines = f.readlines()
            f.close()

            for line in lines:
                dt = datetime.datetime.strptime(line[0:19], "%Y/%m/%d %H:%M:%S")
                cpa = int(line[24:27])
                w = int(line[28:31])
                v = int(line[32:37])
                a = line[38:45]
          
                if (a == "-------"):
                    a = 99999.9
                else:
                    a = float(a)

                if (begin_dt <= dt and dt <= end_dt):
                    data["t0"].append( dt )
                    data["cpa"].append( cpa )
                    data["w"].append( w )
                    data["v"].append( v )
                    data["a"].append( a )
    
        #
        now_dt = now_dt.replace(day=1)
        now_dt = now_dt + datetime.timedelta(days=32)
        now_dt = now_dt.replace(day=1)
    
    return data

