import httplib
from urllib import urlretrieve
from os import path, makedirs
import time
import string
from swxml import Element,et

import sys
import os

g_callback_last_msg = ''

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
        return "%s %s %s  %s(%d) -> %s(%d) %s"\
        %(self.time,self.id,self.success,\
          self.src_path,self.src_size,\
          self.dst_path,self.dst_size,\
          self.error_msg)
    
    

def callback(blocks_read,block_size,total_size):
    global g_callback_last_msg
    if total_size < 0:
    # Unknown size
        g_callback_last_msg = '\rRead %d blocks (%d bytes)' % (blocks_read,blocks_read * block_size)    
    else:
        amount_read = blocks_read * block_size
        g_callback_last_msg = '\rRead %d blocks, or %d/%d' %(blocks_read, amount_read, total_size)
    
    sys.stderr.write(g_callback_last_msg)
        


def download(id_str,src,dst=None,overwrite=False):
    
    r = Receipt(id_str)
    
    r.id        =   id_str
    r.src_path  =   src
    r.dst_path  =   dst
        
    if dst is not None:
            
        dst_dirname, _ = path.split(dst)
        
        if path.exists(dst_dirname) == False:
            makedirs(dst_dirname)
            
    
    iter = 0
    dst2 = dst
    while iter < 3 and r.success == False:
        iter = iter + 1            

        try:
            
            if dst is not None:
                if path.exists(dst) == True:
                    if overwrite == True:
                        os.remove(dst)
                    else:
                        raise IOError("Already exist")
                
                dst2  = dst + '.down'
                           
            
            result = urlretrieve(src,dst2,callback)
            
            
            sys.stderr.write('\n')
            
            r.dst_path = result[0]        
            r.src_size = int(result[1]['Content-Length'])
            
            
            with open(result[0],'r') as f:
                f.seek(0,2)
                r.dst_size = int(f.tell())
             
            
            if dst is not None:
                os.rename(dst2, dst)
                
            r.success   =   True
   
            
        except Exception as err:
            r.error_msg = str(err)
            break
        
        
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
    contents = None
    
    if (url.find("http://") != 0):
        print("The url is invalid, " + url + ".")
        return None
    
    i = url.find("/", 7)
    if (i < 9):
        print("The url is invalid, " + url + ".")
        return None

    domain_name = url[7:i]
    file_path = url[i:]
    try:
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
    except:
        return None

    return contents

# rval = download('asadfasdf','http://www.eveningbeer.com/lib/exe/fetch.php?media=study:computer_languages:c_reference_card_ansi_2.2.pdf')
# print(rval)
# print(et.tostring(rval.element()))


