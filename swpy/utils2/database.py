'''
Created on 2016. 10. 15.

@author: jongyeob
'''
try: import cPickle as pickle
except: import pickle

from os import path
import logging

from swpy.utils2 import date_time as swdt
from swpy.utils2 import filepath as swfp

LOG = logging.getLogger("DataBase")

class DataBase():
    cache = {}
    def __init__(self,client,index_key='timeid',cache_size=100):
        self.client = client
        self.index_key = index_key
        self.cache_size = cache_size
    
    def restore(self,path):
        '''
        Restore DB cache file as pickle
        '''
        fp = open(path,'r')
        loaded_cache = pickle.load(fp)
        self.cache = loaded_cache
        fp.close()
        
    def save(self,path):
        '''
        Save DB cache file
        '''
        
        fp = open(path,'w')
        pickle.dump(self.cache, fp)
        fp.close()
        
    def request(self,time):
        '''
        Block based 
        '''
        parsed_time = swdt.parse(time)
        index_str = self.client.get(parsed_time)
        
        data = {}
        
        try:
            data = self.cache[index_str]
            return data 
        except:
            if path.exists(index_str):
                with open(index_str) as fp:
                    data = self.client.load(fp)
                
                    # __id__
                    data['__id__'] = [ swdt.parse(i) for i in data[self.index_key]]
                    self.cache[index_str] = data
        
        return data
    
    def update(self,time):
        '''
        Block based
        '''
        data = self.request(time)
        
        parsed_time = swdt.parse(time)
        index_str = self.client.get(parsed_time)
        
        try:
            del self.cache[index_str]
        except:
            pass
        
        
        with open(swfp.mkpath(index_str),'w') as fp:
            self.client.save(fp,data)
            self.cache[index_str] = data
            LOG.debug("DB update: {}".format(index_str))
        
    
    def search(self,time):
        '''
        Line based
        '''
        block_data = self.request(time)
        parsed_time = swdt.parse(time)  
        
        time_diff = [
            ( abs((t - parsed_time).total_seconds()), i ) 
            for i,t in enumerate(block_data['__id__'] )
            ]
        
        time_diff.sort()
        _, index = time_diff[0]
                
        return index
    
            
    def insert(self,data):
        '''
        Line based
        '''

        parsed_time = swdt.parse(data[self.index_key])
        insert_data = {'__id__':parsed_time}
        insert_data.update(data)
        
        block_data = self.request(parsed_time)
        
        if block_data:
            index = self.search(block_data,parsed_time)
            
            diff = block_data['__id__'][index] - parsed_time
            diff = diff.total_seconds()
            
            for key in ['__id__'] + self.client.key:
                if diff > 0:
                    block_data[key].insert(index,insert_data[key])
                elif diff < 0:
                    block_data[key].insert(index+1,insert_data[key])
                else:
                    block_data[key][index] = insert_data[key]
                
        else:
            for key in ['__id__'] + self.client.key:
                block_data[key] = [insert_data[key]]
            
        
    def delete(self,data):
        '''
        Line based
        '''
        parsed_time = swdt.parse(data[self.index_key])
        
        block_data = self.request(parsed_time)
        
        
        if block_data:
            index = self.search(parsed_time)
            
            diff = block_data['__id__'][index] - parsed_time
            diff = diff.total_seconds()
            
            if diff == 0:
                for key in ['__id__'] + self.client.key:
                    del block_data[key][index]
            
    
        

