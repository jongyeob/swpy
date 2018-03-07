'''
Created on 2016. 10. 15.

@author: jongyeob
'''

'''
downClient = Downloader(client,path,overwrite=False,timeout=10,thread=4)
downClient.start()
downClient.pause()
downClinet.stop()
'''

import os
import urllib2
import urlparse
import logging
from random import choice
from cStringIO import StringIO
from datetime import datetime

import filepath as swfp
import date_time as swdt


LOG = logging.getLogger(__name__)
CFG = {
    'temp-dir':'temp/'
    }

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]


def download_by_url(src,dst,overwrite=False,post=None):
    '''
    src: string
    dst: string or file
    
    '''
    url = src
    dst_file = dst
    
    if isinstance(dst,str):
        if os.path.exists(dst) and not overwrite:
            LOG.info('Already exist, %s'%(dst))
            return True
        
        swfp.mkpath(dst)
        dst_file = open(dst + '.down', 'wb')
        
    parsed_url = urlparse.urlsplit(url)
     
    chosen_user_agent = choice(user_agents)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent',chosen_user_agent)]
        
    
    f = opener.open(parsed_url.geturl(),data=post)
    
    block_size = 1024*8
    while 1:
        block = f.read(block_size)
        if not block:
            break
        
        dst_file.write(block)
        
    if isinstance(dst,str):
        dst_file.close()
        if os.path.exists(dst):
            os.remove(dst)              
        os.rename(dst + '.down', dst)


    return True

    