'''
Created on 2015. 6. 16.

@author: jongyeob
'''
from __future__ import absolute_import

from . import asciitable


__all__ = ['print_table']

def print_table(row_data,**kwargs):
    asciitable.write(row_data,Writer=asciitable.FixedWidth,**kwargs)
