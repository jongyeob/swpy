'''
Created on 2016. 5. 27.

@author: jongyeob
'''
import math

class SolarImage(object):
    def __init__(self):
        self.size = (-1,-1)
        self.imgcen = (-1,-1)
        self.solcen = (-1,-1)
        self.fov = (-1,-1,-1,-1) # l,r,t,b
        self.arcpix = -1
        self.filepath = ''
        self.rawdata = ''
        self.data = []
        self.obstime = None
    
    def load(self):
        NotImplemented('Abstrcat class!')
    def get(self,fov=(),size=()):
                        
        if len(self.data)> 0 :
            if self.fov == fov: 
                return self.data
                
        if fov:
            self.fov = fov
        
        sample = 1
        if len(size)>=2:
            min_img_size = min(self.size)
            min_size = min(size)
            if min_img_size > 2*min_size:
                sample = 2**int(math.log(min_img_size/min_size)+1)
            
            print "Sample rate : %d"%(sample)
            
              
        #self.data = [self.rawdata[y*self.size[0]:(y+1)*self.size[0]][self.fov[0]:self.fov[1]] for y in range(self.fov[2],self.fov[3])]        
        
        self.data = self.rawdata[self.fov[2]:self.fov[3]:sample,self.fov[0]:self.fov[1]:sample]
        return self.data
    
    
        
    
    def pix2arc(self,i,j,rev=False):
        pass
    def arc2sph(self,x,y,rev=False):
        pass
    def pix2sph(self,i,j,ref=False):
        pass
    
    def save(self,filepath,format='fits'):
        NotImplemented('Abstrcat class!')