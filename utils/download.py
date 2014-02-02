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

import httplib
import ftplib
from os import path, makedirs
import time
import string


import sys
import os
import math

import datetime
import socket

from utils import with_dirs,alert_message 
from urllib2 import urlopen, HTTPError

import swpy
from httplib import HTTPException

g_callback_last_msg = ''



def callback(blocks_read,block_size,total_size):
    global g_callback_last_msg
    if total_size < 0:
    # Unknown size
        g_callback_last_msg = '\rRead %d blocks (%d bytes)' % (blocks_read,blocks_read * block_size)    
    else:
        amount_read = blocks_read * block_size
        g_callback_last_msg = '\rRead %d blocks, or %d/%d' %(blocks_read, amount_read, total_size)
    
    sys.stderr.write(g_callback_last_msg)

def download_url_file(src,dst=None,post_args=None,overwrite=False):
    '''
    Download a file on internet. return when a file saved to loacl is existed.
    
    :param string src: URL
    :param string dst: local path
    :param bool overwrite: Overwrite when local file is already been
    :return: if dst == None, downloaded path string or if dst != None, bool return
    '''
    dst = path.normpath(dst)
    dst_exist = path.exists(dst) 
    if  dst_exist == True and overwrite == False:
        raise IOError("The file is already been at %s"%(dst))
                   
    try_num = 0
    dst2 = dst + '.down'
        
    success = False
    while try_num < 3 and success == False:
        
        try_num = try_num + 1
        
        try:                            
            result = urlopen(src,data=post_args)
            
            contents = result.read()
            with open(with_dirs(dst2),"wb") as fw:
                fw.write(contents)
                        
            if path.exists(dst) == True:
                os.remove(dst) 
                                 
            os.rename(dst2, dst)
            
            result.close()
        
            success = True
                            
        except HTTPError as err:
            print err
            if err.code == 404:
                break
        
        except Exception as err:
            print err   
            break
            
       
    if success == False:
        return None
        
    return dst

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

def load_http_file(url):
    contents = None
    
    if (url.find("http://") != 0):
        print("The url is invalid, " + url + ".")
        return None
    
    i = url.find("/", 7)
    if (i < 9):
        print("The url is invalid, " + url + ".")
        return None

    domain_name = url[7:i]
    file_path = url[i:]
    try:
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
            return None
        else:
            contents = r.read()
    
        conn.close()
    except:
        return None

    return contents


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
        file = open(with_dirs(dst_path), "wb")

        ftp.retrbinary("RETR " + remote_file_path, file.write)

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




# rval = download('asadfasdf','http://www.eveningbeer.com/lib/exe/fetch.php?media=study:computer_languages:c_reference_card_ansi_2.2.pdf')
# print(rval)
# print(et.tostring(rval.element()))

