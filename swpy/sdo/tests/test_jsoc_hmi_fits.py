import logging
import os
from swpy.sdo import hmi
from swpy.sdo import jsoc_hmi_fits as hmi_fits
from swpy.utils import datetime as dt
import tempfile
import pytest


logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))


hmi.DATA_DIR = tempfile.mkdtemp().replace('\\','/') + '/'

test_end   = dt.datetime.now()
test_start = test_end - dt.timedelta(days=10)
test_cadence = 7*86400 # seconds

@pytest.mark.online
def test_download():

    hmi_fits.download(test_start,test_end,test_cadence)


os.removedirs(hmi.DATA_DIR)
