'''
Created on 2015. 6. 15.

@author: jongyeob
'''
import copy
from swpy import utils
import tempfile


def test_config():
    test_ini = \
'''
[foo]
bar1=1
bar2=1.1
bar3=hello
[foo.bar]
bar1=1
bar2=1.1
bar3=hello
'''
    
    filepath = tempfile.mktemp()
    fw = open(filepath,'wt')
    print >> fw , test_ini
    fw.close()
    
    items = utils.config.load(filepath)
    
    
    namespaces_ref     = {'bar1':1,'bar2':'1.1','bar3':'hello'}
    
    namespaces = {'bar1':0,'bar2':'','bar3':''}
    utils.config.set(namespaces,**items['foo'])
    assert namespaces_ref == namespaces
    
    namespaces = {'bar1':0,'bar2':'','bar3':''}
    utils.config.set(namespaces,**items['foo.bar'])
    assert namespaces_ref == namespaces
    
    pop = utils.config.get(items,'foo')
    assert pop.has_key('foo.bar')
    
    pop = utils.config.get(items['foo'],'bar1')
    assert pop.has_key('bar1')
    
    
