# SpaeWeatherPy library

from swpy import utils
from swpy.utils import datetime as dt
from swpy.utils import download as dl


LOG = utils.get_logger(__name__)
DATA_DIR = 'data/sidc/'
SSN_URL = "http://sidc.oma.be/DATA/DAILYSSN/"

def download_ssn(begindate, enddate=""):

    begin_dt, end_dt = dt.trim(begindate,1,'start'), dt.trim(enddate,1,'end')
    
        
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        src = "%(url)sdssn%(yyyy)04d.dat"%{"url":SSN_URL, "yyyy":now_dt.year}


        dst = DATA_DIR + "ssn/daily/ssn_%(yyyy)04d.txt"%{"yyyy":now_dt.year}


        # download it to a tmp file
        rv = dl.download_http_file(src, utils.make_path(dst))
        if rv != False:
            LOG.error("Download failed! : %s"%(src))
        
        #
        now_dt = now_dt + dt.timedelta(days=365)
        


if __name__=='_main__':
    files = download_ssn("2013", "2013")
    