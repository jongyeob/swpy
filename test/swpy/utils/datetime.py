'''
Created on 2013. 12. 30.

@author: jongyeob
'''
from swpy.utils.datetime import *

print "datetime_range()"
print len(datetime_range((2000,01,01),(2002,02,28),years=1)) == 3
print len(datetime_range((2000,01,01),(2001,02,28),months=1)) == 14

print "parsing()"
print parsing(2010) == datetime(2010,1,1)
print datetime(2010,2,27) == parsing(2010,2,27)== \
                             parsing((2010,2,27))== \
                             parsing("20100227")
print datetime(1999,12,31,11,22,33,444000) == \
        parsing(1999,12,31,11,22,33.444) ==\
        parsing("19991231_112233.444")
                             

