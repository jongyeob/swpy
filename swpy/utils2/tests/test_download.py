'''
Created on 2017. 2. 23.

@author: parkj
'''
import logging; logging.basicConfig(level=10)
from swpy.utils2 import testing
from swpy.utils2 import download
from cStringIO import StringIO

LOG = logging.getLogger(__name__)

def test():
    
    test_url = ['http://www.google.com',
                {'url':'http://www.google.com'}]
    
    
    for url in test_url:
        io = StringIO()
        download.download_by_url(url, io)
        text = io.getvalue()
        length = len(text)
        
        LOG.debug('Download {} bytes'.format(length))
        
        io.close()


if __name__ == "__main__":
    testing.run_test(locals())