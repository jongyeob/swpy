'''
Created on 2015. 7. 9.

@author: jongyeob
'''
from swpy.utils import datetime as dt


print dt.replace("$(abc)%Y",dt.parse("20140101"),abc='123')
    
print dt.parse_string("%Y%m%d","20140201")
print dt.parse_string("%y%m%d %H%M%S.%f","990201 030201.3")
print dt.parse_string("%Y-%b-%d","2014-Jul-01")
print dt.parse_string("%H:%M:%S","20:01:03")
index = []
print dt.parse_string("%H:%M:%S","20130103/20:01:03",index=index)
print index

index = []
print dt.parse_date("20130303",index=index)
print index

index = []
print dt.parse_time("130303",index=index)
print index

print dt.parse_datetime('2013')
print dt.parse_datetime('2013',prior='time')
print dt.parse_datetime("asdf/20130101 010101")
print dt.parse_datetime("130303")
print dt.parse_datetime("130303",prior='time')
print dt.parse_datetime("20140101")
print dt.parse_datetime("010101 20140313")
print dt.parse_datetime("010101 20140401",prior='time')
   


print "datetime_range()"
print len(dt.datetime_range((2000,01,01),(2002,02,28),years=1)) == 3
print len(dt.datetime_range((2000,01,01),(2001,02,28),months=1)) == 14


print "parse()"
print dt.parse(2010) == dt.datetime(2010,1,1)
print dt.datetime(2010,2,27) == dt.parsing(2010,2,27)== \
                             dt.parsing((2010,2,27))== \
                             dt.parsing("20100227")
print dt.datetime(1999,12,31,11,22,33,444000)
print dt.parse(1999,12,31,11,22,33.444)
print dt.parse("19991231_112233.444")

text = "abcd/abcdef/2013/20140202/2014-02-02_002233" # Multiple detect
parse_time = dt.parse(text)
print parse_time
  
text = '2-Jul-02'
print dt.parse(text)

print dt.parse_string("/abcd/%Y/%Y%m%d","/abcd/2014/20140101") 
