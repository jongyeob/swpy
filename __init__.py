## standard library
import os
from os import path
import sys

_root,_ = path.split(__path__[0])
SWPY_ROOT = _root
print "# SWPY_ROOT = {}".format(SWPY_ROOT)

## User configuration import
try:
    from swpy_config import *
    print("# User config imported")

except:
    print("# User config not imported")



   
