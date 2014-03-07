'''
Created on 2014. 1. 9.

@author: jongyeob
'''

import os
from swpy import dst, noaa_ace_rt as nar, DATA_DIR
from swpy.utils import data as da, datetime as dt
import sys


startdate = "2013-01-01"
enddate = "2013-01-03"

start = dt.parsing(startdate)
end = dt.parsing(enddate)

filepath = nar.path_local(dt.tuples(start,'date'), 'mag')
mag_filepath = nar.download(start, 'mag',DATA_DIR+filepath)
mag_data = nar.load_mag(mag_filepath)
text = da.convert_text(mag_data)
text_lines = text.splitlines()
print text_lines[0:2]
print text_lines[-1]

filepath = nar.path_local(dt.tuples(start,'date'), 'swepam')
swepam_filepath = nar.download(start, 'swepam',DATA_DIR+filepath)
swepam_data = nar.load_swepam(swepam_filepath)
text = da.convert_text(swepam_data)
text_lines = text.splitlines()
print text_lines[0:2]
print text_lines[-1]

data1 = nar.loads("2013-10-01", 'swepam')
text = da.convert_text(data1)
text_lines = text.splitlines()
print text_lines[0:2]
print text_lines[-1]

data2 = nar.loads("2013-05-01", 'swepam',"2013-12-04")
text = da.convert_text(data2)
text_lines = text.splitlines()
print text_lines[0:2]
print text_lines[-1]