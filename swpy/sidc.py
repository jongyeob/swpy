# SpaeWeatherPy library
import swpy

import utils
import utils.datetime as dt
import utils.download as dl


ssn_url = "http://sidc.oma.be/DATA/DAILYSSN/"
ssn_dir = swpy.data_dir + "/sidc/ssn/daily/"; 


def download_ssn(begindate, enddate=""):

    begin_dt, end_dt = dt.trim(begindate,1,'start'), dt.trim(enddate,1,'end')
    
    files = []
    
    now_dt = begin_dt
    while ( now_dt <= end_dt ):
        src = "%(url)sdssn%(yyyy)04d.dat"%{"url":ssn_url, "yyyy":now_dt.year}

        dst = "%(dir)sdssn_%(yyyy)04d.txt"%{"dir":ssn_dir, "yyyy":now_dt.year}


        # download it to a tmp file
        dst = dl.download_url_file(src, utils.with_dirs(dst))
        if dst != None:
            files.append(dst)
        
        #
        now_dt = now_dt + dt.timedelta(days=365)
        

    return files


def test():
    files = download_ssn("2013", "2013");
    print files
    
    
    return


test()