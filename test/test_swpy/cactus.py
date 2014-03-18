'''
Created on 2014. 2. 17.

@author: jongyeob
'''

from swpy import cactus

cactus.download_cactus_lasco("199705", "201301");
cactus.download_cactus_cor2("200704", "201301");


l = cactus.load_cactus_lasco("19970501", "20130131");
for item in l:
    print item.t0

a = cactus.load_cactus_secchia("20070401", "20130131");
for item in a:
    print item.t0

b = cactus.load_cactus_secchib("20070401", "20130131");
for item in b:
    print item.t0



