'''
SDO Package for KASI

author : Jongyeob Park(pjystar@gmail.com)
'''
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import logging
import os
from sys import stderr, stdout
import sys
import time


DEBUG = 0

def download(wavelength,start,end='',cadence=0,overwrite=False):
    '''
    downloads aia synotic from JSOCs
    
    parameters:
        start          - string
        wavelength     - string
        end            - string
    '''
    
    starttime = dt.parse(start)
    endtime = starttime
    if end != '':
        endtime = dt.parse(end) 

    recent_time = dl.download_http_file(REMOTE_TIME_URL)
    recent_time = recent_time.split()[1]
    recent_time = dt.parse(recent_time)

    time_series = dt.series(starttime,endtime,seconds=cadence)
    archive_series = []
    nrt_series = []
    
    starttime_archive = starttime
    endtime_archive   = endtime
    starttime_recent  = None
    endtime_recent = None
    
    if endtime_archive > recent_time:
        endtime_archive = recent_time
        endtime_recent = endtime
        starttime_recent = recent_time
        if starttime > recent_time:
            starttime_recent = starttime
        
    wave = str(wavelength).zfill(4)
    
    dir_cadence = 3600
    if cadence > 3600:
        dir_cadence = cadence
                 
    for t in dt.series(starttime_archive,endtime_archive,seconds=dir_cadence):
        url = dt.replace(REMOTE_DATA_DIR, t,wavelength=wave)
        LOG.debug(url)
        
        text = dl.download_http_file(url)
        files = dl.get_list_from_html(text, 'fits')
        archive_series.extend(files)
        
    LOG.info('%d files are found'%(len(archive_series)))
    if len(archive_series) > 0:
        LOG.debug(archive_series[0] + ' ...')
    
    time_format = dt.replace(REMOTE_DATA_FILE,wavelength=wave)
    time_parser = lambda s:dt.parse_string(time_format, s)
    index = map(time_parser,archive_series)
    archive_series = dt.filter(zip(index,archive_series),start,end_datetime=end,cadence=cadence)
    
    LOG.info('#(time), #(archive) = %d, %d'%(len(time_series), len(archive_series)))
    
    for t,f in archive_series:
        url = dt.replace(REMOTE_DATA_DIR+REMOTE_DATA_FILE, t,wavelength=wave)
        dstpath = aia.get_path(wavelength,FORMAT,t)
        
        dl.download_http_file(url, dstpath,overwrite=overwrite)
    
            
    if starttime_recent is not None:
        LOG.debug("Append data in nrt archive")
        for t in dt.series(starttime_recent,endtime_recent,seconds=dir_cadence):
            url = dt.replace(NRT_DATA_DIR, t,wavelength=wave)
            LOG.debug(url)
        
            text = dl.download_http_file(url)
            files = dl.get_list_from_html(text, 'fits')
            nrt_series.extend(files)
        
       
        LOG.info('%d files are found'%(len(nrt_series)))
        if len(nrt_series) > 0:
            LOG.debug(nrt_series[0] + ' ...')
        
        time_format = dt.replace(NRT_DATA_FILE,wavelength=wave)
        time_parser = lambda s:dt.parse_string(time_format, s)
        index = map(time_parser,nrt_series)
        nrt_series = dt.filter(zip(index,nrt_series),start,end_datetime=end,cadence=cadence)
        
        LOG.info('#(time), #(nrt) = %d, %d'%(len(time_series), len(nrt_series)))
        
        for t, f in nrt_series:
            dstpath = aia.get_path(wavelength,FORMAT,t)
            url = dt.replace(NRT_DATA_DIR+NRT_DATA_FILE, t,wavelength=wave)
                  
            dl.download_http_file(url, dstpath,overwrite=overwrite)



def download(start,end='',cadence=0,overwrite=False):
    '''
    downloads hmi fits from JSOCs
    '''
    
    ret = []
    
    starttime = dt.parse(start)
    endtime = starttime
    if end != '':
        endtime = dt.parse(end) 

    recent_time = dl.download_http_file(REMOTE_TIME_URL)
    recent_time = recent_time.split()[1]
    recent_time = os.path.split(recent_time)[1]
    
    recent_time = dt.parse(recent_time)
    
    dir_cadence = 86400
    
    archive_series = []
    
    starttime_archive = starttime
    endtime_archive   = endtime
    
    if endtime_archive > recent_time:
        endtime_archive = recent_time
        
    for t in dt.series(starttime_archive,endtime_archive,seconds=dir_cadence):
        url = dt.replace(REMOTE_DATA_DIR, t)
        LOG.debug(url)
        
        text = dl.download_http_file(url)
        files = dl.get_list_from_html(text, 'fits')
        archive_series.extend(files)
        
    LOG.info('%d files are found'%(len(archive_series)))
    if len(archive_series) > 0:
        LOG.debug(archive_series[0] + ' ...')
    
    time_format = dt.replace(REMOTE_NRT_FILE)
    time_parser = lambda s:dt.parse_string(time_format,s)
    index = map(time_parser,archive_series)
    archive_series = dt.filter(zip(index,archive_series),start,end_datetime=end,cadence=cadence)

    
    for t,f in archive_series:
        dstpath = hmi.get_path('M','fits_synoptic',t)
        url = dt.replace(REMOTE_DATA_DIR, t) + f
        
        ret.append((t,url,dstpath))
        if download:
            dl.download_http_file(url, dstpath,overwrite=overwrite)
    
    
    return ret
    

def main(argv=None):
    
    if argv is None: argv = sys.argv
    else: sys.argv.extend(argv)
    
    #-> start time- end time file list
    # keyword
    
    #config, argument
    
    try:
        # Setup argument parser
        parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)    
        parser.add_argument('--data',dest='data',help='hmi_jp2',default='hmi_jp2')
        parser.add_argument('--image',dest='image',help='ic,m')
        parser.add_argument('--start',dest='start_time',help='start time')
        parser.add_argument('--end',dest='end_time',help='end time')
        parser.add_argument('--text',dest='text',action='store_true',help='Text for output format')
        parser.add_argument('--xml',dest='xml',action='store_true',help='Text for output format')
        parser.add_argument('--key',dest='key',help='Keywords for output')
     
        args = parser.parse_args()      
                        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return -1
    except Exception, e:
        if DEBUG:
            raise(e)
        program_name = os.path.basename(sys.argv[0])
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return -1
    
    return 0


if __name__ == "__main__":
    
    sys.exit(main())