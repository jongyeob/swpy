'''
Created on 2015. 7. 9.

@author: jongyeob
'''
from swpy.utils.datetime import *


print replace("$(abc)%Y",parse("20140101"),abc='123')
    
print parse_string("%Y%m%d","20140201")
print parse_string("%y%m%d %H%M%S.%f","990201 030201.3")
print parse_string("%Y-%b-%d","2014-Jul-01")
print parse_string("%H:%M:%S","20:01:03")
index = []
print parse_string("%H:%M:%S","20130103/20:01:03",index=index)
print index

index = []
print parse_date("20130303",index=index)
print index

index = []
print parse_time("130303",index=index)
print index

print parse_datetime('2013')
print parse_datetime('2013',prior='time')
print parse_datetime("asdf/20130101 010101")
print parse_datetime("130303")
print parse_datetime("130303",prior='time')
print parse_datetime("20140101")
print parse_datetime("010101 20140313")
print parse_datetime("010101 20140401",prior='time')
   


print "datetime_range()"
print len(datetime_range((2000,01,01),(2002,02,28),years=1)) == 3
print len(datetime_range((2000,01,01),(2001,02,28),months=1)) == 14


print "parse()"
print parse(2010) == datetime(2010,1,1)
print datetime(2010,2,27) == parsing(2010,2,27)== \
                             parsing((2010,2,27))== \
                             parsing("20100227")
print datetime(1999,12,31,11,22,33,444000)
print parse(1999,12,31,11,22,33.444)
print parse("19991231_112233.444")

text = "abcd/abcdef/2013/20140202/2014-02-02_002233" # Multiple detect
dt = parse(text)
print dt
  
text = '2-Jul-02'
print parse('2-Jul-98')

print parse_string("/abcd/%Y/%Y%m%d","/abcd/2014/20140101") 
