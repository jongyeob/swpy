'''
Created on 2017. 4. 7.

@author: parkj
'''
from swpy.solarpack.image import SolarImage
from astropy.io import fits

class NorhFitsImage(SolarImage):
    def load(self,filepath):
        self.size = (512,512)
        self.fov = (0,512,0,512)
        hdulist = fits.open(filepath)
        self.rawdata = hdulist[0].data[::-1]
        hdulist.close()