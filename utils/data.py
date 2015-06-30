'''
Created on 2015. 6. 16.

@author: jongyeob
'''
import asciitable

def print_table(row_data,**kwargs):
    asciitable.write(row_data,Writer=asciitable.FixedWidth,**kwargs)