'''
@summary: test suite for sdo.py
Created on 2013. 12. 30.

@author: jongyeob
'''
 
import sdo
from utils import datetime as dt

print "datetime_from_filename_local()"
t = sdo.datetime_from_filename_local('20131231_010203400_aia.jp2')
print t == dt.parsing('2013-12-31 01:02:03.400')

print "hmi_jp2_path_nasa()"
s = sdo.hmi_jp2_path_nasa("2010-10-31 00:02:00.101", 'continuum')
print s == 'http://helioviewer.nascom.nasa.gov/2010_10_31__00_02_00_101__SDO_HMI_HMI_continuum.jp2'
s = sdo.hmi_jp2_path_nasa("2010-10-31 00:02:00.10", 'continuum')
print s == 'http://helioviewer.nascom.nasa.gov/2010_10_31__00_02_00_10__SDO_HMI_HMI_continuum.jp2'

print "hmi_jp2_list_nasa()"
print len(sdo.hmi_jp2_list_nasa("20121003","20121005","continuum")) == 3123

