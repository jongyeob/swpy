'''
Created on 2014. 1. 10.

@author: jongyeob
'''
import sys

from swpy import noaa
from swpy.utils import datetime as dt
from swpy.utils import data as da

now = dt.datetime.now()




# rv = noaa.download_dpd("1994",str(now.year))
# print rv
# data = noaa.load_dpd("1994",str(now.year))
# for key in data.keys():
#     sys.stdout.write(key+' ')
# sys.stdout.write('\n')
# 
# for key in data.keys():
#     sys.stdout.write(str(data[key][-1])+' ')
# sys.stdout.write('\n')


        
        

#rv = noaa.download_dsd("1994",str(now.year))
#print rv
table = noaa.load_dsd("1994",str(now.year))
da.print_summary(table)

#rv = noaa.download_dgd("1994",str(now.year))
#print rv
table = noaa.load_dgd("1994",str(now.year))
da.print_summary(table)

#download_se("1996", "2013")
#download_srs("2003", "2013")
#download_sgas("1996", "2013")
#download_rsga("1996", "2013")
#download_geoa("1996", "2013")
