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
from __future__ import absolute_import 

import datetime
import os
import socket
import ftplib
import httplib

import string
import sys
import threading
import time
import urllib
import urllib2

import cStringIO as StringIO
import tempfile
import subprocess


from . import filepath
from . import utils

g_callback_last_msg = ''
LOG = utils.get_logger(__name__)

_download_pools = []


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


def download_http_file(src_url,dst_path='',post={},overwrite=False,trials=3,conn=None):
    '''
    Download a file on internet. return when a file saved to loacl is existed.
    
    :param string src_url: URL
    :param string dst_path: local path
    :param string post: arguments for POST method
    :param bool overwrite: if ture, local file will be overwritten.
    :param int trials: method will be terminated in trails number

    :return: bool
    '''
    # Check existing file
    if dst_path:
        if  os.path.exists(dst_path) and not overwrite:
            print('Already exist, %s'%(dst_path))
            return True
   
    
    domain_name,file_path = split_url(src_url)

    
    headers = {"Content-type": "application/x-www-form-urlencoded",\
               "Accept": "text/plain"}
   
    t = 0
    is_response = False
    
    http = None
    if conn:
        http = conn
    else:
        http = get_http_conn(domain_name)
        
    contents = ""    
    while(not is_response and t < trials): 
        
        try:
            if post:
                encoded = urllib.urlencode(post)
                http.request("POST", file_path,body=encoded,headers=headers)
            else:
                http.request("GET", file_path,headers=headers)
            
            r = http.getresponse()

            if r.status == 200:
                contents = r.read()
            elif r.status in [301,302,303,307,308]:
                r.read()
                new_loc = r.getheader('Location')
                new_host,_ = split_url(new_loc)

                _conn = None
                if http.host == new_host:
                    _conn = http
                
                contents = download_http_file(new_loc,
                                              post=post,
                                              overwrite=overwrite,
                                              trials=trials-1,
                                              conn=_conn)
            else:
                LOG.error("%d, %s - %s"%(r.status, r.reason,file_path))
                

            is_response = True
            r.close()
 
        except Exception as err:               
            LOG.error("Error : {} {}".format(repr(err),file_path))
            http.close()
            t += 1
    
        
        if not is_response:
            print("Re-trying...(%d/%d)"%(t,trials))
            time.sleep(5)
            
    if http and not conn:
        http.close()
   
    # File saving... 
    if dst_path:
        if contents == '':
            return False

        dst_path2 = filepath.make_path(dst_path) + '.down'
        
        with open(dst_path2, "wb") as f:
            f.write(contents)
        if os.path.exists(dst_path):
            os.remove(dst_path)              
        os.rename(dst_path2, dst_path)

        return True

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


def download_ftp_file(src_url, dst_path='', overwrite=False, trials=5, login_id="", login_pw="",conn=None):

   
    if dst_path:
        if os.path.exists(dst_path) and not overwrite:
            print("The file already exists, %s"%dst_path)
            return True

    
    ftp = None
    remote_domain,remote_file_path = split_url(src_url)
    if conn:
        ftp = conn
    else:

        ftp = get_ftp_conn(remote_domain,login_id,login_pw)
        
    contents = ''
    try:
        out = StringIO.StringIO()
        ftp.retrbinary("RETR " + remote_file_path, out.write)
        contents = out.getvalue()
        out.close()
            
    except Exception as e:
        print e
        
    
    if ftp and not conn:
        ftp.quit()
    
 
    if dst_path:
        if contents == '':
            return False

        dst_path2 = filepath.make_path(dst_path) + '.down'
        with open(dst_path2, "wb") as f:
            f.write(contents)
            
        if os.path.exists(dst_path) == True:
            os.remove(dst_path)
                          
        os.rename(dst_path2, dst_path)

        return True
            
    return contents



MODE_ALL = 0
MODE_DIRECTORY = 1
MODE_FILE = 2

def get_list_from_ftp(ftp_url,login_id='',login_pw='',mode=MODE_ALL,conn=None):

    li = []
    ftp_domain,ftp_dir = split_url(ftp_url)
    
    ftp = None
    if conn:
        ftp = conn
    else:
        ftp = get_ftp_conn(ftp_domain,login_id,login_pw)

    try:
        ftp.cwd(ftp_dir)
        ftp.retrlines("LIST", li.append) #, list.append)
    except ftplib.all_errors, e:
        err_string = str(e).split(None, 1)
        print err_string

        return [], []
    
    if ftp and not conn:
        ftp.quit()
    
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

def split_url(url):
    i1 = url.find("://")
    if i1 == -1 : i1 = 0
        
    i2 = url.find("/", i1+3)
    if i2 == -1 : i2 = len(url)
    
    remote_domain_name = url[i1+3:i2]
    remote_file_path = url[i2:]
    
    return remote_domain_name,remote_file_path

def get_http_conn(domain,*args,**kwargs):
    http = httplib.HTTPConnection(domain,timeout=10,*args,**kwargs)
    return http
def get_ftp_conn(domain,*args,**kwargs):
    login_id = kwargs.pop('login_id','anonymous')
    login_pw = kwargs.pop('login_pw','guest@anonymous.com')
    ftp = ftplib.FTP(domain,*args,**kwargs)
    ftp.login(login_id, login_pw)
    return ftp

def download_by_wget(url,dst_path,overwrite=False):
    _, download_path = tempfile.mkstemp()
    
    file_exist = os.path.exists(dst_path)
    
    if not overwrite and file_exist:
        LOG.debug("File already exists!: {}".format(dst_path))
        return

    ret = subprocess.check_call(['wget','-q','-O',download_path,url])
   
    if ret == 0:
        
        if file_exist:
            os.remove(dst_path)
     
        os.rename(download_path, dst_path)
        LOG.debug("Download complete! {}".format(dst_path))



       
        
