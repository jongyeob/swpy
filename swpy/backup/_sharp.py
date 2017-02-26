'''
Created on 2015. 10. 13.

@author: jongyeob
'''

import logging

from swpy.utils2 import FilePath, DateTime 
import json
import urllib


LOG    = logging.getLogger(__name__)

    
class TimedFilePath(object):
    def __init__(self,path):
        self.path  = path
                              
    def request(self,time,**kwargs):    
        
        path = dt.replace(self.path,time)
        response = ResponseFile(path)
                
        return response
    
    def query(self,time,sample_rate=0,**kwargs):
        _time   = dt.parse(time)
                 
        dir_format,_ = fp.path.split(self.path)
        
        
        data_dir = dt.replace(dir_format,_time)    
        _files = fp.get_files(data_dir+'/*')
        
        _files.sort()
        time_parser = lambda p:(dt.parse_string(self.path,p),)
        index = map(time_parser,_files)
        _index = dt.filter(index,_time,cadence=sample_rate)
    
        best_time = None
        if _index:
            best_time = _index[0][0]
                
        return best_time

class ResponseHTTP(object):
    def __init__(self,url,post={},**kwargs):
        self.url  = url
        self.post = post
        self.index = kwargs.pop('index',None)
        
    def read(self):
        content = dl.download_http_file(self.url,post=self.post)
        return content
    def get_info(self):
        method = 'GET'
        if self.post:
            method = 'POST'
            
        msg = "HTTP/{} {} {}".format(method,self.url,self.post)
        return msg     
    
import os
class ResponseFile(object):
    def __init__(self,path,**kwargs):
        self.path = path
        self.mode = kwargs.pop('mode','')
        self.index = kwargs.pop('index',None)
        
    def read(self,**kwargs):
        mode = 'r{}'.format(self.mode)
        
        with open(self.path,mode) as fr:
            content = fr.read()
        return content
    
    def write(self,content,**kwargs):
        mode = 'w{}'.format(self.mode)
        overwrite = kwargs.pop('overwrite',False)
        
        if not overwrite and os.path.exists(self.path):
            raise IOError("The file already exists : {}".format(self.path))
        
        utils.filepath.make_path(self.path)
        
        with open(self.path,mode) as fw:
            fw.write(content)
            
            
    def get_info(self):
        msg = "FILE {}".format(self.path)
        return msg


import json
from swpy.utils import data as da
import cStringIO as StringIO
class ResponseSharp(ResponseHTTP):
    keys = ['T_REC','HARPNUM',
            'USFLUX','MEANGAM','MEANGBT','MEANGBZ','MEANGBH','MEANJZD',
            'TOTUSJZ','MEANALP','MEANJZH','TOTUSJH','ABSNJZH','SAVNCPP',
            'MEANPOT','TOTPOT','MEANSHR','SHRGT45','CRPIX1','CRPIX2',
            'CRVAL1','CRVAL2','CDELT1','CDELT2','IMCRPIX1','IMCRPIX2','CROTA2',
            'CRLN_OBS','CRLT_OBS','RSUN_OBS','SIZE_ACR','AREA_ACR']
    
    def read(self):
        text = super(ResponseSharp,self).read()
        data = json.loads(text)
        
        data2 = dict([(key['name'],key['values']) for key in data['keywords']])
        
        keys = [key for key in self.keys if key in data2.keys()]
        cols = [data2[key] for key in keys] 
        rows = zip(*cols)
        rows = sorted(rows)
        

        otext =StringIO.StringIO()
        da.print_table(rows,output=otext,names=keys)
        new_text =otext.getvalue()
        otext.close() 
        
                
        return new_text
              
"""
From sunpy
"""
JSOC_INFO_URL = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info'
JSOC_EXPORT_URL = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_fetch'

class SharpPathJSOC():
     
    def __init__(self,series):
        """
        type : hmi.sharp_720s     | hmi.sharp_720s_nrt
               hmi.sharp_cea_720s | hmi.sharp_cea_720s_nrt
        """
        
        assert series in ['hmi.sharp_720s','hmi.sharp_720s_nrt',\
                        'hmi.sharp_cea_720s','hmi.sharp_cea_720s_nrt']
        
        self.series = series
                
    def get_last_time(self):
        
        dataset = '{series}'.format(series=self.series)
        postthis = {'ds': dataset,
                    'op': 'rs_list',
                    'key': 'T_REC',
                    'n':'-1',
                    'seg': '**NONE**',
                    'link': '**NONE**'}
        
        url = '{}?{}'.format(JSOC_INFO_URL, urllib.urlencode(postthis))
        
        r = ResponseHTTP(url)
        content = r.read()
        data = json.loads(content)
        
        _last = data['keywords'][0]['values'][0]
        last = dt.parse_string("%Y.%m.%d_%H:%M:%S_TAI", _last)
        
        return last
    def query(self,time,**kwargs):
        best_time = dt.trim(time,'date','start')
        return best_time
    
    def request(self,time,keywords=[],**kwargs):
        
        _time = dt.parse(time)
             
        _keywords = ''        
        if not keywords:
            _keywords = '**ALL**'
        else:
            for key in keywords:
                _keywords += '{},'.format(key)
            _keywords = _keywords[:-1]
        
        
        dataset = '{series}[][{time}/1d]'.format(
                   series=self.series, 
                   time=_time.strftime("%Y.%m.%d"))
        
        postthis = {'ds': dataset,
                    'op': 'rs_list',
                    'key': _keywords,
                    'seg': '**NONE**',
                    'link': '**NONE**'}
        
        url = '{}?{}'.format(JSOC_INFO_URL, urllib.urlencode(postthis))
        
        r = ResponseSharp(url)
       
        return r
    
class SharpPath(TimedFilePath):
    path = 'data/JSOC/SHARP/%Y/%Y%m/JSOC_SHARP_%Y%m%d.txt'
    def __init__(self,path=''):        
        if path :
            self.path = path
      
            
        super(SharpPath,self).__init__(self.path)

class TableDataBase(object):
    def __init__(self):
        self.keys = []
        self.data_series = []
    def append(self,key_data):
        self.keys.append(key_data[0])
        self.keys.append(key_data[1])
    def get_keys(self):
        return self.keys
    def get_data(self,key):
        i = self.keys.index(key)
        return self.data[i]
    
class SharpData(TableDataBase):
    pass
           

class SharpClient(object):
    def __init__(self,path):
        self.path = path
        
    def load(self,time):
        _time = dt.parse(time)
        
        r = self.path.request(_time)
        
        content = r.read()
        
        
        raise NotImplemented
        
    def draw(self,name):
        raise NotImplemented



class TimedDownloader(object):
    def __init__(self,from_path,to_path,logfile='',loglevel=0,**kwargs):
        self.from_path = from_path
        self.to_path = to_path
        
        self.logger = logging.getLogger('Downloader')
        hdlr = None
        if logfile:
            hdlr = logging.FileHandler(logfile)
        else:
            hdlr = logging.StreamHandler()
            
        self.logger.addHandler(hdlr)
        self.logger.setLevel(loglevel)
            
        
    def download(self,start,end,step,**kwargs):
        
        truncated = 25
        overwrite = kwargs.pop("overwrite",False)
        
        for t in dt.series(start,end,seconds=step):
            r_time = self.from_path.query(t,sample_rate=step)
            w_time = self.to_path.query(t,sample_rate=step)
            
            if not r_time:
                print "Reader is empty"
                self.logger.debug("Reader is empty")
                continue
            
            if w_time and not overwrite:    
                print "File is already exist"
                self.logger.debug("File is already exist")
                continue
            
            
            reader = self.from_path.request(t)
            writter = self.to_path.request(t)        
            
            msgr = reader.get_info()
            lenr = len(msgr)
            
            msgw = writter.get_info()
            lenw = len(msgw)
            
            fmt = "From {}"
            if lenr > truncated+3:
                fmt += "...{}"
                print fmt.format(msgr[:truncated],
                                 msgr[-truncated:]),
                                 
            fmt = "To {}"
            if lenw > truncated+3:
                fmt += "...{}"
                print fmt.format(msgw[:truncated],
                                 msgw[-truncated:])
            
            
            try:
                content = reader.read()
            except Exception as err:
                print "Failed - {}".format(err)
                msg = "Read exception ({})".format(err)
                self.logger.error(msg)
                continue
                
            try:
                writter.write(content,overwrite=overwrite,**kwargs)
                print "Success"
            except Exception as err:
                print "Failed - {}".format(err)
                msg = "Write exception ({})".format(err)
                self.logger.error(msg)
            