#!/usr/bin/python
'''
##
#
# Developed by Seonghwan Choi (shchoi@kasi.re.kr, http://www.choi.pro)
# 
#

__author__ = "Seonghwan Choi"
__copyright__ = "Copyright 2012, Korea Astronomy and Space Science"
__credits__ = ["Seonghwan Choi"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Seonghwan Choi"
__email__ = "shchoi@kasi.re.kr"
__status__ = "Production"

'''

# standard library
import calendar
from ctypes import *
import os
import string
from swpy.utils import datetime as dt
from swpy.utils import download as dl


# SpaeWeatherPy library
#import config as cnf
ERROR_INT = -99999

#
class CACTUS_CME(Structure):
    _fields_ = [#("begin_dt", c_double),
                #("end_dt", c_double),
                
                ("no", c_char_p),
                ("t0", c_char_p),
                ("dt0", c_char_p),
                ("pa", c_char_p),
                ("da", c_char_p),
                ("v", c_char_p),
                ("dv", c_char_p),
                ("minv", c_char_p),
                ("maxv", c_char_p),
                ("halo", c_char_p)]


# CACTUS
cactus_lasco_url = "http://sidc.oma.be/cactus/catalog/LASCO/"
cactus_secchia_url = "http://secchi.nrl.navy.mil/cactus/SECCHI-A/"
cactus_secchib_url = "http://secchi.nrl.navy.mil/cactus/SECCHI-B/"

DATA_DIR = 'data/sidc/cactus/'


# monthly files
# LASCO        
# V.2.5.0 (L0) : 1997. 05. ~ 2010. 06.
# V.2.5.0 (QL) : 2010. 07. ~
def download_cactus_lasco(begindate, enddate=""):
    begin_dt, end_dt = dt.trim(begindate, 3, 'start'),dt.trim(begindate, 3, 'end')

    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        # level0
        src1 = "%(url)s2_5_0/%(yyyy)04d/%(mm)02d/cmecat.txt"% \
            {"url":cactus_lasco_url, "yyyy":now_dt.year, "mm":now_dt.month}
        dst1 = DATA_DIR + "lasco/%(yyyy)04d/cactus_lasco_l0_%(yyyy)04d%(mm)02d.txt"% \
            {"yyyy":now_dt.year, "mm":now_dt.month}

        rv = dl.download_http_file(src1, dst1,overwrite=True)
        if (rv == True):
            print ("Downloaded %s."%src1)

        # quick look
        if (rv == False):
            src2 = "%(url)s2_5_0/qkl/%(yyyy)04d/%(mm)02d/cmecat.txt"% \
                {"url":cactus_lasco_url, "yyyy":now_dt.year, "mm":now_dt.month}
            dst2 = DATA_DIR + "lasco/%(yyyy)04d/cactus_lasco_ql_%(yyyy)04d%(mm)02d.txt"% \
                {"yyyy":now_dt.year, "mm":now_dt.month}
            
            rv = dl.download_http_file(src2, dst2,overwrite=True)
            if (rv == True):
                print ("Downloaded %s."%src2)

        #
        mr = calendar.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])

    return;

# monthly files
# COR2 : SECCHI-A and SECCHI-B
# Date : 2007. 4. ~

def download_cactus_cor2(begindate, enddate=""):
    begin_dt, end_dt = dt.trim(begindate, 3, 'start'),dt.trim(begindate, 3, 'end')
    
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        # COR2 SECCHI-A
        src = "%(url)s%(yyyy)04d/%(mm)02d/out/cmecat.txt"% \
                {"url":cactus_secchia_url, "yyyy":now_dt.year, "mm":now_dt.month}
        dst = "%(dir)s%(yyyy)04d/cactus_secchia_%(yyyy)04d%(mm)02d.txt"% \
                {"dir":cactus_cor2_dir, "yyyy":now_dt.year, "mm":now_dt.month}
        
        rv = dl.download_http_file(src, dst,overwrite=True)
        if (rv == True):
            print ("Downloaded %s."%src)
        
        # COR2 SECCHI-B
        src = "%(url)s%(yyyy)04d/%(mm)02d/out/cmecat.txt"% \
                {"url":cactus_secchib_url, "yyyy":now_dt.year, "mm":now_dt.month}
        dst = "%(dir)s%(yyyy)04d/cactus_secchib_%(yyyy)04d%(mm)02d.txt"% \
                {"dir":cactus_cor2_dir, "yyyy":now_dt.year, "mm":now_dt.month}
        
        rv = dl.download_http_file(src, dst,overwrite=True)
        if (rv == True):
            print ("Downloaded %s."%src)
        
        #
        mr = calendar.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
    
    return;

def load_cactus_lasco(begindate, enddate=""):
    
    begin_dt, end_dt = dt.trim(begindate, 3, 'start'), dt.trim(begindate, 3, 'end')
    
    # cme_no t0 dt0 pa da v dv minv maxv halo
    list = []    

    #
    now_dt = begin_dt.replace(day=1)
    while ( now_dt <= end_dt ):
        
        # level0
        file_path_l0 = "%(dir)s%(yyyy)04d/cactus_lasco_l0_%(yyyy)04d%(mm)02d.txt"% \
            {"dir":cactus_lasco_dir, "yyyy":now_dt.year, "mm":now_dt.month}

        # quick look
        file_path_ql = "%(dir)s%(yyyy)04d/cactus_lasco_ql_%(yyyy)04d%(mm)02d.txt"% \
                {"dir":cactus_lasco_dir, "yyyy":now_dt.year, "mm":now_dt.month}
    
        # select file path for level0 or quicklook
        file_path = ""
        if ( os.path.exists(file_path_l0) == True):
            file_path = file_path_l0
        else:
            if ( os.path.exists(file_path_ql) == True):
                file_path = file_path_ql
            else:
                print "The file does not exist, %(l0)s or %(ql)s."%{"l0":file_path_l0, "ql":file_path_ql}

        if (file_path == ""):
            # next month
            mr = calendar.monthrange(now_dt.year, now_dt.month)
            now_dt = now_dt + dt.timedelta(days=mr[1])
            continue;

        print "Load the file, " + file_path + "."

        # Open a file
        file = open(file_path, "r")
        
        # Skip headers
        for line in file:
            if (line[0:5] == "# CME"):
                break;
            
        # Read records
        for line in file:
            
            if (len(line) < 62):
                break;

            #
            cme_no = line[2:6]
            t0 = line[7:23]
            dt0 = line[24:28]

            pa = line[29:33]
            da = line[34:38]
            v = line[39:44]
            dv = line[45:50]
            minv = line[51:56]
            maxv = line[57:62]
            halo = line[63:67]

            #  
            dt2 = dt.datetime.strptime(t0, "%Y/%m/%d %H:%M")


            if (dt2 < begin_dt or end_dt < dt2):
                continue

            #
            item = CACTUS_CME(cme_no, t0, dt0, pa, da, v, dv, minv, maxv, halo)
                
            
            list.append(item)

            #print item.no, item.t0
                

        # Close the file
        file.close()
                

        # next month
        mr = calendar.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
     
    # Sort order
    list = sorted(list, key=lambda CACTUS_CME: CACTUS_CME.t0)

    return list

def load_cactus_secchia(begindate, enddate=""):
    begin_dt, end_dt = dt.trim(begindate, 3, 'start'),dt.trim(begindate, 3, 'end')
    
    # cme_no t0 dt0 pa da v dv minv maxv halo
    list = []    
    
    #
    now_dt = begin_dt
    now_dt = now_dt.replace(day=1)
    while ( now_dt <= end_dt ):
        # file_path
        file_path = "%(dir)s%(yyyy)04d/cactus_secchia_%(yyyy)04d%(mm)02d.txt"% \
            {"dir":cactus_cor2_dir, "yyyy":now_dt.year, "mm":now_dt.month}
                
        if ( os.path.exists(file_path) == False):
            # next month
            mr = calendar.monthrange(now_dt.year, now_dt.month)
            now_dt = now_dt + dt.timedelta(days=mr[1])
            continue;
        
        print "Load the file, " + file_path + "."
        
        # Open a file
        file = open(file_path, "r")
        
        # Skip headers
        for line in file:
            if (line[0:5] == "# CME"):
                break;
        
        # Read records
        for line in file:
            
            if (len(line) < 62):
                break;
            
            #
            cme_no = line[2:6]
            t0 = line[7:23]
            dt0 = line[24:28]
            
            pa = line[29:33]
            da = line[34:38]
            v = line[39:44]
            dv = line[45:50]
            minv = line[51:56]
            maxv = line[57:62]
            halo = line[63:67]
            
            #  
            dt2 = dt.datetime.strptime(t0, "%Y/%m/%d %H:%M")
            
            
            if (dt2 < begin_dt or end_dt < dt2):
                continue
            
            #
            item = CACTUS_CME(cme_no, t0, dt0, pa, da, v, dv, minv, maxv, halo)
            
            
            list.append(item)
        
        #print item.no, item.t0
        
        
        # Close the file
        file.close()
        
        
        # next month
        mr = calendar.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
    
    # Sort order
    list = sorted(list, key=lambda CACTUS_CME: CACTUS_CME.t0)
    
    return list


def load_cactus_secchib(begindate, enddate=""):
    begin_dt, end_dt = dt.trim(begindate, 3, 'start'),dt.trim(begindate, 3, 'end')
    
    # cme_no t0 dt0 pa da v dv minv maxv halo
    list = []    
    
    #
    now_dt = begin_dt
    now_dt = now_dt.replace(day=1)
    while ( now_dt <= end_dt ):
        # file_path
        file_path = "%(dir)s%(yyyy)04d/cactus_secchib_%(yyyy)04d%(mm)02d.txt"% \
            {"dir":cactus_cor2_dir, "yyyy":now_dt.year, "mm":now_dt.month}
        
        if ( os.path.exists(file_path) == False):
            # next month
            mr = calendar.monthrange(now_dt.year, now_dt.month)
            now_dt = now_dt + dt.timedelta(days=mr[1])
            continue;
        
        print "Load the file, " + file_path + "."
        
        # Open a file
        file = open(file_path, "r")
        
        # Skip headers
        for line in file:
            if (line[0:5] == "# CME"):
                break;
        
        # Read records
        for line in file:
            
            if (len(line) < 62):
                break;
            
            #
            cme_no = line[2:6]
            t0 = line[7:23]
            dt0 = line[24:28]
            
            pa = line[29:33]
            da = line[34:38]
            v = line[39:44]
            dv = line[45:50]
            minv = line[51:56]
            maxv = line[57:62]
            halo = line[63:67]
            
            #  
            dt2 = dt.datetime.strptime(t0, "%Y/%m/%d %H:%M")
            
            
            if (dt2 < begin_dt or end_dt < dt2):
                continue
            
            #
            item = CACTUS_CME(cme_no, t0, dt0, pa, da, v, dv, minv, maxv, halo)
            
            
            list.append(item)
        
        #print item.no, item.t0
        
        
        # Close the file
        file.close()
        
        
        # next month
        mr = calendar.monthrange(now_dt.year, now_dt.month)
        now_dt = now_dt + dt.timedelta(days=mr[1])
    
    # Sort order
    list = sorted(list, key=lambda CACTUS_CME: CACTUS_CME.t0)

    return list


if __name__ == '__main__':
    download_cactus_lasco("199705", "201301");
    download_cactus_cor2("200704", "201301");


    l = load_cactus_lasco("19970501", "20130131");
    for item in l:
        print item.t0
    
    a = load_cactus_secchia("20070401", "20130131");
    for item in a:
        print item.t0
    
    b = load_cactus_secchib("20070401", "20130131");
    for item in b:
        print item.t0
