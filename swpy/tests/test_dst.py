'''
Created on 2015. 6. 11.

@author: jongyeob
'''
import tempfile
import datetime
from swpy import dst
from swpy import utils

def test():
    
    date = datetime.datetime.now()
    date_2yr_ago  = date - datetime.timedelta(days=365*2)
    date_4yr_ago  = date - datetime.timedelta(days=365*4)
    
    
    dst.DATA_DIR =tempfile.mkdtemp().replace('\\','/') + '/'
    dst.download(date)
    dst.download(date_2yr_ago)
    dst.download(date_4yr_ago)
    
    data = dst.load(date_4yr_ago, date)
    utils.data.print_table(data,field_name=dst.DST_KEYS,vrules=3)
    
    coldata = zip(*data)
    dst.draw(coldata[1])

