import httplib
from urllib import urlretrieve
from os import path, makedirs
import time
import string
from swxml import Element,et

import sys

class Receipt():
    id = ''
    time = ''
    src_path = ''
    dst_path = ''
    src_size = 0
    dst_size = 0
    error_msg = 'None'
    success = False
    def __init__(self,id_str): 
        self.id = id_str
        self.time = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime())
    def to_element(self):
        r = Element('Receipt')
        r.attrib['id'] = self.id
        r.attrib['time'] = self.time
        r.attrib['src_path'] = self.src_path
        r.attrib['src_size'] = str(self.src_size)
        r.attrib['dst_path'] = self.dst_path
        r.attrib['dst_size'] = str(self.dst_size)
        r.attrib['error_msg'] = self.error_msg
        r.attrib['success'] = str(self.success)
        return r
    def from_element(self,element):
        self.id = element.attrib['id']
        self.time = element.attrib['time']
        self.src_path = element.attrib['src_path']
        self.src_size = int(element.attrib['src_size']) 
        self.dst_path = element.attrib['dst_path']
        self.dst_size = int(element.attrib['dst_size']) 
        self.error_msg = element.attrib['error_msg']
        self.success = False
        if element.attrib['success'].UpperCase() == 'TRUE':
            self.success = True
        
    def __str__(self):        
        return "ID : %s(%s) | Time : %s\n\
SRC : %s(%d)\n\
DST : %s(%d)\n\
Error : %s"\
        %(self.id,self.success,self.time,\
          self.src_path,self.src_size,\
          self.dst_path,self.dst_size,\
          self.error_msg)
    
    

def callback(blocks_read,block_size,total_size):
    if total_size < 0:
    # Unknown size
        sys.stderr.write('Read %d blocks (%d bytes)\n' % (blocks_read,blocks_read * block_size))
    else:
        amount_read = blocks_read * block_size
        sys.stderr.write('Read %d blocks, or %d/%d\n' %(blocks_read, amount_read, total_size))


def download(id_str,src,dst=None,overwrite=False):
    
    r = Receipt(id_str)
    
    r.id = id_str
    r.src_path  =   src
    r.dst_path = dst
    
    
        
    if dst is not None:
            
        dst_dirname, _ = path.split(dst)
        
        if path.exists(dst_dirname) == False:
            makedirs(dst_dirname)
        
    try:   
        if path.exists(dst) == True:
            raise IOError("Already exist")
       
    
        result = urlretrieve(src,dst,callback)
        
        r.dst_path = result[0]        
        r.src_size = int(result[1]['Content-Length'])
        
        
        with open(result[0],'r') as f:
            f.seek(0,2)
            r.dst_size = int(f.tell())
            
        r.success   =   True 
    
       
        
    except Exception as err:
        r.error_msg = str(err)
                
        
    return r

def get_list_from_html(contents, ext_list = None):
    strList = []
    
    # Make strExtList a list object if strExtList is not.
    if( ext_list != None):
        if (isinstance(ext_list, list) != True ):
            ext_list = [ext_list]
    
    
    
    iBegin = 0
    iEnd = 0
    
    i = 0
    
    while True:
        iBegin = string.find(contents,  "<a href=\"", iEnd)
        iBegin = iBegin + 9 # 9 is the length of "<a href=\"".
        if (iBegin == -1 or iBegin < iEnd):
            break
        
        iEnd = string.find(contents, "\"", iBegin)
        if (iEnd == -1):
            break
        
        strLink = contents[iBegin:iEnd]
        
        if (ext_list != None):
            for strExtName in ext_list:
                if(string.find(strLink, "." + strExtName) != -1):
                    strList.append(strLink)
        else:
            strList.append(strLink)
    
    #print strList[0]
    
    
    #iBegin = iEnd = iEnd + 1
    
    #        i = i+1
    #        if (i > 80000):
    #break;
    
    
    return strList

def load_http_file(url):
    contents = ""
    
    if (url.find("http://") != 0):
        print("The url is invalid, " + url + ".")
        return None
    
    i = url.find("/", 7)
    if (i < 9):
        print("The url is invalid, " + url + ".")
        return None

    domain_name = url[7:i]
    file_path = url[i:]

    conn = httplib.HTTPConnection(domain_name)
    conn.request("GET", file_path)


    r = conn.getresponse()

    #print (r.getheaders())
    
    if r.status == 301:
        contents = r.read()
    elif r.status != 200:
        print(r.status, r.reason)
        print("Can not download the file, " + url + ".")
        conn.close()
        return None
    else:
        contents = r.read()

    conn.close()

    return contents

# rval = download('asadfasdf','http://www.eveningbeer.com/lib/exe/fetch.php?media=study:computer_languages:c_reference_card_ansi_2.2.pdf')
# print(rval)
# print(et.tostring(rval.element()))


