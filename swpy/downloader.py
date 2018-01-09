'''
Created on 2017. 12. 21.

@author: jongyeob
'''
import os
from cStringIO import StringIO
from datetime import datetime
import ftplib
import logging
import urlparse


from swpy import utils2 as utils
from request import RequestUnit
from timepath import TimeFormat

LOG = logging.getLogger()
CFG = {'temp-dir':'temp/'}

class DownloaderUnit(RequestUnit):
    def request(self,time):
        raise NotImplemented
    
    def retrieve(self,time,dst='',overwrite=False):
        
        src_url = self.path.get(time)
        src_url_item = urlparse.urlparse(src_url)
        
        dst_path =  CFG['temp-dir'] + src_url_item.hostname + src_url_item.path
               
        if dst:
            dst_path = dst
            
        if os.path.exists(dst_path) and not overwrite:
            LOG.info('Already exist, %s'%(dst))
            return dst_path
        
        utils.mkpath(dst_path)
        dst_file = open(dst_path + '.down', 'wb')
            
        self.fetch(time,dst_file)
        
        dst_file.close()
        if os.path.exists(dst_path):
            os.remove(dst_path)              
        os.rename(dst_path + '.down', dst_path)

        return dst_path

class HttpDownloader(DownloaderUnit):
    def request(self,time):
        
        input_time = utils.time_parse(time)
    
        path = self.path.get(input_time)
        path_format = self.path.get_style()
        
        dir_path, file_name = os.path.split(path)
        dir_format, file_format = os.path.split(path_format)
        
        buf = StringIO()

        utils.download_by_url(dir_path, buf)
        file_time_list = []   
        
        contents = buf.getvalue()
        buf.close()
                
        start_index = 0
        end_index = 0
        
        while True:
            start_index = contents.find("<a href=\"", end_index)
            start_index += 9
            if (start_index == -1 or start_index < end_index):
                break
            
            end_index = contents.find("\"", start_index)
            if (end_index == -1):
                break
            
            url_path = contents[start_index:end_index]
            sub_dir,file_name = os.path.split(url_path)
            
            try:
                file_time = datetime.strptime(file_name,file_format)
                file_time_list.append(file_time)
            except:
                pass
            
        file_time_list.sort()
        
        return file_time_list
    
        def fetch(self,time,wfile):
            
            input_time = utils.time_parse(time)
    
            path = self.path.get(input_time)
                

            utils.download_by_url(path,wfile)
             
            
class FtpDownloader(DownloaderUnit):
    ftp = None
    def connect(self,user='',passwd=''):
        
        user_in = 'Anonymous'
        if user:
            user_in = user
            
        passwd_in = 'swpy@github.com'
        if passwd:
            passwd_in = passwd
            
            
        ftp_url = self.path.get_style()
        parse_ftp_url = urlparse.urlparse(ftp_url)
        ftp_domain = parse_ftp_url.hostname
        ftp_port   = parse_ftp_url.port
        
        
        if self.ftp:
            raise RuntimeError("Already FTP server connected. Disconnect first")
        
        self.ftp = ftplib.FTP()
        self.ftp.connect(ftp_domain,ftp_port)
        self.ftp.login(user_in, passwd_in)
        
    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            
            self.ftp = None
            
    def set_conection(self,ftp):
        
        if self.ftp:
            raise RuntimeError("Already FTP server connected. Disconnect first")
        
        self.ftp = ftp
        
    def get_connection(self):
        
        if not self.ftp:
            raise RuntimeError("No connection. Connect first")
        
        return self.ftp          
    
    def request(self,time):
        li = []
        
        time_in = utils.time_parse(time)
        
        ftp_url = self.path.get(time_in)
        parse_ftp_url = urlparse.urlparse(ftp_url)
        ftp_path = parse_ftp_url.path
        
        ftp_dir, _ = os.path.split(ftp_path)
        
        try:
            self.ftp.cwd(ftp_dir)
            self.ftp.retrlines("LIST", li.append) #, list.append)
        except ftplib.all_errors, e:
            err_string = str(e).split(None, 1)
            LOG.error(err_string)
    
            return []
        
        ftp_format = self.path.get_style()
        parse_ftp_format = urlparse.urlparse(ftp_format)
        path_format = parse_ftp_format.path
        _, file_format = os.path.split(path_format)
        
        
        file_time_list = []

        for line in li:
            if line[0] == "d" :
                continue
            
        
            file_size = line.split()[-2]
            file_name = line.split()[-1]
            
            file_time = utils.time_string(file_format,file_name)
            
            if file_time:
                file_time_list.append(file_time)
            else:
                LOG.debug("Not match time format for file name: {}".format(file_name))
            
        
    
        return file_time_list
    
            
    def fetch(self,time,wfile):
                   
        time_in = utils.time_parse(time)
        
        ftp_url = self.path.get(time_in)
        parse_ftp_url = urlparse.urlparse(ftp_url)
        ftp_path = parse_ftp_url.path

        self.ftp.retrbinary("RETR " + ftp_path, wfile.write)
        
        