# SpaeWeatherPy library
import swpy

from utils import utils
import utils.date_time as dt
import utils.download as dl


SSN_URL = "http://sidc.oma.be/DATA/DAILYSSN/"
SSN_DIR = swpy.DATA_DIR + "/sidc/ssn/daily/"; 


def download_ssn(begindate, enddate=""):

    begin_dt, end_dt = dt.trim(begindate,1,'start'), dt.trim(enddate,1,'end')
    
    files = []
    
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        src = "%(url)sdssn%(yyyy)04d.dat"%{"url":SSN_URL, "yyyy":now_dt.year}

        dst = "%(dir)sdssn_%(yyyy)04d.txt"%{"dir":SSN_DIR, "yyyy":now_dt.year}


        # download it to a tmp file
        rv = dl.download_http_file(src, utils.make_path(dst))
        if rv != False:
            files.append(dst)
        
        #
        now_dt = now_dt + dt.timedelta(days=365)
        

    return files

if __name__=='_main__':
    files = download_ssn("2013", "2013")
    print files