'''
Created on 2015. 10. 9.

@author: jongyeob
'''
class LocalFiles():
    def __init__(self,path):
        self.dir  = path.dir
        self.file = path.file
        
    def query(self):
        raise NotImplemented
           
    def get_path(self):
        raise NotImplemented
    
    
class RemoteFiles():
    def __init__(self,local):
        self.local = local
        pass
    servers = []
    def add_server(self):
        raise NotImplemented
    def download(self):
        raise NotImplemented
    
    
class GOESXRay():
    def __init__(self,local):
        pass
    def load(self):
        pass
    def download(self):
        pass
    def plot(self):
        pass
    
class GOESProton():
    def plot(self):
        pass
    
class GOESElectron():
    def plot(self):
        pass