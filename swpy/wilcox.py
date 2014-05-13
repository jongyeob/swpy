'''
Created on 2013. 12. 9.

@author: jongyeob
'''

import swpy

import os.path
import utils.date_time as dt
import utils.download as dl
from utils.utils import make_path


PROGRAM_PHOTOSPHERIC = 0
PROGRAM_CLASSICSS   = 1
PROGRAM_RADIAL250   = 2
PROGRAM_RADIAL325   = 3
PROGRAM_FILLED      = 4


PROJECTION_LATITUDE          = 1
PROJECTION_SINED_LATITUDE    = 0

DATATYPE_PRELIM          = 0
DATATYPE_FINAL          = 1

program_name = ['Photospheric','ClassicSS','Radial250','Radial325','Filled']
program_filename =['p','ss','r250','r325','f']
projection_name = ['Sined_Latitude','Latitude']
projection_filename = ['sl','l']
datatype_name = ['Prelim','Final']
datatype_filename = ['prelim','final']

DATA_DIR = swpy.DATA_DIR + '/wilcox/synoptic'

def download_synoptic_file(datetime,program=PROGRAM_PHOTOSPHERIC,projection=PROJECTION_SINED_LATITUDE,datatype=DATATYPE_PRELIM,overwrite=False):
    '''
    Download synoptic file from cgi get
    
    :param int program: Program name [Photospheric:0,ClassicSS:1,Radial250:2,Radial325:3,Filled:4]
    :param int projection: projection method [Sine_latitude:0, Latitude:1]
    :return: File path, if it failed, return None
    :see: Data request form refers to http://wso.stanford.edu/forms/prsyn.html  
    
    cgi-post (sample)
    http://wso.stanford.edu/cgi-bin/wso_prsyn.pl?rotation=&degrees=360&center=2013_12_01_00&ProgName=Photospheric&Type=Prelim&Projection=Sine_Latitude
    '''
       

    input_dt = dt.parsing(datetime)
    
    cgi = 'http://wso.stanford.edu/cgi-bin/wso_prsyn.pl'   

    args = 'center=%s&Type=%s&ProgName=%s&Projection=%s'%(input_dt.strftime("%Y_%m_%d_%H"),datatype_name[datatype],program_name[program],projection_name[projection])
    print args
    
    dstfile = '/wso_syn_%s_%s_%s_%s.txt'%(input_dt.strftime("%Y_%m_%d_%H"),\
                                       program_filename[program],projection_filename[projection],\
                                       datatype_filename[datatype])
    dstpath = DATA_DIR + dstfile
    print dstpath
    
    if overwrite == False and os.path.exists(dstpath) == True:
        return dstpath
     
    contents = dl.download_http_file(cgi,post_args=args)
    if contents == False:
        return None
        
    i1 = contents.find("<pre>")
    i1 = i1 + 5 # length of <pre>
    i2 = contents.find("</pre>")
    
    if (i1 == -1 or i2 == -1):
        return None
    
    if contents[i1:i2].find("30 data points") == -1:
        return None 
    
    with open(make_path(dstpath), "w") as fw:
        fw.write(contents[i1:i2])
     
    return dstpath

def path_local(datetime):
    pass
def path_wso(datetime):
    pass

if __name__ == '__main__':
    print "TEST : WILCOX download"
    print download_synoptic_file("2013-12-19")
