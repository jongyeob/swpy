'''
Created on 2014. 2. 17.

@author: jongyeob
'''

from swpy import sidc

files = sidc.download_ssn("2013", "2013");
print files
