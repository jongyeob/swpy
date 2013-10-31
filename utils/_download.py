#!/usr/bin/python

##
#
# Developed by Seonghwan Choi (shchoi@kasi.re.kr, http://www.choi.pro)
# 
#
#
##


__author__ = "Seonghwan Choi"
__copyright__ = "Copyright 2012, Korea Astronomy and Space Science"
__credits__ = ["Seonghwan Choi"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Seonghwan Choi"
__email__ = "shchoi@kasi.re.kr"
__status__ = "Production"


import os
import string
import types
import math

import datetime
import time
import calendar

import socket
import httplib
import ftplib

    
##
def alert_message(message):
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + message)


## Convert string (yyyymmdd_HHMMSS) to datetime
'''
def str2dt(param, last=False):
    yyyy = 1975
    mm = 1
    dd = 1
    HH = 0
    MM = 0
    SS = 0
    
    if (isinstance(param, datetime.datetime) == True):
        param = param.replace(microsecond=0)
        return param
    elif (isinstance(param, datetime.date) == True):
        return datetime.datetime(param.year, param.month, param.day, 0, 0, 0)
    elif (isinstance(param, str) == False):
        alert_message("The param is not a string in str2dt().")
        return False

    try:
        if (param.__len__() == 4):
            yyyy = int(param)
            if (last == True):
                mm = 12
                dd = 31
                HH = 23
                MM = 59
                SS = 59
        elif (param.__len__() == 6):
            yyyy = int(param[0:4])
            mm = int(param[4:6])
            if (last == True):
                dd = calendar.monthrange(yyyy, mm)[1]
                HH = 23
                MM = 59
                SS = 59
        elif (param.__len__() == 8):
            yyyy = int(param[0:4])
            mm = int(param[4:6])
            dd = int(param[6:8])
            if (last == True):
                HH = 23
                MM = 59
                SS = 59
        elif (param.__len__() == 11):
            yyyy = int(param[0:4])
            mm = int(param[4:6])
            dd = int(param[6:8])
            HH = int(param[9:11])
            if (last == True):
                MM = 59
                SS = 59
        elif (param.__len__() == 13):
            yyyy = int(param[0:4])
            mm = int(param[4:6])
            dd = int(param[6:8])
            HH = int(param[9:11])
            MM = int(param[11:13])
            if (last == True):
                SS = 59
        elif (param.__len__() == 15):
            yyyy = int(param[0:4])
            mm = int(param[4:6])
            dd = int(param[6:8])
            HH = int(param[9:11])
            MM = int(param[11:13])
            SS = int(param[13:15])
        else:
            alert_message("The format should be yyyymmdd_HHMMSS in str2dt().")
            return False
    except TypeError:
        alert_message("The format should be yyyymmdd_HHMMSS in str2dt().")
        return False
    
    try:
        dt = datetime.datetime(yyyy, mm, dd, HH, MM, SS)
    except ValueError:
        alert_message("datetime.datetime() ValueError in str2dt().")
        return False
    
    return dt

def str2dt(begindate, enddate):
    #
    if (enddate == 0):
        enddate = util.str2dt(begindate, last=True)
    else:
        enddate = util.str2dt(enddate, True)
    
    begindate = util.str2dt(begindate)

    return dt1, dt2
'''

    #def str2time(begindate, enddate):
def str2dt(begindate, enddate):

    begin_dt = 0
    end_dt = 0
    
    if (enddate == ""):
        enddate = begindate
    
    # Format : yyyymmdd
    if (len(begindate) == 8 and len(enddate) == 8):
        begin_dt = datetime.datetime.strptime(begindate, "%Y%m%d")
        end_dt = datetime.datetime.strptime(enddate, "%Y%m%d")
        end_dt = end_dt.replace(hour=23, minute=59, second=59)

    # Format : yyyymm
    if (len(begindate) == 6 and len(enddate) == 6):
        begin_dt = datetime.datetime.strptime(begindate, "%Y%m")
        end_dt = datetime.datetime.strptime(enddate, "%Y%m")

        mr = calendar.monthrange(end_dt.year, end_dt.month)
        end_dt = end_dt.replace(day = mr[1], hour=23, minute=59, second=59)

    # Format : yyyy
    if (len(begindate) == 4 and len(enddate) == 4):
        begin_dt = datetime.datetime.strptime(begindate, "%Y")
        end_dt = datetime.datetime.strptime(enddate, "%Y")
        end_dt = end_dt.replace(month=12, day=31, hour=23, minute=59, second=59)
    
    return begin_dt, end_dt


##
# The filepath should be ended with '/'.
# If not, the last part of the filepath will be considered as a file name.
# It will create a directory, '/abc/def/', when the filepath is '/abc/def/ghi'.
# It will create a directory, '/abc/def/ghi/', when the filepath is '/abc/def/ghi/'.
#
def make_directory(filepath):
    filepath = os.path.dirname(filepath) + "/"
    if (os.path.exists(filepath) == False):
        os.makedirs(os.path.dirname(filepath))
    return True

def download_ftp_file(src_url, dst_path, overwrite=False, trials=5, id="", pw=""):
    
    
    #if (os.path.isfile(dst_path) == True and overwrite == False):
    #    print("The file already exists, %s"%dst_path)
    #    return True

    
    if (src_url.find("ftp://") != 0):
        print("src_url is invalid url, " + src_url + ".")
        return False
    
    i = src_url.find("/", 6)
    if (i < 8):
        print("src_url is invalid url, " + src_url + ".")
        return False

    remote_domain_name = src_url[6:i]
    remote_file_path = src_url[i:]

    # print remote_domain_name
    # print remote_file_path

    try:

        ftp = ftplib.FTP(remote_domain_name)
        ftp.login(id, pw)
        

        # If the file exists and its file size is the same.
        if (os.path.isfile(dst_path) == True):
            rs = ftp.size(remote_file_path)
            ls = os.path.getsize(dst_path)
            
            #print rs, ls

            if (rs == ls and overwrite == False):
                ftp.quit()
                print "Already exist, %s."%(dst_path)
                return True

        # In the case,
        # 1. The local file does not exist.
        # 2. OVERWRITE = TRUE
        # 3. The file sizes on a remote path and a local path are different.
        make_directory(dst_path)
        file = open(dst_path, "wb")

        ftp.retrbinary("RETR " + remote_file_path, file.write)

        file.close()
        ftp.quit()
        print "Downloaded, %s."%(src_url)
    except socket.error, e:
        alert_message("Socket exception error, %s."%e)
        return False


    return True
    

def download_http_file(src_url, dst_path=False, overwrite=False, trials=5):
    
    if (dst_path != False):
        if (os.path.isfile(dst_path) == True and overwrite == False):
            print("The file already exists, %s"%dst_path)
            return True
    
    if (src_url.find("http://") != 0):
        print("src_url is invalid url, " + src_url + ".")
        return False
    
    i = src_url.find("/", 7)
    if (i < 9):
        print("src_url is invalid url, " + src_url + ".")
        return False
 
    domain_name = src_url[7:i]
    file_path = src_url[i:]
            

    contents = ""
    t = 0
    for t in range(1, trials):
        contents = ""
        
        try:
            conn = httplib.HTTPConnection(domain_name)
            conn.request("GET", file_path)
            r = conn.getresponse()
            if (r.status >= 200 or r.status < 300 or    # Success
                r.status == 302):                       # Found
                contents = r.read()
                conn.close()
            else:
                print(r.status, r.reason)
                print("Can not download the file, " + src_url + ".")
                conn.close()
            
            t = 0   # if success
            break
        except httplib.HTTPException, msg:
            #nFails = nFails + 1
            alert_message("HTTPException")
        except httplib.NotConnected, msg:
            #nFails = nFails + 1
            alert_message("NotConnected")
        except httplib.InvalidURL, msg:
            #nFails = nFails + 1
            alert_message("InvalidURL")
        except httplib.UnknownProtocol, msg:
            #nFails = nFails + 1
            alert_message("UnknownProtocol")
        except httplib.UnknownTransferEncoding, msg:
            #nFails = nFails + 1
            alert_message("UnknownTransferEncoding")
        except httplib.UnimplementedFileMode, msg:
            #nFails = nFails + 1
            alert_message("UnimplementedFileMode")
        except httplib.IncompleteRead, msg:
            #nFails = nFails + 1
            alert_message("IncompleteRead")
        except httplib.ImproperConnectionState, msg:
            #nFails = nFails + 1
            alert_message("ImproperConnectionState")
        except httplib.CannotSendRequest, msg:
            #nFails = nFails + 1
            alert_message("CannotSendRequest")
        except httplib.CannotSendHeader, msg:
            #nFails = nFails + 1
            alert_message("CannotSendHeader")
        except httplib.ResponseNotReady, msg:
            #nFails = nFails + 1
            alert_message("ResponseNotReady")
        except httplib.BadStatusLine, msg:
            #nFails = nFails + 1
            alert_message("BadStatusLine")
        except socket.error, e:
            alert_message("Socket exception error, %s."%e)
        # finally:
            #nFails = nFails + 1
        #alert_message("Unknown exception in DownloadHttpFile().")
        
        alert_message("It will be start again after several seconds in download_http_file().")
        time.sleep(5)

    if (t > 0):
        return False
        
    if (dst_path == False):
        return contents

    if (contents == ""):
        return False


    #print (strDstFile)
    
    make_directory(dst_path)
    

    f = open(dst_path, "w")
    f.write(contents)
    f.close()

    #print ("Success downloading the file, " + strSrcUrl + ".")

    return True

def load_http_file(url):
    contents = ""
    
    if (url.find("http://") != 0):
        print("The url is invalid, " + url + ".")
        return False
    
    i = url.find("/", 7)
    if (i < 9):
        print("The url is invalid, " + url + ".")
        return False

    domain_name = url[7:i]
    file_path = url[i:]

    conn = httplib.HTTPConnection(domain_name)
    conn.request("GET", file_path)


    r = conn.getresponse()

    #print (r.getheaders())
    
    if r.status == 301:
        contents = r.read()
    elif r.status != 200:
        print(r.status, r.reason)
        print("Can not download the file, " + url + ".")
        conn.close()
        return False
    else:
        contents = r.read()

    conn.close()

    return contents

def get_list_from_html(contents, ext_list = None):
    strList = []
    
    # Make strExtList a list object if strExtList is not.
    if( ext_list != None):
        if (isinstance(ext_list, types.ListType) != True ):
            ext_list = [ext_list]
    
    
    
    iBegin = 0
    iEnd = 0
    
    i = 0
    
    while True:
        iBegin = string.find(contents,  "<a href=\"", iEnd)
        iBegin = iBegin + 9 # 9 is the length of "<a href=\"".
        if (iBegin == -1 or iBegin < iEnd):
            break
        
        iEnd = string.find(contents, "\"", iBegin)
        if (iEnd == -1):
            break
        
        strLink = contents[iBegin:iEnd]
        
        if (ext_list != None):
            for strExtName in ext_list:
                if(string.find(strLink, "." + strExtName) != -1):
                    strList.append(strLink)
        else:
            strList.append(strLink)
    
    #print strList[0]
    
    
    #iBegin = iEnd = iEnd + 1
    
    #        i = i+1
    #        if (i > 80000):
    #break;
    
    
    return strList

MODE_ALL = 0
MODE_DIRECTORY = 1
MODE_FILE = 2

def get_list_from_ftp(ftp_domain, ftp_id, ftp_pw, ftp_dir, mode=MODE_ALL):

    list = []

    try:
        ftp = ftplib.FTP(ftp_domain, ftp_id, ftp_pw)        
        ftp.login(ftp_id, ftp_pw)
        ftp.cwd(ftp_dir)
        ftp.retrlines("LIST", list.append) #, list.append)
        ftp.quit()
    except ftplib.all_errors, e:
        err_string = str(e).split(None, 1)
        print err_string

        return [], []
    
    #
    file_names = []
    file_size = []
    for line in list:
        if ((mode == MODE_DIRECTORY and line[0] != "d") or
            (mode == MODE_FILE and line[0] == "d") ):
            continue
        
        file_size.append(line.split()[4])
        file_names.append(line.split()[-1])


    return file_names, file_size


def save_list(filepath, list):
    make_directory(filepath)
    
    f = open(filepath, "w")
    for line in list:
        f.write(line + "\n")
    f.close()

    return True


def save_list_2(filepath, list):
    make_directory(filepath)

    list.sort()
    f = open(filepath, "w")
    
    for line in list:
        f.write(get_filename(line) + "\n")
    
    f.close()

    return True

def get_filename(filepath):
    import string
    
    index = string.rfind(filepath, '/')    # Return -1 on failure
    filename = filepath[index+1:]

    return filename


def num2str(num):
    str_num = ""

    if (num >= 1000000000000):
        temp = int(math.floor(num / 1000000000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000000000

    if (num >= 1000000000):
        temp = int(math.floor(num / 1000000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000000

    if (num >= 1000000):
        temp = int(math.floor(num / 1000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000

    if (num >= 1000):
        temp = int(math.floor(num / 1000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000

    if (len(str_num) > 0): str_num += "%03d"%(num)
    else: str_num += "%d"%(num)

    return str_num


