'''
Created on 2016. 10. 20.

@author: jongyeob
'''
from swpy.utils2 import *
from StringIO import StringIO
import sys



def test_TableHeaderIO():
        
    test_data = {
        'var1':1,
        'var2':'a',
        'var3':['1',2],
        'var4':{'a':1,'b':'2'}}
    
    
    header = TableHeaderIO()
    
    str_io = StringIO()
    header.write(str_io,test_data)
    
    str_io.seek(0)
    print str_io.read()
    
    str_io.seek(0)
    
    read_data = header.read(str_io)
    print read_data
    
    str_io.seek(0)
    
    read_data = header.read(str_io,dtype={'var1':int,'var4':eval,'var3':eval})
    print read_data
        
def test_TableIO():
    test_data ={
        'test1':['hello'],
        'test2':[2],
        'test3':[3.333],
        'test4':[[1,2,3]]}
    test_key   = ['test1','test2','test3','test4']
    test_format = ['7.3','7','5','3.3']
    test_types  = {'test4':eval}
    
    
    table = TableIO()
    
    table.write(sys.stdout,test_data)
    table.write(sys.stdout,test_data,keys=['test1','test2'])
    table.write(sys.stdout,test_data,style={'test1':'>10'})
    table.write(sys.stdout,test_data,format={'test3':'.1f'})
    
    strIO = StringIO()
    table.write(strIO,test_data)
    width = "5 5 5 9"
    
    strIO.seek(0)
    data = table.read(strIO,width)
    print data
    strIO.seek(0)
    data = table.read(strIO,width,keys=test_key)
    print data
    strIO.seek(0)
    data = table.read(strIO,width,keys=test_key,dtype={'test4':eval})
    print data
    strIO.close()
