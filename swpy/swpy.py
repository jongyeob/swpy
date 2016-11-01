'''
Created on 2016. 10. 17.

@author: jongyeob
'''
import logging

def get_logger(name):
    if not name.startswith('swpy.'):
        name = 'swpy.' + name
    
    logger = logging.getLogger(name)
    logger.setLevel(0)
    
    return logger
