

import sys
from os.path import normpath

if sys.platform.startswith("win"):
    file_path = "%s/lib/site-packages/swpy.pth"%(sys.prefix)
elif sys.platform.startswith("linux"):
    file_path = "%s/lib/python%d.%d/site-packages/swpy.pth"%(sys.prefix,sys.version_info[0],sys.version_info[1])
else:
    sys.stderr.write("Unknown platform")
    sys.exit(-1)
    
file_path = normpath(file_path)

pth_file = open(file_path, "w")
swpy_path = normpath(sys.path[0])
pth_file.write(swpy_path);


pth_file.close();