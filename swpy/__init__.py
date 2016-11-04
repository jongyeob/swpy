from __future__ import absolute_import

## standard library
import os
from os import path
import sys

_root,_ = path.split(__path__[0])
ROOT = "{}/".format(_root)

print "# SWPY_ROOT = {}".format(ROOT)

## User configuration import
try:
    from swpy_config import *
    print("# User config imported")

except:
    print("# User config not imported")

