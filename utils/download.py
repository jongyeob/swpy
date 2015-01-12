'''
__author__ = "Seonghwan Choi"
__copyright__ = "Copyright 2012, Korea Astronomy and Space Science"
__credits__ = ["Seonghwan Choi","Jongyeob Park"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Seonghwan Choi"
__email__ = "shchoi@kasi.re.kr"
__status__ = "Production"
'''
import time
import datetime
import ftplib
from httplib import HTTPException
import httplib
import math
from os import path, makedirs
import os
import socket
import string
import swpy
import sys
import time
import urllib2
from urllib2 import urlopen, HTTPError

import datetime
from utils import make_path, make_dirs, alert_message
import threading

g_callback_last_msg = ''
import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(10)

_download_pools = []



class AutoTempFile():
    _filepath = None
    
    def __init__(self,filepath=None):
        self._filepath = filepath

        if self._filepath is None:
            now = datetime.datetime.now()
            print now
            self._filepath = now.strftime("%Y%m%d_%H%M%S_%f.temp")  
            
    def get_path(self):
        return self._filepath
    
    def __del__(self):
        try:
            if os.path.exists(self._filepath) == True:
                os.remove(self._filepath)
        except:
            LOG.error("File removing error!")

class DownloadThread(threading.Thread):
    '''
    class for mulitthread of download_http_file
    '''
    def __init__(self,src,dst=None,post_args=None,overwrite=False,trials=3):
        threading.Thread.__init__(self)
                
        self.src = src
        self.dst = dst
        self.post_args = post_args
        self.overwrite = overwrite
        self.trials = trials
        self.rval = None
        
    def run(self):
        
        self.rval = download_http_file(self.src, self.dst, self.post_args, self.overwrite, self.trials)


def download_http_file(src_url,dst_path=None,post_args=None,overwrite=False,trials=3):
    '''
    Download a file on internet. return when a file saved to loacl is existed.
    
    :param string src_url: URL
    :param string dst_path: local path
    :param string post_args: arguments for POST method
    :param bool overwrite: if ture, local file will be overwritten.
    :param int trials: method will be terminated in trails number

    :return: bool
    '''
    # Check existing file
    if dst_path is not None:
        dst_path = path.normpath(dst_path)
        dst_exist = path.exists(dst_path) 
        if  dst_exist == True and overwrite == False:
            LOG.debug('Already exist, %s'%(dst_path))
            return True
   

    i = src_url.find("/", 7)
    if (src_url.find("http://") != 0 and \
        i < 9 ):
        raise ValueError("Url is invalid, " + src_url)
    
    
    domain_name = src_url[7:i]
    file_path = src_url[i:]
    
    headers = {"Content-type": "application/x-www-form-urlencoded",\
               "Accept": "text/plain"}
   
    t = 0
    is_response = False
    while(not is_response and t < trials): 
        
        contents = ""
        try:
            conn = httplib.HTTPConnection(domain_name,timeout=75)
            
            if(post_args != None):
                conn.request("POST", file_path, post_args,headers)
            else:
                conn.request("GET", file_path)
            
            r = conn.getresponse()

            if r.status == 200:
                contents = r.read()
            elif r.status in [300, 301, 302, 303, 307]:
                new_loc  = r.getheader('Location')
                contents = download_http_file(new_loc,None,post_args,overwrite,trials-1)
            else:
                LOG.error("HTTP response error : %d, %s"%(r.status, r.reason))

            is_response = True
 
        except Exception as err:
            LOG.error("Error : %s"%str(err))
            t += 1
        finally:
            conn.close()
        
        if not is_response:
            LOG.debug("Re-trying...(%d/%d)"%(t,trials))
            time.sleep(5)
   
    # File saving... 
    if dst_path is not None:
        if contents == '':
            return False

        dst_path2 = make_path(dst_path) + '.down'
        try:
            with open(dst_path2, "wb") as f:
                f.write(contents)
            if path.exists(dst_path) == True:
                os.remove(dst_path)              
            os.rename(dst_path2, dst_path)

            return True
        except Exception as err:
            LOG.error("File Save error! - %s"%str(err))
            return False


    return contents

def get_list_from_html(contents, ext_list = None):
    strList = []
    
    # Make strExtList a list object if strExtList is not.
    if( ext_list != None):
        if (isinstance(ext_list, list) != True ):
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


def download_ftp_file(src_url, dst_path, overwrite=False, trials=5, login_id="", login_pw=""):
    
    
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
        ftp.login(login_id, login_pw)
        

        # If the file exists and its file size is the same.
        if (os.path.isfile(dst_path) == True):
            rs = ftp.size(remote_file_path)
            ls = os.path.getsize(dst_path)
            
            #print rs, ls

            if (rs == ls and overwrite == False):
                ftp.quit()
                LOG.info("Already exist, %s."%(dst_path))
                return True

        # In the case,
        # 1. The local file does not exist.
        # 2. OVERWRITE = TRUE
        # 3. The file sizes on a remote path and a local path are different.
        #fw = open(make_path(dst_path), "wb")
	with open(make_path(dst_path), 'wb') as fw:
		ftp.retrbinary("RETR " + remote_file_path, fw.write)
	#file.close()
        
        ftp.quit()
        print "Downloaded, %s."%(src_url)
    except socket.error, e:
        alert_message("Socket exception error, %s."%e)
        return False


    return True


MODE_ALL = 0
MODE_DIRECTORY = 1
MODE_FILE = 2

def get_list_from_ftp(ftp_domain, ftp_id, ftp_pw, ftp_dir, mode=MODE_ALL):

    li = []

    try:
        ftp = ftplib.FTP(ftp_domain, ftp_id, ftp_pw)        
        ftp.login(ftp_id, ftp_pw)
        ftp.cwd(ftp_dir)
        ftp.retrlines("LIST", li.append) #, list.append)
        ftp.quit()
    except ftplib.all_errors, e:
        err_string = str(e).split(None, 1)
        print err_string

        return [], []
    
    #
    file_names = []
    file_size = []
    for line in li:
        if ((mode == MODE_DIRECTORY and line[0] != "d") or
            (mode == MODE_FILE and line[0] == "d") ):
            continue
        
        file_size.append(line.split()[4])
        file_names.append(line.split()[-1])


    return file_names, file_size

if __name__ =='__main__':
    # ## Configuration
    # src = "http://www.swpc.noaa.gov/ftpdir/latest/27DO.txt"
    # dst = './a/test.txt'
    # 
    # 
    # print "No dstination path"
    # print dl.download_http_file(src)
    # 
    # ##
    # print "TEST : 404 Error"
    # print dl.download_http_file(src[:-2], dst)
    # 
    # ##
    # print "TEST : Download"
    # 
    # print dl.download_http_file(src,dst)
    # if(os.path.exists(src) == True):
    #     print src + 'is exists'
    # 
    # ##
    # print "TEST : Already exists"
    # try:
    #     dl.download_http_file(src,dst,overwrite=False)
    # except Exception as err:
    #     print err
    
    # print 'TEST : DownloadPool'
    # pool = DownloadPool()
    # print pool.recieving
    # pool.close()
    # print pool.recieving 
    
    print "TEST: AutoTempFile"
    
    temp_file = AutoTempFile()
    print temp_file.get_path()
    
    print "end"
