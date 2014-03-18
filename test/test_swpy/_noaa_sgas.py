'''
Created on 2014. 1. 10.

:author: jongyeob
'''

import os,sys
from swpy import noaa_sgas as sgas
   
data = sgas.load_sgas("20120212")
data = sgas.load_sgas("20130312")
data = sgas.load_sgas("19970512")
    