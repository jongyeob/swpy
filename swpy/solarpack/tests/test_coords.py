'''
Created on 2016. 6. 3.

@author: jongyeob
'''
from swpy.utils import datetime as swdt
from swpy.solarpack import coords
from astropy  import units as u
from sunpy.physics import differential_rotation as sdiff

def test():
    test_date = swdt.parse('2000-01-01_00:00:00')
    
    print "Diff rot: ", coords.diff_rot(86400, 0),sdiff.diff_rot(86400*u.second,0*u.degree)
    print "P, B0, SD: ", coords.get_pb0sd(test_date),sdiff._calc_P_B0_SD(test_date)
    print "Solar position: ",coords.get_solar_position(test_date),sdiff._sun_pos(test_date)
    
    l0 = 0
    b0 = 0
    scale = 0.6,0.6
    reference_pixel = 2048.5,2048.5
    reference_coordinate = 0, 0
    rotation = 180

    ij = 1000,1000
    print "Input coords: ",ij
    
    xy = coords.convert_pixel_to_data(ij, scale, reference_pixel, reference_coordinate,rotation)
    print "Convert to data: ",xy
    recall_ij = coords.convert_data_to_pixel(xy, scale, reference_pixel, reference_coordinate,rotation)
    print "Recall: ", recall_ij
    
    lonlat = coords.convert_hpc_hg(xy,b0,l0)
    print "Convert to hg", lonlat
    recall_xy = coords.convert_hg_hpc(lonlat,b0,l0)
    print "Recall to hpc", recall_xy
    recall_ij = coords.convert_data_to_pixel(recall_xy, scale, reference_pixel, reference_coordinate,rotation)
    print "Recall to pixel", recall_ij