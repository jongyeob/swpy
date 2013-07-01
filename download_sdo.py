#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Download SDO data

@author:     Jongyeob Park
        
@copyright:  2013 Kyunghee Universty. All rights reserved.
        
@license:    license

@contact:    x9bong@hanmail.net
@deffield    updated: Updated

'''

import sys
import os
import time


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from swpy import sdo
from time import sleep
from swpy.utils import swdt as dt
from swpy.utils import download as dl
from swpy.utils import swxml as sx
from swpy.sdo import datetime_from_filename_lmsal, hmi_jp2_path_local


__all__ = []
__version__ = 0.1
__date__ = '2013-06-19'
__updated__ = '2013-06-19'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg
    
    
config_keys = ['id','src','data','image','dst_dir','start_datetime','end_datetime','last_datetime','realtime','continue']
config_path = './config/download_sdo.conf'

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv

    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Jongyeob Park on %s.
  Copyright 2013 Kyunghee Universty. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    now = time.localtime()
    
    image_types = ['aia_fits','aia_jp2','hmi_fits','hmi_jp2','hmi_gif']
    source_locations = ['kasi','jsoc','lmsal'] 
    
    dest_path = ('./data')
     
    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        #parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
#        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
#        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
#        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('--data',dest='data',help='aia_fits, aia_jp2, hmi_fits, hmi_jp2, hmi_gif')
        parser.add_argument('--image',dest='image',help='continuum, magnetogram')
        parser.add_argument('--src',dest='source',help='kasi, jsoc, lmsal [default : kasi]',default='kasi')
        parser.add_argument('--dest',dest='destination',help='path [default : %(default)s]',default=dest_path)
        
        parser.add_argument('--start',dest='start_time',help='start time',default=time.strftime("%Y-%m-%dT%H:%M:%S",now))
        parser.add_argument('--end',dest='end_time',help='end time',default=time.strftime("%Y-%m-%dT%H:%M:%S",now))
        parser.add_argument('--continue',dest='mode_continue',help='download files from last success',default=False)
        parser.add_argument('--realtime',dest='mode_realtime',help='download new files periodically',default=False)
        parser.add_argument('--config',dest='config',help='id for program configuration',default='default')
        
        
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        #parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')
              
        # Process arguments 
        args = parser.parse_args(argv[1:])
        print args
        
        # load config
        config_root = sx.open_xml(config_path)
        if config_root == None:
            config_root = sx.create_xml('configs', config_path)
        # init config    
        config_elem = config_root.find('./config[id="%s"]'%(args.config))
        if config_elem is None:
            config_elem = sx.Element('config')
            config_elem.attrib['id'] = args.config
            config_elem.attrib['src'] = args.source
            config_elem.attrib['data'] = args.data
            config_elem.attrib['image'] = args.image
            config_elem.attrib['dst_dir'] = args.destination
            config_elem.attrib['start_datetime'] = args.start_time
            config_elem.attrib['end_datetime'] = args.end_time
            config_elem.attrib['last_datetime'] = args.start_time
            config_elem.attrib['realtime'] = str(args.mode_realtime)
            config_elem.attrib['continue'] = str(args.mode_continue)
            config_root.append(config_elem)
            sx.write_xml(config_root, config_path)
        
            
        first_run = False    
        while config_elem.attrib['realtime'] == 'True' or first_run == False:
            first_run = True
        
            if(args.data == 'hmi_jp2' and args.source == 'lmsal'):
                
                start_datetime_t = dt.str_to_datetime(config_elem.attrib['start_datetime'],"%Y-%m-%dT%H:%M:%S")
                if config_elem.attrib['continue'] == 'True':
                    start_datetime_t = dt.str_to_datetime(config_elem.attrib['last_datetime'],"%Y-%m-%dT%H:%M:%S")
                    print("continue mode : "+str(start_datetime_t))
                    
                
                end_datetime_t = dt.str_to_datetime(config_elem.attrib['end_datetime'],"%Y-%m-%dT%H:%M:%S")
                if config_elem.attrib['realtime'] == 'True':
                    end_datetime_t = dt.datetime.utcnow()
                    print("Realtime mode : "+str(end_datetime_t))
                
                for t in dt.datetime_range(start_datetime_t, end_datetime_t, dt.timedelta(1)):
                    
                    start_t = t
                    end_t = t + dt.timedelta(1)
                    if end_t > end_datetime_t :
                        end_t = end_datetime_t
                        
                    for f in sdo.hmi_jp2_list_lmsal(start_t, end_t,args.image ):
                    
                        #dir manipulation
                        
                        f_datetime_t = datetime_from_filename_lmsal(f)
                        dst_filepath = config_elem.attrib['dst_dir'] + hmi_jp2_path_local(f_datetime_t,config_elem.attrib['image'])
                        r = dl.download(config_elem.attrib['config'], f,dst_filepath)
                         
                        sys.stdout.write(str(r))
                        
                        if r.success is True:
                            _,filename = os.path.split(f)
                            last_datetime_t = datetime_from_filename_lmsal(filename)
                            config_elem.attrib['last_datetime'] = dt.datetime.strftime(last_datetime_t,"%Y-%m-%dT%H:%M:%S")
                             
                            # save config
                            sx.write_xml(config_elem, config_path)
                         
                       
            
            sleep(1.0)
                    
    
        
                
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        #sys.argv.append("-v")
        #sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'download_srs_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())