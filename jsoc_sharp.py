'''
Created on 2015. 11. 27.

@author: jongyeob
'''
import sys
from swpy.sdo import sharp
from swpy.utils import datetime as dt
import multiprocessing as mp

def main(argv):
    mode = ''
    start = ''
    end   = ''
    opt_cea = False
    opt_nrt = False
    
    
    for i,arg in enumerate(argv):
        if arg == '-m':
            mode = argv[i+1]
        if arg == '-s':
            start = argv[i+1]
        if arg == '-e':
            end = argv[i+1]
        if arg == '--cea':
            opt_cea = True
        if arg == '--nrt':
            opt_nrt = True
    
    start = dt.parse(start)
    end   = dt.parse(end)
    if not end:
        end = start
        
    if mode == 'download':
        
        
        series  = 'hmi.sharp_720s'
        postfix = ''
        path    = 'd:/data/JSOC/SHARP{postfix}/%Y/%Y%m/JSOC_SHARP{postfix}_%Y%m%d.txt'
        
        if opt_cea:
            series = 'hmi.sharp_cea_720s'
            postfix = '_CEA'
            
        if opt_nrt:
            series += '_nrt'
            postfix += '_NRT'
            
        path = path.format(postfix=postfix)
            
        local = sharp.SharpPath(path=path)
        jsoc  = sharp.SharpPathJSOC(series)       
        last_time = jsoc.get_last_time()
            
        td = sharp.TimedDownloader(jsoc,local)
        
        start_ = start
        end_ = end
        
        if last_time < end:
            end_   = last_time
               
        td.download(start_, end_, step=86400)
        
        
        
        
def test():
    
    argv_ = "-m download -s 20151001_000000 -e 20151001_235959"
    argv = argv_.split()
    main(argv)        
    
    argv_ = "-m download --cea -s 20151001_000000 -e 20151001_235959"
    argv = argv_.split()
    main(argv)
    
    argv_ = "-m download --nrt -s 20151001_000000 -e 20151001_235959"
    argv = argv_.split()
    main(argv)
    
    argv_ = "-m download --cea --nrt -s 20151001_000000 -e 20151001_235959"
    argv = argv_.split()
    main(argv)
      
        
     

if __name__ == '__main__':
    
    if '-t' in sys.argv:
        test()
    else: 
        main(sys.argv)
    

