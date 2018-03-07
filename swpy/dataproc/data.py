'''
Created on 2016. 5. 27.

@author: jongyeob
'''
import math

def great_circle_distance(loc,loc2):
    lon,lat = loc
    lon2,lat2 = loc2
    
    d2r = math.pi/180.
    dlon,dlat = (lon2-lon),(lat2-lat)
    
    sindis = math.sqrt(math.sin(dlat/2.*d2r)**2+
                       math.cos(lon*d2r)*math.cos(lon2*d2r)*
                       math.sin(dlon/2.*d2r)**2)
    
    return 2.0*math.asin(sindis)

def euclidean_distance(loc,loc2):
    x1,y1 = loc
    x2,y2 = loc2
    
    dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    return dis


class IDWEstimator():
    '''
    Interpolate data at location from datalist group by time
    '''
    def __init__(self,dist_func=None):
        self.locs = []
        self.datas = []
        self.dist_func = euclidean_distance
        if dist_func:
            self.dist_func = dist_func
                    
        
    def get_weight(self,loc,loc2):
        dist = self.dist_func(loc,loc2)

        weight = 1./dist 
        return  weight
         
        
    def load(self,loc,data):
        self.locs = loc
        self.datas = data

        
    def select(self,loc):
        total_weight = 0.
        total_wdata  = 0.
        
        try:
            weights = [self.get_weight(loc,loc2) for i,loc2 in enumerate(self.locs)]        
            for w,data in zip(weights,self.datas):
                total_weight += w
                total_wdata += w*data
        except ZeroDivisionError:

            total_wdata = self.datas[i]
            total_weight = 1
            
        val = total_wdata/total_weight
        
        return val
        