'''
Created on 2014. 1. 13.

@author: jongyeob
'''
import os
import sys

import swpy.sdo2 as sdo


print sdo.download_hmi_jpg("20131021_000000","20131021_000100")

'''
print sdo.download_aia_jp2(304,"20131021_000000","20131021_000100",overwrite=True)
print sdo.download_aia_jp2(304,"20131021_000000","20131021_000100",overwrite=False)


print sdo.download_hmi_fits_njit()
'''
print "end"