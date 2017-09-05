from __future__ import division

import numpy as np

import sun
from swpy import utils2 as swut
import constants
import math

D2R = math.pi/180.0

'''
It comes from sunpy.
It is removed astropy and sunpy dependencies.

Thanks to the following authors.
__author__ = ["Jose Ivan Campos Rozo", "Stuart Mumford", "Jack Ireland"]
'''

def diff_rot(duration, latitude, rot_type='howard', frame_time='sidereal'):
    """
    This function computes the change in longitude over days in degrees.

    duration: [second]
    
    latitude: [degree]
    
    returns: 
    """

    latitude = latitude*D2R #deg
    delta_seconds = duration
    delta_days = delta_seconds / 24.0 / 3600.0

    sin2l = (np.sin(latitude))**2
    sin4l = sin2l**2

    rot_params = {'howard': [2.894, -0.428, -0.370],
                  'snodgrass': [2.851, -0.343, -0.474]
                  }

    if rot_type not in ['howard', 'allen', 'snodgrass']:
        raise ValueError("""rot_type must equal one of
                        { 'howard' | 'allen' | 'snodgrass' }""")

    elif rot_type == 'allen':
        rotation_deg = delta_days * (14.44 - (3.0 * sin2l))

    else:
        A, B, C = rot_params[rot_type]

        # This is in micro-radians / sec
        rotation_rate = A + B * sin2l + C * sin4l
        rotation_deg = rotation_rate * 1e-6 * delta_seconds / np.deg2rad(1)

    if frame_time == 'synodic':
        rotation_deg -= 0.9856 * delta_days

    #return Longitude((np.round(rotation_deg, 4)), u.deg)
    return np.round(rotation_deg, 4)


def get_pb0sd(date):
    """
    To calculate the solar P, B0 angles and the semi-diameter as seen from
    Earth.  This function is assigned as being internal as these quantities
    should be calculated in a part of SunPy that can calculate these quantities
    accurately.

    Parameters
    -----------
    date : `sunpy.time.time`
        the time at which to calculate the solar P, B0 angles and the
        semi-diameter.

    Returns
    -------
    A dictionary with the following keys with the following meanings:

    p  -  Solar P (position angle of pole)  (degrees)
    b0 -  latitude of point at disk centre (degrees)
    sd -  semi-diameter of the solar disk in arcminutes

    Notes
    -----
    SSWIDL code equivalent:
        http://hesperia.gsfc.nasa.gov/ssw/gen/idl/solar/pb0r.pro
    """
    # number of Julian days since 2415020.0
    de = swut.julian_day(swut.time_parse(date)) - 2415020.0

    # get the longitude of the sun etc.
    sun_position = get_solar_position(date)
    longmed = sun_position[0] #longitude
    #ra = sun_position["ra"]
    #dec = sun_position["dec"]
    appl = sun_position[1] #app_long
    oblt = sun_position[2] #obliq

    # form the aberrated longitude
    Lambda = longmed - (20.50 / 3600.0)

    # form longitude of ascending node of sun's equator on ecliptic
    node = 73.6666660 + (50.250 / 3600.0) * ((de / 365.250) + 50.0)
    arg = Lambda - node

    # calculate P, the position angle of the pole
    p = np.rad2deg(
        np.arctan(-np.tan(np.deg2rad(oblt)) * np.cos(np.deg2rad(appl))) +
        np.arctan(-0.127220 * np.cos(np.deg2rad(arg))))

    # B0 the tilt of the axis...
    b = np.rad2deg(np.arcsin(0.12620 * np.sin(np.deg2rad(arg))))

    # ... and the semi-diameter
    # Form the mean anomalies of Venus(MV),Earth(ME),Mars(MM),Jupiter(MJ)
    # and the mean elongation of the Moon from the Sun(D).
    t = de / 36525.0
    mv = 212.60 + np.mod(58517.80 * t, 360.0)
    me = 358.4760 + np.mod(35999.04980 * t, 360.0)
    mm = 319.50 + np.mod(19139.860 * t, 360.0)
    mj = 225.30 + np.mod(3034.690 * t, 360.0)
    d = 350.70 + np.mod(445267.110 * t, 360.0)

    # Form the geocentric distance(r) and semi-diameter(sd)
    r = 1.0001410 - (0.0167480 - 0.00004180 * t) * np.cos(np.deg2rad(me)) \
        - 0.000140 * np.cos(np.deg2rad(2.0 * me)) \
        + 0.0000160 * np.cos(np.deg2rad(58.30 + 2.0 * mv - 2.0 * me)) \
        + 0.0000050 * np.cos(np.deg2rad(209.10 + mv - me)) \
        + 0.0000050 * np.cos(np.deg2rad(253.80 - 2.0 * mm + 2.0 * me)) \
        + 0.0000160 * np.cos(np.deg2rad(89.50 - mj + me)) \
        + 0.0000090 * np.cos(np.deg2rad(357.10 - 2.0 * mj + 2.0 * me)) \
        + 0.0000310 * np.cos(np.deg2rad(d))

    sd_const = constants.RADIUS / constants.AU
    sd = np.arcsin(sd_const / r) * 180.0 / np.pi * 3600. #arcsec

    return (p,b,sd)


def get_solar_position(date):
    """
    Calculate solar ephemeris parameters.  Allows for planetary and lunar
    perturbations in the calculation of solar longitude at date and various
    other solar positional parameters. This routine is a truncated version of
    Newcomb's Sun and is designed to give apparent angular coordinates (T.E.D)
    to a precision of one second of time.  This function replicates the SSW/
    IDL function "sun_pos.pro".  This function is assigned to be
    internal at the moment as it should really be replaced by accurate
    ephemeris calculations in the part of SunPy that handles ephemeris.

    Parameters
    -----------
    date : `sunpy.time.time`
        Time at which the solar ephemeris parameters are calculated.  The
        input time can be in any acceptable time format.

    Returns
    -------
    A dictionary with the following keys with the following meanings:

    longitude  -  Longitude of sun for mean equinox of date (degs)
    ra         -  Apparent RA for true equinox of date (degs)
    dec        -  Apparent declination for true equinox of date (degs)
    app_long   -  Apparent longitude (degs)
    obliq      -  True obliquity (degs)

    Notes
    -----
    SSWIDL code equivalent:
        http://hesperia.gsfc.nasa.gov/ssw/gen/idl/solar/sun_pos.pro

    Examples
    --------
    >>> from sunpy.physics.differential_rotation import _sun_pos
    >>> sp = _sun_pos('2013-03-27')
    """
    # Fractional Julian day with correct offset
    dd = swut.julian_day(date) - 2415020.0

    # form time in Julian centuries from 1900.0
    t = dd / 36525.0

    # form sun's mean longitude
    l = (279.6966780 + np.mod(36000.7689250 * t, 360.00)) * 3600.0

    # allow for ellipticity of the orbit (equation of centre) using the Earth's
    # mean anomaly ME
    me = 358.4758440 + np.mod(35999.049750 * t, 360.0)
    ellcor = (6910.10 - 17.20 * t) * np.sin(np.deg2rad(me)) + \
    72.30 * np.sin(np.deg2rad(2.0 * me))
    l = l + ellcor

    # allow for the Venus perturbations using the mean anomaly of Venus MV
    mv = 212.603219 + np.mod(58517.8038750 * t, 360.0)
    vencorr = 4.80 * np.cos(np.deg2rad(299.10170 + mv - me)) + \
          5.50 * np.cos(np.deg2rad(148.31330 + 2.0 * mv - 2.0 * me)) + \
          2.50 * np.cos(np.deg2rad(315.94330 + 2.0 * mv - 3.0 * me)) + \
          1.60 * np.cos(np.deg2rad(345.25330 + 3.0 * mv - 4.0 * me)) + \
          1.00 * np.cos(np.deg2rad(318.150 + 3.0 * mv - 5.0 * me))
    l = l + vencorr

    # Allow for the Mars perturbations using the mean anomaly of Mars MM
    mm = 319.5294250 + np.mod(19139.858500 * t, 360.0)
    marscorr = 2.0 * np.cos(np.deg2rad(343.88830 - 2.0 * mm + 2.0 * me)) + \
            1.80 * np.cos(np.deg2rad(200.40170 - 2.0 * mm + me))
    l = l + marscorr

    # Allow for the Jupiter perturbations using the mean anomaly of Jupiter MJ
    mj = 225.3283280 + np.mod(3034.69202390 * t, 360.00)
    jupcorr = 7.20 * np.cos(np.deg2rad(179.53170 - mj + me)) + \
          2.60 * np.cos(np.deg2rad(263.21670 - mj)) + \
          2.70 * np.cos(np.deg2rad(87.14500 - 2.0 * mj + 2.0 * me)) + \
          1.60 * np.cos(np.deg2rad(109.49330 - 2.0 * mj + me))
    l = l + jupcorr

    # Allow for the Moons perturbations using the mean elongation of the Moon
    # from the Sun D
    d = 350.73768140 + np.mod(445267.114220 * t, 360.0)
    mooncorr = 6.50 * np.sin(np.deg2rad(d))
    l = l + mooncorr

    # Note the original code is
    # longterm  = + 6.4d0 * sin(( 231.19d0  +  20.20d0 * t )*!dtor)
    longterm = 6.40 * np.sin(np.deg2rad(231.190 + 20.20 * t))
    l = l + longterm
    l = np.mod(l + 2592000.0, 1296000.0)
    longmed = l / 3600.0

    # Allow for Aberration
    l = l - 20.5

    # Allow for Nutation using the longitude of the Moons mean node OMEGA
    omega = 259.1832750 - np.mod(1934.1420080 * t, 360.0)
    l = l - 17.20 * np.sin(np.deg2rad(omega))

    # Form the True Obliquity
    oblt = 23.4522940 - 0.01301250 * t + \
    (9.20 * np.cos(np.deg2rad(omega))) / 3600.0

    # Form Right Ascension and Declination
    l = l / 3600.0
    ra = np.rad2deg(np.arctan2(np.sin(np.deg2rad(l)) * \
                        np.cos(np.deg2rad(oblt)), np.cos(np.deg2rad(l))))

    if isinstance(ra, np.ndarray):
        ra[ra < 0.0] += 360.0
    elif ra < 0.0:
        ra = ra + 360.0

    dec = np.rad2deg(np.arcsin(np.sin(np.deg2rad(l)) *
                               np.sin(np.deg2rad(oblt))))

    # convert the internal variables to those listed in the top of the
    # comment section in this code and in the original IDL code.  Quantities
    # are assigned following the advice in Astropy "Working with Angles"
    
    return (longmed,ra,dec,l,oblt)

def convert_pixel_to_data(xy_pix, scale, reference_pixel,
                          reference_coordinate,rotation_deg):
    """Calculate the data coordinate for particular pixel indices.

    Parameters
    ----------
    size : 2d ndarray
        Number of pixels in width and height.
    scale : 2d ndarray
        The size of a pixel (dx,dy) in data coordinates (equivalent to WCS/CDELT)
    reference_pixel : 2d ndarray
        The reference pixel (x,y) at which the reference coordinate is given (equivalent to WCS/CRPIX)
    reference_coordinate : 2d ndarray
        The data coordinate (x, y) as measured at the reference pixel (equivalent to WCS/CRVAL)
    x,y : int or ndarray
        The pixel values at which data coordinates are requested. If none are given,
        returns coordinates for every pixel.

    Returns
    -------
    out : ndarray
        The data coordinates at pixel (x,y).

    Notes
    -----
    This function assumes a gnomic projection which is correct for a detector at the focus
    of an optic observing the Sun.

    Examples
    --------

    """
    cdelt = np.array(scale)
    crpix = np.array(reference_pixel)
    crval = np.array(reference_coordinate)
    crota = rotation_deg * D2R
    cosr  = math.cos(crota)
    sinr  = math.sin(crota)

    # note that crpix[] counts pixels starting at 1

#     coordx = (xy_pix[0] - (crpix[0] - 1)) * cdelt[0] + crval[0]
#     coordy = (xy_pix[1] - (crpix[1] - 1)) * cdelt[1] + crval[1]
#     
#     rot_coordx = cdelt[0]*cosr*coordx - cdelt[1]*sinr*coordy 
#     rot_coordy = cdelt[0]*sinr*coordx + cdelt[1]*cosr*coordy
    
    cent_i = xy_pix[0] - (crpix[0] - 1)
    cent_j = xy_pix[1] - (crpix[1] - 1)
    
    coordx = cdelt[0]*cosr*cent_i - cdelt[1]*sinr*cent_j + crval[0] 
    coordy = cdelt[0]*sinr*cent_i + cdelt[1]*cosr*cent_j + crval[1]


    return coordx, coordy


def convert_data_to_pixel(xy, scale, reference_pixel, reference_coordinate,rotation_deg):
    """Calculate the pixel indices for a given data coordinate.

    Parameters
    ----------
    x, y : float
        Data coordinate in same units as reference coordinate
    scale : 2d ndarray
        The size of a pixel (dx,dy) in data coordinates (equivalent to WCS/CDELT)
    reference_pixel : 2d ndarray
        The reference pixel (x,y) at which the reference coordinate is given (equivalent to WCS/CRPIX)
    reference_coordinate : 2d ndarray
        The data coordinate (x, y) as measured at the reference pixel (equivalent to WCS/CRVAL)

    Returns
    -------
    out : ndarray
        The  pixel coordinates (x,y) at that data coordinate.

    Examples
    --------

    """

    # TODO: Needs to check what coordinate system the data is given in
    cdelt = np.array(scale)
    crpix = np.array(reference_pixel)
    crval = np.array(reference_coordinate)
    crota = -rotation_deg*D2R
    cosr  = math.cos(crota)
    sinr  = math.sin(crota)
    # De-apply any tabular projections.
    # coord = inv_proj_tan(coord)

    # note that crpix[] counts pixels starting at 1
    cent_x = xy[0] - crval[0] 
    cent_y = xy[1] - crval[1]
    
    pixelx = cosr*cent_x/cdelt[0] - sinr*cent_y/cdelt[1] + (crpix[0] - 1) 
    pixely = sinr*cent_x/cdelt[0] + cosr*cent_y/cdelt[1] + (crpix[1] - 1)
    
    
    return pixelx, pixely

def convert_hpc_hcc(xy_arcsec,rsun_meters=None,dsun_meters=None):
    """Converts from Helioprojective-Cartesian (HPC) coordinates into
    Heliocentric-Cartesian (HCC) coordinates. Returns all three dimensions, x, y, z

    xy_arcsec: 2d-tuples [arcsec]
    
    return: 3d-tuples [dimless]
    
    """
    
    x,y = xy_arcsec
    x = x/3600.*D2R
    y = y/3600.*D2R
    
    
    cosx = np.cos(x)
    sinx = np.sin(x)
    cosy = np.cos(y)
    siny = np.sin(y)

    dsun = constants.AU
    if dsun_meters:
        dsun = dsun_meters
        
    rsun = constants.RADIUS
    if rsun_meters:
        rsun = rsun_meters

    q = dsun * cosy * cosx
    distance = q ** 2 - dsun ** 2 + rsun ** 2
    # distance[np.where(distance < 0)] = np.sqrt(-1)
    distance = q - np.sqrt(distance)

    rx = distance * cosy * sinx
    ry = distance * siny
    rz = dsun - distance * cosy * cosx

    return rx, ry, rz
    

def convert_hcc_hpc(xyz_meters, dsun_meters=None):
    """Convert Heliocentric-Cartesian (HCC) to angular
    Helioprojective-Cartesian (HPC) coordinates (in degrees).

    xyz_meters: x,y,z [meter]
    
    return: x,y [arcsec]
    """
    
    x,y,z = xyz_meters

    # Calculate the z coordinate by assuming that it is on the surface of the Sun

    dsun = constants.AU
    if dsun_meters:
        dsun = dsun_meters

    zeta = dsun - z
    distance = np.sqrt(x**2 + y**2 + zeta**2)
    hpcx = np.rad2deg(np.arctan2(x, zeta))*3600. #arcsec
    hpcy = np.rad2deg(np.arcsin(y / distance))*3600. #arcsec

    return hpcx, hpcy

def convert_hcc_hg(xyz,b0_deg=0, l0_deg=0):
    """Convert from Heliocentric-Cartesian (HCC) to
    Stonyhurst Heliographic coordinates (HG) given in degrees, with
    radial output in meters.

    xyz_meters: 3d-tuple
    
    return: 2d-tuple
    """
    x,y,z = xyz
    
    
    cosb = np.cos(np.deg2rad(b0_deg))
    sinb = np.sin(np.deg2rad(b0_deg))

    hecr = np.sqrt(x**2 + y**2 + z**2)
    hgln = np.arctan2(x, z * cosb - y * sinb) + np.deg2rad(l0_deg)
    hglt = np.arcsin((y * cosb + z * sinb) / hecr)

    return np.rad2deg(hgln), np.rad2deg(hglt)

def convert_hg_hcc(lonlat_deg, radius, b0_deg=0, l0_deg=0):
    """Convert from Stonyhurst Heliographic coordinates (given in degrees) to
    Heliocentric-Cartesian coordinates (given in dimensionless).
    
    lonlat_deg: 2d-tuple
    
    return: x,y,z [dimless] as 3d-tuple
    """
    hglon_deg,hglat_deg = lonlat_deg
    
    lon = np.deg2rad(hglon_deg)
    lat = np.deg2rad(hglat_deg)

    cosb = np.cos(np.deg2rad(b0_deg))
    sinb = np.sin(np.deg2rad(b0_deg))

    lon = lon - np.deg2rad(l0_deg)

    cosx = np.cos(lon)
    sinx = np.sin(lon)
    cosy = np.cos(lat)
    siny = np.sin(lat)
    
    # Perform the conversion.
    x = radius*cosy * sinx
    y = radius*(siny * cosb - cosy * cosx * sinb)
    zz =radius*(siny * sinb + cosy * cosx * cosb)

    return x, y, zz
    
def convert_hg_hpc(lonlat_deg, b0_deg=0, l0_deg=0, rsun_meters=None,dsun_meters=None):
    """Convert from Heliographic coordinates (HG) to Helioprojective-Cartesian
    (HPC).
    
    lonlat_deg: 2d-tuple
    
    return: 
    """
    
    rsun = constants.RADIUS
    if rsun_meters:
        rsun = rsun_meters

    tempxyz = convert_hg_hcc(lonlat_deg, rsun, b0_deg=b0_deg, l0_deg=l0_deg)
    x, y = convert_hcc_hpc(tempxyz, dsun_meters=dsun_meters)
    return x, y

def convert_hpc_hg(xy_arcsec, b0_deg=0, l0_deg=0,rsun_meters=None,dsun_meters=None):
    """Convert from Helioprojective-Cartesian (HPC) to Heliographic coordinates
    (HG) in degrees.
    
    xy: 2d-tuple
    
    return: 2d-tuple
    """
    rsun = constants.RADIUS
    if rsun_meters:
        rsun = rsun_meters
        
    tempxyz = convert_hpc_hcc(xy_arcsec, rsun_meters=rsun_meters,dsun_meters=dsun_meters)
    lon, lat = convert_hcc_hg(tempxyz,b0_deg=b0_deg, l0_deg=l0_deg)
    return lon, lat

def xyz(xy,r):
    z = math.sqrt(r**2 - xy[0]**2 - xy[1]**2)
    return xy[0],xy[1],z
