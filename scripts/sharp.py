#!/usr/bin/python

'''
Created on 2015. 11. 27.

@author: jongyeob
'''
import sys
import os
from swpy import sharp
from swpy import utils2 as ut
import logging
from cStringIO import StringIO
import traceback


def main(argv):
    mode = ''
    start = ''
    end   = ''
    opt_cea = False
    opt_nrt = False
    opt_overwrite = False
    opt_keys = ''
    
    for i,arg in enumerate(argv):
        if arg == '-m':
            mode = argv[i+1]
        if arg == '-s':
            start = argv[i+1]
        if arg == '-e':
            end = argv[i+1]
        if arg == '-o':
            opt_overwrite = True
        if arg == '--cea':
            opt_cea = True
        if arg == '--nrt':
            opt_nrt = True
        if arg == '--keys':
            opt_keys = argv[i+1]

    logging.basicConfig(level=10)
            
    
    start = ut.time_parse(start)
    end   = ut.time_parse(end)
    if not end:
        end = start
        
    if mode == 'download':
        
        keywords = sharp.DEFAULT_KEYWORDS
        if opt_keys:
            keywords = opt_keys.split(',')
            
        local = sharp.SharpClient(keywords,cea=opt_cea,nrt=opt_nrt)
        remote = sharp.SharpJsocClient(cea=opt_cea,nrt=opt_nrt)
        last_time = remote.get_last_time()
        logging.debug("Last avaiable data time: {}".format(last_time))
        
        if last_time < end:
            end   = last_time
        logging.debug("Start from {} to {}".format(start,end))
        
        for cur in ut.time_iseries(start,end,days=1):
            logging.info("Iteration {}".format(cur))
            
            try:
                path = local.get(cur)
                url = remote.get(cur)
                
                if os.path.exists(path) and not opt_overwrite:
                    logging.info("Already exists: {}".format(path))
                    continue
                
                buf = StringIO()
                ut.download_by_url(url,buf)
                text = buf.getvalue()
                buf.close()
                
                buf = StringIO(text)
                data = remote.load(buf)
                buf.close()
                
                ut.mkpath(path)
                f = open(path,'w')
                local.save(f,data)
                f.close()
            except:
                buf = StringIO()
                traceback.print_exc(file=buf)
                
                logging.error(buf.getvalue())
                buf.close()
                
        
def test():
    
    argv_test = "-m download -s 20151001_000000 -e 20151001_235959"
    argv = argv_test.split()
    main(argv)        
    
    argv_test = "-m download --cea -s 20151001_000000 -e 20151001_235959"
    argv = argv_test.split()
    main(argv)
    
    argv_test = "-m download --nrt -s 20151001_000000 -e 20151001_235959"
    argv = argv_test.split()
    main(argv)
    
    argv_test = "-m download --cea --nrt -s 20151001_000000 -e 20151001_235959"
    argv = argv_test.split()
    main(argv)
      
        
     

if __name__ == '__main__':
    
    if '-t' in sys.argv:
        test()
    else: 
        main(sys.argv)
    

