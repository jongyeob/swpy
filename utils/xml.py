'''
Created on 2013. 5. 7.

@author: kasi
'''

from os import path
import os

from lxml import etree as et
from lxml.etree import Element

from swpy.utils import date_time as swdt


def create_xml(rootname,filepath=None):
    root = et.Element(rootname)
#    root = doc.createElement(rootname)
#    new_doc = new_xmldoc(rootname)
#    doc.appendChild(root)
    
    if filepath is not None:
        
        d,_ = path.split(filepath)
        if path.exists(d) == False:
            os.makedirs(d)
        
        write_xml(root,filepath)
        
    return root
def open_xml(filepath):
    if path.exists(filepath) == False:
        return None
    
    tree = et.parse(filepath)
    return tree.getroot()
def write_xml(elem,filepath):
    tree = et.ElementTree(elem)
    tree.write(filepath)
def is_exist(parent,elem):
    for el in parent.iter(elem.tag):
        if el.attrib == elem.attrib:
            return True 
        
    return False    
        
    
def julian_date(context,*args):
    # Input : 
    # [0] : Datetime string
    # [1] : Datetime string format
    # Output :
    # double : julian date
            
    return swdt.julian_date(args[0], args[1])

def range_number(context,*args):
    if args[1] <= args[0] <= args[2]:
        return True
    else:
        return False
    
def test(context,*args):
    print context
    print len(args)
    print args
    return ['1','2','3']
ns = et.FunctionNamespace(None)
ns['jd'] = julian_date
ns['range'] = range_number
ns['test'] = test


#    with open(filepath) as f_db:
#        xml_str = unicode(f_db.read(),'euc-kr').encode('utf-8')
            
#    return open_xmlstr(xml_str)




#    f_db = open(filepath,"w")
#    f_db.write(xml_str.encode('euc-kr'))
#    f_db.close()

#def append_dics(parent,dic_list):
#    if isinstance(dic_list, dict) is True :
#        dic_list = [dic_list]
#        
#        
#    for item in dic_list:
#        child = mdom.Element(item['NAME'])
#        
#        for key in item['ATTR'].iterkeys():
#            child.setAttribute(key,item['ATTR'][key])
#        
#        append_dics(child,item['CHILD'])
#                                
#        parent.appendChild(child)
#            
##    doc.appendChild(root)
#
#
#def new_dics(name,attr={},child=[]):
#    return {'NAME':name,'ATTR':attr,'CHILD':child}
#
#
#def dics_to_xmldoc(rootname,itemlist):
#    
#    doc = mdom.Document()
#    root = doc.createElement(rootname)
#    doc.appendChild(root)
#    
#    append_dics(root,itemlist)
#        
##    for item in itemlist:
##        child = doc.createElement("ITEM")
##        for key in item.iterkeys():
##            if find(key,'@') is 0 : # attribution
##                child.setAttribute(key[1:],item[key])
##            else: 
##                node = doc.createElement(key)
##                data = doc.createTextNode(str(item[key]))
##                node.appendChild(data)
##                child.appendChild(node)
##                                
##        root.appendChild(child)
#            
##    doc.appendChild(root)
#    return doc
#
#def dics_to_xml(rootname,itemlist):
#    doc = dics_to_xmldoc(rootname,itemlist)
#    return doc.toxml()
#
#def is_file(filepath):
#    return os.path.exists(filepath)
#
#def merge_xml(src_xml,dst_xml):
#
#    src_doc = mdom.parseString(src_xml)
#    dst_doc = mdom.parseString(dst_xml)
#    
#    src = src_doc.firstChild
#    dst = dst_doc.firstChild
#    
#    child = src.firstChild
#    while child != None:
#        dst.appendChild(child)
#        child = src.firstChild
#        
#    #print dst_doc.toprettyxml()
#        
#
##def new_xmldoc(rootname):
##    
##    doc = mdom.Document()
##    root = doc.createElement(rootname)
##    
###    child = doc.createElement('LAST_ID')
###    text = doc.createTextNode('0')
###    child.appendChild(text)
###    root.appendChild(child)
###    
###    child = doc.createElement('TOTAL')
###    text = doc.createTextNode('0')
###    child.appendChild(text)
###    root.appendChild(child)
###        
##    doc.appendChild(root)
##    
##    return doc
#
#
#
#
#    
#
#def add_items(parent,nodes):
#    
##    item_doc = mdom.parse(item_xml)
#    if isinstance(nodes, mdom.Document) is True:
#        nodes = [nodes]
#    
##    root = db_doc.firstChild
#     
##    total_node = db_doc.getElementsByTagName('TOTAL')[0].firstChild
##    last_id_node = db_doc.getElementsByTagName('LAST_ID')[0].firstChild
#    
#    count = 0
#    for node in nodes:
#                
#        
##        for item in item_root.childNodes:
#            
##            item.setAttribute('id',last_id_node.data)
##            child = db_doc.createElement('ITEM_ID')
##            data = db_doc.createTextNode(last_id_node.data)
##            child.appendChild(data)
##            
##            item.appendChild(child)
#
#        clone = node.cloneNode(True)
#        parent.appendChild(clone)
#                
##            last_id_node.data = str(long(last_id_node.data) + 1)
##            total_node.data = str(long(total_node.data) + 1)
#            
#        count = count + 1
#    
##    db_doc.appendChild(root)
#    
#    return count
#