'''
Created on 2015. 11. 19.

@author: jongyeob
'''
from __future__ import absolute_import

import os
import logging


from . import datetime as dt
from . import filepath as fp

def create_timed_dummies(timed_path,start,end,delta):
    total = 0
    if not isinstance(delta,dict):
        delta = {'seconds':delta}
        
    for _t in dt.series(start,end,**delta):
        filepath = dt.replace(timed_path,_t)
        
        fp.make_path(filepath)
        
        
        if os.path.exists(filepath) == False:
            with open(filepath,"wb"): pass
        total += 1
        
    logging.debug("The number of created files : %d"%(total))