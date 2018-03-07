'''
Created on 2017. 4. 7.

@author: parkj
'''
'''
Created on 2015. 7. 29.

@author: jongyeob
'''
from __future__ import absolute_import

import logging
from swpy.base import TimeFormattedPath,UrlPathRequest,FilePathRequest
 

LOG    = logging.getLogger(__name__)
LOCAL_URL ='data/ICCON/NoRH/%Y/%Y%m%d/%Y%m%d_%H%M%S_NoRH.fits'
REMOTE_URL = 'http://solar.nro.nao.ac.jp/norh/images/10min/%Y/%m/%d/ifa%y%m%d_%H%M%S'

class Norh10minFilePath(FilePathRequest): pass
class Norh10minUrlPath(UrlPathRequest): pass

norh_10min_file_path  = Norh10minFilePath(TimeFormattedPath(LOCAL_URL),margin=10*60)
norh_10min_url_path   = Norh10minUrlPath(TimeFormattedPath(REMOTE_URL),margin=10*60)
