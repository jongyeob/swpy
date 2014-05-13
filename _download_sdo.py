'''
@summary: 
Download SDO data
@license:    GPLv2
@author:     Jongyeob Park(pjystar@gmail.com)
@version:    2013-08-14
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os
from swpy import sdo
from swpy.sdo import datetime_nasa, hmi_jp2_path_local
from swpy.utils import datetime as dt, download as dl
import sys
from time import sleep


config_keys = ['id','src','data','image','dst_dir','start_datetime','end_datetime','last_datetime','realtime','continue']
config_path = './config/download_sdo.conf'

DEBUG = 0

print __name__

def main(argv=None):
    '''
    @summary:     Main module
    @param :      (list) argv - System arguments
    @return :     (int) status - Non-zero is success
    @change:      2013-08-06 / Jongyeob Park(pjystar@gmail.com)
                  Change code from eclipse
    '''
### To do
# Args <-> Config
    if argv is None: argv = sys.argv
    else: sys.argv.extend(argv)
    
    now = dt.datetime.utcnow()
    
    image_types = ['aia_fits','aia_jp2','hmi_fits','hmi_jp2','hmi_gif']
    source_locations = ['kasi','jsoc','lmsal'] 
    
    dest_path = ('./data')
     
    try:
        # Setup argument parser
        parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
        #parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
#        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
#        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
#        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('--data',dest='data',help='aia_fits, aia_jp2, hmi_fits, hmi_jp2, hmi_gif')
        parser.add_argument('--image',dest='image',help='continuum, magnetogram')
        parser.add_argument('--src',dest='source',help='kasi, jsoc, lmsal [default : kasi]',default='kasi')
        parser.add_argument('--dest',dest='destination',help='path [default : %(default)s]',default=dest_path)
        parser.add_argument('--start',dest='start_time',help='start time',default=dt.datetime.strftime(now,"%Y-%m-%dT%H:%M:%S"))
        parser.add_argument('--end',dest='end_time',help='end time')
        parser.add_argument('--overwrite',action='store_true',dest='mode_overwrite',help='overwrite new files',default=False)
        parser.add_argument('--config',dest='config',help='id for program configurations')
             
        # Process arguments 
        args = parser.parse_args()

### Init config
#
#
        config_elem = sx.Element('config')
        config_elem.attrib['id'] = str(args.config)
        config_elem.attrib['src'] = args.source
        config_elem.attrib['data'] = args.data
        config_elem.attrib['image'] = args.image
        config_elem.attrib['dst_dir'] = args.destination
        config_elem.attrib['start_datetime'] = args.start_time
        end_datetime_t = dt.datetime.strptime(args.start_time,"%Y-%m-%dT%H:%M:%S") + dt.timedelta(seconds=1)
        config_elem.attrib['end_datetime'] =  dt.datetime.strftime(end_datetime_t,"%Y-%m-%dT%H:%M:%S")
        if args.end_time != None:
            config_elem.attrib['end_datetime'] = args.end_time
        config_elem.attrib['last_datetime'] = args.start_time

### Load config
#
#
        if args.config != None:
            config_root = sx.open_xml(config_path)
            if config_root != None:
                load_config_elem = config_root.xpath('./config[id="%s"][0]'%(args.config))
                if load_config_elem != None:
                    config_elem = load_config_elem
    
           
        sys.stdout.write(sx.et.tostring(config_elem)+"\n")
        

        
        if(args.data == 'hmi_jp2' and args.source == 'lmsal'):
            
            start_datetime_t = dt.str_to_datetime(config_elem.attrib['start_datetime'],"%Y-%m-%dT%H:%M:%S")
            end_datetime_t = dt.str_to_datetime(config_elem.attrib['end_datetime'],"%Y-%m-%dT%H:%M:%S")
           
            for t in dt.datetime_range(start_datetime_t, end_datetime_t, dt.timedelta(1)):
                
                start_t = t
                end_t = t + dt.timedelta(1)
                if end_t > end_datetime_t :
                    end_t = end_datetime_t
                    
                for f in sdo.hmi_jp2_list_lmsal(start_t, end_t,args.image ): # change generator
                
                    #dir manipulation
                    
                    f_datetime_t = datetime_from_filename_lmsal(f)
                    
                    if f_datetime_t == start_t :
                        continue
                    
                    dst_filepath = config_elem.attrib['dst_dir'] +'/'+ config_elem.attrib['image'] +\
                    hmi_jp2_path_local(f_datetime_t,config_elem.attrib['image'])
                
                    
                    r = dl.download_url_file(config_elem.attrib['id'], f,dst_filepath,args.mode_overwrite)
                 
                    sys.stdout.write(str(r)+'\n')
                
                    if r.success == True:
                        _,filename = os.path.split(f)
                        last_datetime_t = datetime_from_filename_lmsal(filename)
                        config_elem.attrib['last_datetime'] = dt.datetime.strftime(last_datetime_t,"%Y-%m-%dT%H:%M:%S")
          
    
        
### save config
#
#
        if args.config != None:
            config_root = sx.open_xml(config_path)
            if config_root == None:
                config_root = sx.create_xml('configs', config_path)
                
            old_config_elem = config_root.xpath('./config[id="%s"][0]'%(args.config))
            if old_config_elem == None:
                config_root.append(config_elem)
            else:
                old_config_elem.replace(config_elem)
    
            sx.write_xml(config_root, config_path)
            
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
  
DEBUG = 0

if __name__ == "__main__":
    '''
    @summary:     Main entry
    @change:      2013-08-06 / Jongyeob Park(pjystar@gmail.com)
                  Change code from eclipse
    '''

    sys.exit(main())
