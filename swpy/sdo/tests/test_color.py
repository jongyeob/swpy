'''
Created on 2016. 5. 31.

@author: jongyeob
'''
from swpy.sdo.color import AIAColorTables

def test():
    print zip(*AIAColorTables.AIA304)
    
if __name__ == '__main__':
    test()