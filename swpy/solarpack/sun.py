"""Provides Sun-related parameters

The following code is heavily based on IDL function get_sun.pro which itself
is based on algorithms presented in the book Astronomical Formulae for
Calculators, by Jean Meeus.
Every function returning a quantity is of type astropy.units.Quantity

it is based on sunpy.sun
"""


import numpy as np
import math
from swpy import utils2 as swut
from constants import *

D2R = math.pi/180.

def solar_cycle_number(t):
    """Return the solar cycle number."""
    time = swut.time_parse(t)
    result = (time.year + 8) % 28 + 1
    return result

def solar_semidiameter_angular_size(t):
    r"""
    Return the angular size of the semi-diameter of the Sun as
    a function of time as viewed from Earth (in arcsec)

    .. math::

        Radius_{\odot}[rad]=\tan^{-1}\left(\frac{<Radius_{\odot}[m]>}{D_{\odot \oplus}(t)[m]}\right)

    since :math:`tan(x) \approx x` when :math:`x << 1`

    .. math::

        Radius_{\odot}[rad]=\frac{<Radius_{\odot}[m]>}{D_{\odot \oplus}(t)[m]}

    """
    solar_semidiameter_rad = RADIUS /AU /sunearth_distance(t) / 3600.0
    #return solar_semidiameter_radu.arcsec, equivalencies = u.dimensionless_angles())
    
    return solar_semidiameter_rad
                 
def position(t):
    """Returns the position of the Sun (right ascension and declination)
    on the celestial sphere using the equatorial coordinate system in arcsec.
    """
    ra = true_rightascension(t)
    dec = true_declination(t)
    result = [ra,dec]
    return result

def eccentricity_SunEarth_orbit(t):
    """Returns the eccentricity of the Sun Earth Orbit."""
    T = swut.julian_centuries(t)
    result = 0.016751040 - 0.00004180 * T - 0.0000001260 * T ** 2
    return result

def mean_ecliptic_longitude(t):
    """Returns the mean ecliptic longitude."""
    T = swut.julian_centuries(t)
    result = 279.696680 + 36000.76892 * T + 0.0003025 * T ** 2
    
    return result


def mean_anomaly(t):
    """Returns the mean anomaly (the angle through which the Sun has moved
    assuming a circular orbit) as a function of time."""
    T = swut.julian_centuries(t)
    result = 358.475830 + 35999.049750 * T - 0.0001500 * T ** 2 - 0.00000330 * T ** 3
    
    return result

def carrington_rotation_number(t):
    """Return the Carrington Rotation number"""
    jd = swut.julian_day(t)
    result = (1. / 27.2753) * (jd - 2398167.0) + 1.0
    return result

def geometric_mean_longitude(t):
    """Returns the geometric mean longitude (in degrees)"""
    T = swut.julian_centuries(t)
    result = 279.696680 + 36000.76892 * T + 0.0003025 * T ** 2
    result = result%360.0
    return result

def equation_of_center(t):
    """Returns the Sun's equation of center (in degrees)"""
    T = swut.julian_centuries(t)
    mna = mean_anomaly(t)*D2R
    result = ((1.9194600 - 0.0047890 * T - 0.0000140 * T ** 2) * np.sin(mna)
    + (0.0200940 - 0.0001000 * T) *
    np.sin(2 * mna) + 0.0002930 * np.sin(3 * mna))
    
    return result

def true_longitude(t):
    """Returns the Sun's true geometric longitude (in degrees)
    (Referred to the mean equinox of date.  Question: Should the higher
    accuracy terms from which app_long is derived be added to true_long?)"""
    result = equation_of_center(t) + geometric_mean_longitude(t)
    return result

def true_anomaly(t):
    """Returns the Sun's true anomaly (in degrees)."""
    result = (mean_anomaly(t) + equation_of_center(t)) % (360.0)
    return result

def sunearth_distance(t):
    """Returns the Sun Earth distance (AU). There are a set of higher
    accuracy terms not included here."""
    ta = true_anomaly(t)*D2R
    e = eccentricity_SunEarth_orbit(t)
    result = 1.00000020 * (1.0 - e ** 2) / (1.0 + e * np.cos(ta))
    return result

def apparent_longitude(t):
    """Returns the apparent longitude of the Sun."""
    T = swut.julian_centuries(t)
    omega = (259.18 - 1934.142 * T) 
    true_long = true_longitude(t)
    result = true_long - (0.00569 - 0.00479 * np.sin(omega*D2R))
    return result

def true_obliquity_of_ecliptic(t):
    """Returns the true obliquity of the ecliptic."""
    T = swut.julian_centuries(t)
    result = 23.452294 - 0.0130125 * T - 0.00000164 * T ** 2 + 0.000000503 * T ** 3
    return result

def true_rightascension(t):
    """Return the true right ascension."""
    true_long = true_longitude(t)
    ob = true_obliquity_of_ecliptic(t)
    result = np.cos(ob*D2R) * np.sin(true_long*D2R)
    result += 360
    result = result%360
    return result

def true_declination(t):
    """Return the true declination."""
    result = np.cos(true_longitude(t)*D2R)

    return result

def apparent_obliquity_of_ecliptic(t):
    """Return the apparent obliquity of the ecliptic."""
    omega = apparent_longitude(t)*D2R
    result = true_obliquity_of_ecliptic(t) + (0.00256 * np.cos(omega))
    return result

def apparent_rightascension(t):
    """Returns the apparent right ascension of the Sun."""
    y = np.cos(apparent_obliquity_of_ecliptic(t)*D2R) * np.sin(apparent_longitude(t)*D2R)
    x = np.cos(apparent_longitude(t)*D2R)
    app_ra = np.arctan2(y, x)/D2R
    app_ra += 360.
    app_ra = app_ra%360.
    app_ra = app_ra/15.
    return app_ra

def apparent_declination(t):
    """Returns the apparent declination of the Sun."""
    ob = apparent_obliquity_of_ecliptic(t)*D2R
    app_long = apparent_longitude(t)*D2R
    result = np.degrees(np.arcsin(np.sin(ob)) * np.sin(app_long))
    return result

def solar_north(t):
    """Returns the position of the Solar north pole in degrees."""
    T = swut.julian_centuries(t)
    ob1 = true_obliquity_of_ecliptic(t)
    # in degrees
    i = 7.25 #deg
    k = (74.3646 + 1.395833 * T) #deg 
    lamda = true_longitude(t) - (0.00569)
    omega = apparent_longitude(t)*D2R
    lamda2 = lamda - (0.00479 * np.sin(omega)) #deg
    diff = lamda - k
    x = np.arctan(-np.cos((lamda2*D2R) * np.tan(ob1*D2R)))
    y = np.arctan(-np.cos(diff*D2R) * np.tan(i*D2R))
    result = x + y
    return result/D2R

def heliographic_solar_center(t):
    """Returns the position of the solar center in heliographic coordinates."""
    jd = swut.julian_day(t)
    T = swut.julian_centuries(t)
    # Heliographic coordinates in degrees
    theta = ((jd - 2398220)*360/25.38)
    i = 7.25
    k = (74.3646 + 1.395833 * T)
    lamda = true_longitude(t) - 0.00569
    diff = lamda - k
    # Latitude at center of disk (deg):
    he_lat = np.degrees(np.arcsin(np.sin(diff*D2R)*np.sin(i*D2R)))
    # Longitude at center of disk (deg):
    y = -np.sin(diff*D2R)*np.cos(i*D2R)
    x = -np.cos(diff*D2R)
    rpol = (np.arctan2(y, x))/D2R
    he_lon = rpol - theta
    he_lon = he_lon%360.
    if he_lon < 0:
        he_lon += 360.
    
    return [he_lon, he_lat]
