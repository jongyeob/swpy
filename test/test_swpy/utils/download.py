'''
Created on 2014. 1. 6.

@author: jongyeob
'''
import os
import sys

import swpy.utils.download as dl


# ## Configuration
# src = "http://www.swpc.noaa.gov/ftpdir/latest/27DO.txt"
# dst = './a/test.txt'
# 
# 
# print "No dstination path"
# print dl.download_http_file(src)
# 
# ##
# print "TEST : 404 Error"
# print dl.download_http_file(src[:-2], dst)
# 
# ##
# print "TEST : Download"
# 
# print dl.download_http_file(src,dst)
# if(os.path.exists(src) == True):
#     print src + 'is exists'
# 
# ##
# print "TEST : Already exists"
# try:
#     dl.download_http_file(src,dst,overwrite=False)
# except Exception as err:
#     print err

# print 'TEST : DownloadPool'
# pool = DownloadPool()
# print pool.recieving
# pool.close()
# print pool.recieving 

print "TEST: AutoTempFile"

temp_file = dl.AutoTempFile()
print temp_file.get_path()

print "end"