'''
Created on 2015. 7. 29.

@author: jongyeob
'''
from __future__ import absolute_import

import logging
from .base import LocalTimedClient,TimedClientBase,TimedCache

from .utils import datetime as swdt
from .utils import download as swdl

from swpy.dataproc.image import SolarImage 
import pyfits

 

LOG    = logging.getLogger(__name__)
LOCAL_URL ='data/ICCON/NoRH/%Y/%Y%m%d/%Y%m%d_%H%M%S_NoRH.fits'
REMOTE_URL = 'ftp://solar-pub.nao.ac.jp/pub/nsro/norh/fits/10min/%Y/%m/%d/ifa%y%m%d_%H%M%S'

class NoRH10minClient(LocalTimedClient):
    def __init__(self):
        LocalTimedClient.__init__(self,LOCAL_URL,cache_size=120)
    def request(self,time,margin=10*60):
        ret = LocalTimedClient.request(self, time, margin=margin)
        return ret


class RemoteNoRH10minClient(TimedClientBase):
    def __init__(self):
        TimedClientBase.__init__(self, REMOTE_URL)
        self.cache = TimedCache(size=120)
        self.last_access = None
                    
    def request(self, time, margin=10*60):
        '''
        time : UT
        '''
        input_time  = swdt.parse(time)
        input_time_lt = input_time + swdt.timedelta(hours=9)
        access_time = swdt.trim(input_time_lt,'date','start')
        
        LOG.debug("Input Time: {}, Cached Time: {}".format(input_time,access_time))
       
        
        ret = self.cache.request(input_time,margin=margin)
        if ret:    return ret
        elif self.last_access == access_time:
            return None
                
            
        format = self.get_url()
        
        i = format.find("://")
        protocol = format[:i]
        j = format.find("/",i+3)
        host = format[i+3:j]
        l = format.rfind('/')
        file_fmt = format[l+1:]
        
        LOG.debug("Protocol: {}, Host: {}, file_fmt: {}".format(protocol,host,file_fmt))        
        conn = swdl.get_ftp_conn(host)
        
        request_url = input_time_lt.strftime(format[:l])
        LOG.debug("URL: {}".format(request_url))
        files,sizes = swdl.get_list_from_ftp(request_url,conn=conn)
        
        def time_parser(s):
            t = swdt.parse_string(file_fmt,s)
            if t:
                t = t.replace(year=t.year+100)
            return t
        
        ret = []
        index = map(time_parser,files)
        
        for ti,file_name in zip(index,files):
            if not ti:
                continue
            
            remote_url = request_url + "/" + file_name
            ret.append((ti,remote_url)) 
        
        conn.close()
        
        self.cache.update(ret)
        self.last_access = access_time
        
        ret = self.request(time,margin=margin)
        
        return ret
    
class NORHFitsImage(SolarImage):
    def load(self,filepath):
        self.size = (512,512)
        self.fov = (0,512,0,512)
        hdulist = pyfits.open(filepath)
        self.rawdata = hdulist[0].data[::-1]
        hdulist.close()
        