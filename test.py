'''
Created on 2014. 2. 13.

@author: jongyeob
'''
import traceback
import logging
logging.basicConfig(level=0)

test_modules = [\
                #'swpy.sdo',\
                #'download_sdo',\
                'swpy.utils.download',\
                #'swpy.cactus'\
                ]



for test in test_modules:
    print "$$ Test module : %s"%(test)
    try:
        exec('import test.test_%s'%(test))
        print "$$ Done"
    except Exception as e:
        traceback.print_exc()
        