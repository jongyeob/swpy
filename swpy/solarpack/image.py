'''
Created on 2017. 3. 25.

@author: jongyeob
'''
from swpy.base import DataUnit
from swpy import solarpack as swsp
import numpy as np

class SolarImage(DataUnit): pass
    
class SurfaceNorm():
    def __init__(self,solar_image):
        self.image = solar_image
        
    def get(self):
        
        header = self.image.header
        width, height = self.image.data.shape
    
        xx = np.arange(0,width)
        yy = np.arange(0,height)
        
        (X,Y) = np.meshgrid(xx,yy)
        X = (X-header['CRPIX1'] + 1)*header['CDELT1']
        Y = (Y-header['CRPIX2'] + 1)*header['CDELT2']
        
        r = header['RSUN_OBS']
        
        U = np.sqrt(1- (X*X + Y*Y)/(r*r))
        
        return U
        
class SolarGrid():
    def __init__(self,solar_image):
        self.image = solar_image
    
        header = self.image.header
        width, height = self.image.data.shape
    
        xx = np.arange(0,width)
        yy = np.arange(0,height)
        
        (X,Y) = np.meshgrid(xx,yy)
        X = (X-header['CRPIX1'] + 1)*header['CDELT1']
        Y = (Y-header['CRPIX2'] + 1)*header['CDELT2']
        
        self.data = (X,Y)
        
        
    def get_grid(self,coord='hpc'):
        
        outX,outY = self.data
               
        if coord == 'hg':
            outX,outY = swsp.convert_hpc_hg(self.data)
    
                            
        return (outX,outY)
    
    def get_norm(self):
        
        header = self.image.header
        
        r = header['RSUN_OBS']
        X,Y = self.data
        
        U = np.sqrt(1- (X*X + Y*Y)/(r*r))
        
        return U
    
    def get_surface(self):
        
        header = self.image.header
        
        r = header['RSUN_OBS']
        X,Y = self.data
        
        dist2 = X*X + Y*Y - r*r
        
        return dist2<0 