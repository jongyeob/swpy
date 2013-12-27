'''
Created on 2012. 11. 7.

@author: Daniel
'''
from re import match

from lxml import etree as et


datetime_format = "%Y-%m-%d"

scale = {'A':0.01,'B':0.1,'C':1,'M':10,'X':100}
xra_name = ['EVENT','SELECT','BEGIN','MAX','END','OBS','Q','TYPE','FRQ','SCALE','FLUX','REG_NO']


month_number = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

total_var = 11

db_dir = 'd:\\Database\\SWPC_SER'
db_file = 'd:\\Xmls\\swpc_ser.xml'

def noaa_path(date_t):
    yyyy = int(date_t[0])
    mm = int(date_t[1])
    dd = int(date_t[2])
    host  = 'ftp://ftp.swpc.noaa.gov'
    loc       = '/pub/warehouse/'
    
    filename = '%04d%02d%02devents.txt'%(yyyy,mm,dd)
    dirname = '%04d/%04d_events/'%(yyyy,yyyy)
    path = host + loc+ dirname + filename
    
    return path
def local_path(date_t):
    yyyy = int(date_t[0])
    mm = int(date_t[1])
    dd = int(date_t[2])
    dirname = '/%04d/'%(yyyy)
    filename = '%04d%02d%02devents.txt'%(yyyy,mm,dd)
    path = db_dir + dirname + filename
    
    return path
def paths(yyyy,mm,dd):
    return (noaa_path(yyyy, mm, dd),local_path(yyyy, mm, dd))
def read_date(text):
    date_fmt = (':Date: (\d+) (\d+) (\d+)','EDITED EVENTS for (\d+) (\S+) (\d+)')
    
    lines = text.splitlines()
    date = None
    for line in lines:
        i = 0    
        while date is None and i < len(date_fmt):
            date = match(date_fmt[i],line)
            i = i+1
                              
        if date is not None:
            year = int(date.group(1))
            if i == 1 :
                month = int(date.group(2))
            elif i == 2:
                month = month_number[date.group(2)]                    
            day = int(date.group(3))
            
#            jd = dbms.gc_to_jd(int(date.group(1)), int(date.group(2)), int(date.group(3)), 0, 0, 0)
#            mjd = dbms.jd_to_mjd(jd)
#            time_key['MJD'] = str(mjd[0])
#            time_key['DATE'] = str('%s-%s-%s'%(date.group(1),date.group(2),date.group(3)))
            return str('%04d-%02d-%02d'%(year,month,day))
            break
#            item['serID'] = str('SER%s%s%s' %date.groups())

    return None
   
def read(text):
    name = ['EVENT','SELECT','BEGIN','MAX','END','OBS','Q','TYPE','LOC_FRQ','PROPERTIES','REG_NO']
    fmt = ['(\d+).(.)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.)\s+(\S+)\s+(\S+)\s+(.{15})\s+(.{4})',
       '(\d+).(.)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.)\s+(\S+)\s+(\S+)\s+(.{16})']
    
    lines = text.splitlines()
   
    items = []    
   
    #time_key = {'srsID':'','MJD':'','DATE':''}
#    idx = 0
#    date = None
    for line in lines:
#        item = {'DATE':None}
        item = {}
#        if date is None:
#            date = match(date_fmt,line)
#                      
#        if date is not None:
#        if (date is not None) and (item['DATE'] is None):
            #jd = dbms.gc_to_jd(int(date.group(1)), int(date.group(2)), int(date.group(3)), 0, 0, 0)
            #mjd = dbms.jd_to_mjd(jd)
            #time_key['MJD'] = str(mjd[0])
            #time_key['DATE'] = str('%s-%s-%s'%(date.group(1),date.group(2),date.group(3)))
#            item['DATE'] = str('%s-%s-%s'%(date.group(1),date.group(2),date.group(3)))
#            item['serID'] = str('SER%s%s%s' %date.groups())
        
        i = 0
        data = None     
        while data is None and i < len(fmt):
            data = match(fmt[i],line)
            i = i+1
            
        if data is not None:
            #item['MJD'] = time_key['MJD']
            #item['DATE'] = time_key['DATE']
#            item['serID'] = item['serID'] + str('_%02d'%idx)
            
            item['REG_NO']  =   ''
            for i in range(len(data.groups())):
                item[name[i]] = data.group(i+1)
           
            if item['SELECT'].find('+') is not -1:
                item['SELECT'] = 'Y'
            else:
                item['SELECT'] = 'N'
            
            if item['REG_NO'].isspace() is True :
                item['REG_NO'] = ''
                
            if item['TYPE'].find('XRA') is not -1:
                #data = match('(\S+)(\s+)',item.pop('PROPERTIES'))
                data = item.pop('PROPERTIES').split()
                item['SCALE']   =   ''
                item['FLUX']    =   ''
                if len(data) > 0 :
                    item['SCALE']   =   data[0]
                if len(data) > 1:
                    item['FLUX']    =   data[1]
                
                data = item.pop('LOC_FRQ')
                item['FRQ'] = data
            else:
                continue
                   
            items.append(item)
#            idx = idx + 1
        
    return items
def append_srs(elem):
    pass
def append_ssf(elem):
    pass

def convert_elem(item):
     
    elem = None
    try:
        tag = item.pop('TYPE')    
        elem = et.Element(tag,item)
            
    except:
        print 'Error! - Convert_elem'
        
    return elem

def flare_scale(text):
    pass
        
    
#def convert_xml(text):
#    doc = convert_xmldoc(text)
#    return doc.toxml()

#def convert_xml(text):
#    lines = text.splitlines()
#    
#    doc = mdom.Document()
#    root = doc.createElement("ITEMS")
#    doc.appendChild(root)
#    
#    date = None
#    rkeys = {'MJD':'','DATE':''}
#    mjd_format = (':Date: (\d+) (\d+) (\d+)','EDITED EVENTS for (\d+) (\S+) (\d+)')
#    for line in lines:
#        if rkeys['MJD'] is '' :
#            i = 0    
#            while date is None and i < len(mjd_format):
#                date = match(mjd_format[i],line)
#                i = i+1
#            
#            if date is not None:
#                year = int(date.group(1))
#                
#                if i == 1 :
#                    month = int(date.group(2))
#                elif i == 2:
#                    month = month_number[date.group(2)]                    
#                day = int(date.group(3))
#                
#                jd = gc_to_jd(year,month,day , 0, 0, 0)
#                mjd = jd_to_mjd(jd)
#                rkeys['MJD'] = str(mjd[0])
#                rkeys['DATE'] = str('%04d-%02d-%02d'%(year,month,day))
#                
#                child = doc.createElement('MJD')
#                textnode = doc.createTextNode(rkeys['MJD'])
#                child.appendChild(textnode)
#                root.appendChild(child)
#                
#                child = doc.createElement('DATE')
#                textnode = doc.createTextNode(rkeys['DATE'])
#                child.appendChild(textnode)
#                root.appendChild(child)
#                
#                
#          
#            
#        data = match(fmt,line)
#        if data is not None:
#            item = doc.createElement('ITEM')
#                             
#            item.setAttribute('TYPE', 'SER')
#            
#            child = doc.createElement('MJD')
#            textnode = doc.createTextNode(rkeys['MJD'])
#            child.appendChild(textnode)
#            item.appendChild(child)
#            
#            child = doc.createElement('DATE')
#            textnode = doc.createTextNode(rkeys['DATE'])
#            child.appendChild(textnode)
#            item.appendChild(child)
#
#            for i in range(total_var):
#                child = doc.createElement(name[i])
#                textnode = doc.createTextNode(data.group(i+1))
#                child.appendChild(textnode)
#                item.appendChild(child)
#            
#            root.appendChild(item)
#                
#    doc.appendChild(root)
#    return doc.toxml()


#def save_item(item_xml):
#    if is_file(db_path) == 0:
#        create_xmlfile(db_path, 'SER_DB')
#    
#    db_xml = open_xmlfile(db_path)
#    
#    db_xml =  add_items(db_xml, item_xml)
#    
#    write_xmlfile(db_xml, db_path)
#    
#    return db_xml
