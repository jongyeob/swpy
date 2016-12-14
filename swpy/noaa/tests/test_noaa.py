'''
Created on 2015. 6. 11.

@author: jongyeob
'''
import datetime
import logging
import os
from swpy import utils
from swpy.noaa import indices, reports
from swpy.utils import data
import tempfile


logging.basicConfig(level=10,format="%(asctime)s [%(name)s:%(lineno)s] %(message)s")

temp_dir = tempfile.mkdtemp().replace('\\','/') + '/'
indices.DATA_DIR = temp_dir
reports.DATA_DIR = temp_dir

def test_events():
    now = datetime.datetime.now() - datetime.timedelta(days=2)
    past = now - datetime.timedelta(days=5)
    
    reports.download_events(past,now)
    rows = reports.load_events(past,now)
    
    data.print_table(rows)
        
    
def test_SRS():
   
    now = datetime.datetime.now() - datetime.timedelta(days=2)
    past = now - datetime.timedelta(days=5)
       
    reports.download_srs(past, now)
    rows = reports.load_srs(past, now)
    
    data.print_table(rows)

def test_SGAS():
    now = datetime.datetime.now() - datetime.timedelta(days=2)
    past = now - datetime.timedelta(days=5)
    
    reports.download_sgas(past, now)
    
def test_RSGA():
    now = datetime.datetime.now() - datetime.timedelta(days=2)
    past = now - datetime.timedelta(days=5)
    
    reports.download_rsga(past, now)

def test_GEOA():
    now = datetime.datetime.now() - datetime.timedelta(days=2)
    past = now - datetime.timedelta(days=5)
    
    reports.download_geoa(past, now)    

def test_DPD():

    now = datetime.datetime.now() - datetime.timedelta()
    past = now - datetime.timedelta(days=365)
    
    indices.download_dpd(past,now)
    
    rows = indices.load_dpd(past,now)
    data.print_table(rows)
    
    indices.draw_dpd(zip(*rows))
     
     
def test_DSD():
    
    now = datetime.datetime.now()
    past = now - datetime.timedelta(days=365)
    
    indices.download_dsd(past,now)
       
    rows = indices.load_dsd(past,now)
    data.print_table(rows)
    

def test_DGD():
    now = datetime.datetime.now()
    past = now - datetime.timedelta(days=365)
    
    indices.download_dgd(past,now)
    
    rows1,rows2 = indices.load_dgd(past,now)
    data.print_table(rows1)
    data.print_table(rows2)
