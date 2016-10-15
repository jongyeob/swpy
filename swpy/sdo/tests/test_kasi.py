'''
Created on 2015. 5. 20.

@author: jongyeob
'''
import logging
import os
from swpy import utils
from swpy.sdo import kasi
from swpy.utils import datetime as dt


logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

     
data = kasi.request('fits','hmi','Ic_45s',"20121003",end_datetime="20121005",cadence=45)
print "# of Ic_45s [/45s] : ", len(data)
data = kasi.request('fits','hmi','Ic_45s',"20121003",end_datetime="20121005",cadence=90)
print "# of Ic_45s [/90s] : ", len(data)
data = kasi.request('fits','hmi','Ld_45s',"20121003",end_datetime="20121005",cadence=90)
print "# of Ld_45s [/90s] : ", len(data)
data = kasi.request('fits','hmi','Lw_45s',"20121003",end_datetime="20121005",cadence=90)
print "# of Lw_45s [/90s] : ", len(data)
data = kasi.request('fits','hmi','M_45s',"20121003",end_datetime="20121005",cadence=90)
print "# of M_45s [/90s] : ", len(data)
data = kasi.request('fits','hmi','V_45s',"20121003",end_datetime="20121005",cadence=90)
print "# of V_45s [/90s] : ", len(data)
data = kasi.request('fits','hmi','Ic_720s',"20121003",end_datetime="20121005",cadence=90)
print "# of Ic_720s [/90s] : ", len(data)
data = kasi.request('fits','hmi','Ld_720s',"20121003",end_datetime="20121005",cadence=90)
print "# of Ld_720s [/90s] : ", len(data)
data = kasi.request('fits','hmi','Lw_720s',"20121003",end_datetime="20121005",cadence=90)
print "# of Lw_720s [/90s] : ", len(data)
data = kasi.request('fits','hmi','M_720s',"20121003",end_datetime="20121005",cadence=90)
print "# of M_720s [/90s] : ", len(data)
data = kasi.request('fits','hmi','V_720s',"20121003",end_datetime="20121005",cadence=90)
print "# of V_720s [/90s] : ", len(data)
data = kasi.request('fits','hmi','S_720s',"20121003",end_datetime="20121005",cadence=90)
print "# of S_720s [/90s] : ", len(data)