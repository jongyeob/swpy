'''
Created on 2014. 1. 10.

author: jongyeob
'''

print "Start"
download_dst("20130901", "20131010")
download_dst_web("19991011", "19991112")

data = load_dst("20130901", "20130907")
draw_dst(data)
    
