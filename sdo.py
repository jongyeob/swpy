'''
@summary: 
1. Make filepaths from local
2. Save XML or TXT

@license:    GPLv2
@author:     Jongyeob Park(pjystar@gmail.com)
@version:    2013-08-06
@note: Keywords[Time,Path]
'''
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os
import sys


DEBUG = 0
def main(argv=None):
    '''
    @summary:     catalog_hmi    
    @param :     (swdt)start_date - year,month,day
                 (swdt)end_date - year,month,day
                 (str)inst - instrument ["continuum","magnetogram"] 
    @return :    (list)localpath
    @change:      2013-08-06 / Jongyeob Park(pjystar@gmail.com)
                  New code
    '''
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
    '''
    @summary:     Main entry
    @change:      2013-08-06 / Jongyeob Park(pjystar@gmail.com)
                  Change code from eclipse
    '''
    sys.exit(main())