'''
Created on 2016. 11. 1.

@author: jongyeob
'''
def dict_iseries(listed_dict):
    for values in zip(*listed_dict.values()):
        unit_dict = dict(zip(listed_dict.keys(),values))
        yield unit_dict

def dict_series(listed_dict):
    return [dict_iseries(listed_dict)]