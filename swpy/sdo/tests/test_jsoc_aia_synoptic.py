import logging

import os
from swpy.sdo import aia
from swpy.sdo import jsoc_aia_synoptic as syn
from swpy.utils import datetime as dt
import tempfile
import pytest


logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))


aia.DATA_DIR = tempfile.mkdtemp().replace('\\','/') + '/'

test_end = dt.datetime.now()
test_start = test_end - dt.timedelta(days=20)
test_cadence = 7*86400 # seconds

@pytest.mark.online
def test_download():    
    for wave in aia.WAVELENGTHS:
        syn.download(wave,test_start,end=test_end,cadence=test_cadence)
        
os.removedirs(aia.DATA_DIR)