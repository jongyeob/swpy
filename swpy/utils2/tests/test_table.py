'''
Created on 2016. 10. 20.

@author: jongyeob
'''
from swpy.utils2 import TableIO
from StringIO import StringIO

def test():
    test_data ={
        'test1':['hello'],
        'test2':[2],
        'test3':[3.3],
        'test4':[[1,2,3]]}
    test_key   = ['test1','test2','test4','test3']
    test_format = ['7.3','7','5','3.3']
    test_style  = ['<7','^10','>10','>9']
    
    
    table = TableIO(test_style)
    
    strIO = StringIO()
    table.write(strIO, test_data)
    strIO.seek(0)
    print table.read(strIO,test_key)
    strIO.close()
    
    strIO = StringIO()
    table.write(strIO, test_data,key=test_key)
    strIO.seek(0)
    print table.read(strIO,test_key)
    strIO.close()

    strIO = StringIO()
    table.write(strIO, test_data,key=test_key,format=test_format)
    strIO.seek(0)
    print table.read(strIO,test_key)
    strIO.close()
    