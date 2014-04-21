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

_download_pools = []

TEMP_DIR = swpy.TEMP_DIR

class AutoTempFile():
    _filepath = None
    
    def __init__(self,filepath=None):
        self._filepath = filepath

        if self._filepath is None:
            now = datetime.datetime.now()
            print now
            self._filepath = TEMP_DIR + '/' + now.strftime("%Y%m%d_%H%M%S_%f.temp")  
            
    def get_path(self):
        return self._filepath
    
    def __del__(self):
        try:
            if os.path.exists(self._filepath) == True:
                os.remove(self._filepath)
        except:
            LOG.error("File removing error!")

class DownloadPool():
    '''
    Class for download file list. 
    '''
    def __init__(self,max_pool=10,iter_obj=None):
        self.recieving = [False]
        self._pool_thread = None
        self._pool = []
        self._max = max_pool
                        
        if iter_obj is not None:
            self._pool.extend(iter_obj)
            
    def start(self,output_list,overwrite=False,trials=3,max_thread=8):
        if self.recieving[0] == False : 
            self.recieving[0] = True
        else:
            LOG.warn("Download Pool has been already started")
            return False
        
        assert self._pool_thread == None, 'Thread is not normally terminated'
        
        self._pool_thread = threading.Thread(target=_pool_thread,\
                                              args=(self.recieving,self._pool,output_list,overwrite,trials,max_thread))
        self._pool_thread.start()
        assert self._pool_thread != None, 'Thread is not created'
        
        return True        
    def append(self,src,dst):
        
        while(len(self._pool) > self._max and self._pool_thread.isAlive() == True):
            time.sleep(0.1)
            
        if(self._pool_thread.isAlive() == False):
            return False
        
        self._pool.append((src,dst))
               
        
    def close(self):
        if self.recieving[0] == True:
            self.recieving[0] = False
            #print 'id(self.recieving) : %d'%(id(self.recieving))
        else:
            LOG.warn("Download Pool was not started")
            return False
        
        assert self._pool_thread != None, 'Thread is not normally terminated before closing itself'
        
        while(self._pool_thread.isAlive() == True):
            print ("Waiting to exit a thread")
            self._pool_thread.join(1)
        
        self._pool_thread = None
        #print ("pool_thread end")
            
        
        return True
def _pool_thread(r,input_pool,output_list=[],overwrite=False,trials=3,max_thread=3):
    '''
    Download files in pool class. when status of pool is end, pool count is 0
    This function will be terminated. return number of download files
    '''
    assert type(input_pool) == list, 'Wrong input_pool type. must be download_pool'
    
    threads = []
    
    finish = False
    while(not finish):
        #print "r",r,'id',id(r)
        try:
            if r[0] == False and len(input_pool) == 0 and len(threads) == 0:
                finish = True
        
            if len(threads) < max_thread and len(input_pool) > 0:
                src,dst = input_pool.pop()
                th = DownloadThread(src,dst,None,overwrite,trials)
                threads.append(th)
                th.start()
                
            for th in threads:
                if(th.isAlive() == False):
                    output_list.append((th.src,th.dst,th.rval)) 
                    threads.remove(th)
            
        except:
            #print ('parent(%s),this(%s),Threads(%d),Pool(%d)'%(r,finish,len(threads),len(input_pool)))
            break
                    
        time.sleep(1)
       
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


def callback(blocks_read,block_size,total_size):
    global g_callback_last_msg
    if total_size < 0:
    # Unknown size
        g_callback_last_msg = '\rRead %d blocks (%d bytes)' % (blocks_read,blocks_read * block_size)    
    else:
        amount_read = blocks_read * block_size
        g_callback_last_msg = '\rRead %d blocks, or %d/%d' %(blocks_read, amount_read, total_size)
    
    sys.stderr.write(g_callback_last_msg)

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
    if dst_path is not None:
        dst_path = path.normpath(dst_path)
        dst_exist = path.exists(dst_path) 
        if  dst_exist == True and overwrite == False:
            print('Already exist, %s'%(dst_path))
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
    
    t = 0
    headers = {"Content-type": "application/x-www-form-urlencoded",\
               "Accept": "text/plain"}
    
    for t in range(1, trials):
        contents = ""
        
        conn = httplib.HTTPConnection(domain_name)
        try:
            
            if(post_args != None):
                conn.request("POST", file_path, post_args,headers)
            else:
                conn.request("GET", file_path)
                
            r = conn.getresponse()
            if r.status == 200:
                contents = r.read()
            elif r.status == 302:
                ret = download_http_file(r.getheader('Location'),dst_path,post_args,overwrite,trials)
                return ret
            else:
                LOG.debug(r.status, r.reason)
                print("Can not download the file, " + src_url + ".")
                break
            
            t = 0
            break

        except httplib.HTTPException, msg:
            #nFails = nFails + 1
            LOG.debug("HTTPException")
        except httplib.NotConnected, msg:
            #nFails = nFails + 1
            LOG.debug("NotConnected")
        except httplib.InvalidURL, msg:
            #nFails = nFails + 1
            LOG.debug("InvalidURL")
        except httplib.UnknownProtocol, msg:
            #nFails = nFails + 1
            LOG.debug("UnknownProtocol")
        except httplib.UnknownTransferEncoding, msg:
            #nFails = nFails + 1
            LOG.debug("UnknownTransferEncoding")
        except httplib.UnimplementedFileMode, msg:
            #nFails = nFails + 1
            LOG.debug("UnimplementedFileMode")
        except httplib.IncompleteRead, msg:
            #nFails = nFails + 1
            LOG.debug("IncompleteRead")
        except httplib.ImproperConnectionState, msg:
            #nFails = nFails + 1
            LOG.debug("ImproperConnectionState")
        except httplib.CannotSendRequest, msg:
            #nFails = nFails + 1
            LOG.debug("CannotSendRequest")
        except httplib.CannotSendHeader, msg:
            #nFails = nFails + 1
            LOG.debug("CannotSendHeader")
        except httplib.ResponseNotReady, msg:
            #nFails = nFails + 1
            LOG.debug("ResponseNotReady")
        except httplib.BadStatusLine, msg:
            #nFails = nFails + 1
            LOG.debug("BadStatusLine")
        except socket.error, e:
            LOG.debug("Socket exception error, %s."%e)
        finally:
            conn.close()
        # finally:
            #nFails = nFails + 1
        #alert_message("Unknown exception in DownloadHttpFile().")
        
        print("It will be start again after several seconds in download_http_file().")
        time.sleep(5)

    if (t > 0):
        return False
           
    if dst_path == None:
        return contents
       
    dst_path2 = make_path(dst_path) + '.down'

    try:
        with open(dst_path2, "wb") as f:
            f.write(contents)
        if path.exists(dst_path) == True:
            os.remove(dst_path)              
        os.rename(dst_path2, dst_path)
    except Exception:
        LOG.error("File Save error! - %s"%(dst_path2))
        return False

    #print ("Success downloading the file, " + strSrcUrl + ".")

    return True

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
                print "Already exist, %s."%(dst_path)
                return True

        # In the case,
        # 1. The local file does not exist.
        # 2. OVERWRITE = TRUE
        # 3. The file sizes on a remote path and a local path are different.
        fw = open(make_path(dst_path), "wb")
        ftp.retrbinary("RETR " + remote_file_path, fw.write)
        file.close()
        
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
