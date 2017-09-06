'''
Created on 2016. 6. 1.

@author: jongyeob
'''

from swpy.solarpack import sun
from swpy.utils import datetime as swdt
from sunpy import time as sunt
from sunpy import sun as ssun


def test():
    """
    Print out a summary of Solar ephemeris
    
    A correct answer set to compare to

    Solar Ephemeris for  1-JAN-01  00:00:00
    
    Distance (AU) = 0.98330468
    Semidiameter (arc sec) = 975.92336
    True (long, lat) in degrees = (280.64366, 0.00000)
    Apparent (long, lat) in degrees = (280.63336, 0.00000)
    True (RA, Dec) in hrs, deg = (18.771741, -23.012449)
    Apparent (RA, Dec) in hrs, deg = (18.770994, -23.012593)
    Heliographic long. and lat. of disk center in deg = (217.31269, -3.0416292)
    Position angle of north pole in deg = 2.0102649
    Carrington Rotation Number = 1971.4091        check!
    
    """
    t = '2001-01-01T00:00:00'
    
    
    swpy_jd  = swdt.julian_day(t)
    sunpy_jd = sunt.julian_day(t)
    
    print "SWPY JD: {}, SUNPY JD: {}".format(swpy_jd,sunpy_jd)
    print "Sun-earth distance: {}, {}".format(
                                              sun.sunearth_distance(t),
                                              ssun.sunearth_distance(t))
    print "Solar semidiameter angular size: {}, {}".format(
                                                           sun.solar_semidiameter_angular_size(t),
                                                           sun.solar_semidiameter_angular_size(t))
    print "True longitude: {}, {}".format(sun.true_longitude(t),
                                          ssun.true_longitude(t))
    print "Apparent Longitude: {}, {}".format(sun.apparent_longitude(t),
                                              ssun.apparent_longitude(t))
    print "True R.A.: {}, {}".format(
                                     sun.true_rightascension(t),
                                     ssun.true_rightascension(t))
    print "True Dec.: {}, {}".format(sun.true_declination(t),
                                     ssun.true_declination(t))
    print "Apparent R.A.: {}, {}".format(
                                         sun.apparent_rightascension(t),
                                         ssun.apparent_rightascension(t))
    print "Apparent Dec.: {}, {}".format(sun.apparent_declination(t),
                                         ssun.apparent_declination(t))
    print "Heliographic center: {}, {}".format(sun.heliographic_solar_center(t),
                                               ssun.heliographic_solar_center(t))
    print "Position angle of north pole [deg]: {}, {}".format(sun.solar_north(t),
                                                              ssun.solar_north(t))
    print "Carrington rotation number: {}, {}".format(sun.carrington_rotation_number(t),
                                                      ssun.carrington_rotation_number(t))
    
    
