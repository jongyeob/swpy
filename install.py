from os import path
import os
import sys


file_path = None
os_type = None

print "# Check platform = ",
if sys.platform.startswith("win"):
    os_type = 'win'
elif sys.platform.startswith("linux"):
    os_type = 'linux'
elif sys.platform.startswith("darwin"):
    os_type = 'linux'
else:
    sys.stderr.write("{} unknown platform\n".format(sys.platform))
    sys.exit(-1)
print os_type

if 'doc' in sys.argv[1:]:
    print "# build document"

    ret = None
    old = os.getcwd()

    os.chdir('doc/source')
    if os_type == 'win':
        ret = os.system('make.bat html')
    elif os_type == 'linux':
        ret = os.system('make html')
    os.chdir(old)

file_path = os.getcwd() + os.path.split(sys.argv[0])[0]
print "# Write package path in python directory = %s"%(file_path)

if os_type == 'win':
    file_path = "%s/lib/site-packages/swpy.pth"%(sys.prefix)
elif os_type == 'linux':
    file_path = "%s/lib/python%d.%d/site-packages/swpy.pth"%(sys.prefix,sys.version_info[0],sys.version_info[1])

file_path = path.normpath(file_path)
with open(file_path, "w") as f:
    swpy_path = path.normpath(sys.path[0])
    f.write(swpy_path)

