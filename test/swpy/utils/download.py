'''
Created on 2014. 1. 6.

@author: jongyeob
'''
import os
import sys

import download as dl

## Configuration
src = "http://www.swpc.noaa.gov/ftpdir/latest/27DO.txt"
dst = './a/test.txt'
os.remove(dst) 
##
print "TEST : 404 Error"
print dl.download_url_file(src[:-2], dst)

##
print "TEST : Download"

print dl.download_url_file(src,dst)
if(os.path.exists(src) == True):
    print src + 'is exists'

##
print "TEST : Already exists"
try:
    dl.download_url_file(src,dst)
except Exception as err:
    print err


