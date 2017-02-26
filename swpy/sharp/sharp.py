'''
Created on 2017. 2. 23.

@author: parkj
'''
import logging
LOG = logging.getLogger(__name__)

import json
import urllib
import urllib2
from cStringIO import StringIO
from datetime import datetime

from swpy import utils2 as ut
from swpy.utils2 import TableIO


JSOC_INFO_URL = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info'
JSOC_EXPORT_URL = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_fetch'

DEFAULT_KEYWORDS = ['T_REC','HARPNUM',
            'USFLUX','MEANGAM','MEANGBT','MEANGBZ','MEANGBH','MEANJZD',
            'TOTUSJZ','MEANALP','MEANJZH','TOTUSJH','ABSNJZH','SAVNCPP',
            'MEANPOT','TOTPOT','MEANSHR','SHRGT45','CRPIX1','CRPIX2',
            'CRVAL1','CRVAL2','CDELT1','CDELT2','IMCRPIX1','IMCRPIX2','CROTA2',
            'CRLN_OBS','CRLT_OBS','RSUN_OBS','SIZE_ACR','AREA_ACR','NOAA_AR']

PATH_PATTERN = 'data/JSOC/SHARP/%Y/JSOC_SHARP{_CEA}{_NRT}_%Y%m%d.txt'

class SharpJsocClient():
    def __init__(self,cea=True,nrt=False,keywords=[]):
        self.cea = cea
        self.nrt = nrt
        self.keywords = ['**ALL**']
        
        self.series = 'hmi.sharp'
        if self.cea:
            self.series += '_cea'
        
        self.series += '_720s'
        
        if self.nrt:
            self.series += '_nrt'
            
        if keywords:
            self.keywords = keywords
            
        LOG.debug("SharpJsocClient initiated with {}".format(self.series))
        
        
    def get(self,time):
        
        parsed_time = ut.time_parse(time)
        
        dataset = '{series}[][{time}/1d]'.format(
                   series=self.series, 
                   time=parsed_time.strftime("%Y.%m.%d"))
        
        keywords = ''     
        for key in self.keywords:
            keywords += '{},'.format(key)
        
        keywords = keywords[:-1]
        
        postthis = {'ds': dataset,
                    'op': 'rs_list',
                    'key': keywords,
                    'seg': '**NONE**',
                    'link': '**NONE**'}
        
        url = '{}?{}'.format(JSOC_INFO_URL, urllib.urlencode(postthis))
        LOG.debug("Requested url: {}".format(url))
        
        return url
    
    def load(self,file):
       
        json_data = json.load(file)
        
        data = dict([(key['name'],key['values']) for key in json_data['keywords']])
        
        return data
    
    def get_last_time(self):
        
        dataset = '{series}'.format(series=self.series)
        postthis = {'ds': dataset,
                    'op': 'rs_list',
                    'key': 'T_REC',
                    'n':'-1',
                    'seg': '**NONE**',
                    'link': '**NONE**'}
        
        postdata = urllib.urlencode(postthis)
        
        url = '{}?{}'.format(JSOC_INFO_URL, postdata)

        dst = StringIO()
        
        ut.download_by_url(url, dst)
        
        content = dst.getvalue()
        dst.close()

        
        data = json.loads(content)
        
        last_time_str = data['keywords'][0]['values'][0]
        last_time = ut.parse_string("%Y.%m.%d_%H:%M:%S_TAI", last_time_str)
        
        return last_time
   


class SharpClient():
    def __init__(self,keywords,styles=[],cea=True,nrt=False):
        '''
        style: (dict) headers and style in python string format
        '''
        self.cea = cea
        self.nrt = nrt        
        
        self.keys = keywords
        
        self.styles = ['<24']*len(self.keys)
        
        if styles:
            self.styles = styles
            
        
        self.table = TableIO(self.styles)
        
        LOG.debug("SharpClient initiated")
            
      
    def get(self,time):
        
        parsed_time = ut.time_parse(time)
        cea = ''
        nrt = ''
        if self.cea:
            cea = '_CEA'
        if self.nrt:
            nrt = '_NRT'
        
            
        path = PATH_PATTERN.format(_CEA=cea,_NRT=nrt)
        path = datetime.strftime(parsed_time,path)
        
        return path
    
    def load(self,file):
        
        read_data = self.table.read(file, self.keys)
        
        return read_data
    
    def save(self,file,data):
        
        
        self.table.write(file, data,key=self.keys)

        return 0
