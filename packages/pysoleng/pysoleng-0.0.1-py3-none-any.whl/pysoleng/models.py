"""
Author: Pedro L. Magalhães
Email: pmlpm@posteo.de
Date: 2023
"""

#******************************************************************************
#******************************************************************************

# import libraries

import math

# import pysoleng.solar as ps

from . import solar as ps

from .timeplace import Location, Plane, day_of_the_year

import datetime as dt

def tilted_plane_irradiance_isotropic(
        site: Location,
        surface: Plane,
        local_time: dt.datetime,
        site_ground_reflectance: float,
        site_horizontal_total,
        site_horizontal_diffuse,
        use_average_ratio: bool = True,
        sample_duration_seconds: int = 3600):    
    """
    Return the irradiance on tilted plane using the isotropic model.

    This function converts irradiation data obtained for a horizontal plane 
    into data that concerns a tilted plane, such as a wall or a solar module.    

    Parameters
    ----------
    site_longitude : float
        The site longitude in radians. If positive, it is west of Greenwich.
    site_latitude : float
        The site latitude in radians. If positive, it is north of the Equator.
    site_ground_reflectance : float
        The average ground reflectance (0<=,<=1) in the site\'s vinicity.
    plane_slope_horizontal : float
        The slope the target plane forms with the horizontal plane.
    plane_azimuth : float
        The azimuth the target plane has, in radians. If zero, it faces south.
        If pi/2, it faces west. If -pi/2, it faces east.
    star_altitude : float
        The local star\'s altitude as per the horizontal coordinate system.
        If zero, the star is on the horizon. If pi/2, it is overhead.
    star_azimuth : float
        The local star\' azimuth, as per the horizontal coordinate system.
        It uses the same convention as the plane_azimuth variable.
    site_time : datetime
        A datetime object for the local time, not the apparent solar time.
    site_horizontal_total : float
        The total irradiance on the horizontal plane for the site. It should
        concern the time period indicated by site_time.
    site_horizontal_diffuse : float
        The diffuse component of the total irradiance on the horizontal plane.
        It should concern the time period indicated by site_time.

    Return
    ------
    I_tilted_total : float
        Subset of the original series with the n first values.
    I_tilted_beam : float
        Subset of the original series with the n first values.
    I_tilted_sky_diffuse : float
        Subset of the original series with the n first values.
    I_tilted_albedo : float
        Subset of the original series with the n first values.

    See Also
    --------
    tail : Return the last n elements of the Series.

    Examples
    --------
    >>> s = pd.Series(['Ant', 'Bear', 'Cow', 'Dog', 'Falcon',
    ...                'Lion', 'Monkey', 'Rabbit', 'Zebra'])
    >>> s.head()
    0   Ant
    1   Bear
    2   Cow
    3   Dog
    4   Falcon
    dtype: object

    With the ``n`` parameter, we can change the number of returned rows:

    >>> s.head(n=3)
    0   Ant
    1   Bear
    2   Cow
    dtype: object
    """
    
    #**************************************************************************
    
    # verify inputs
    
    #**************************************************************************
    
    # convert the local time into solar time
    
    site_ast = ps.lst_to_ast(local_time, site)
    
    # get the declination angle
    
    declination_angle = math.radians(
        ps.declination_angle(
            day_of_the_year(local_time)
            )
        )
    
    # get the solar hour angle
    
    hour_angle = ps.hour_angle(site_ast)
    
    #**************************************************************************
    
    # compute ratio
    
    R_b = ps.beam_irradiation_ratio(
        declination_angle, 
        math.radians(site.latitude),   
        surface.slope, 
        surface.azimuth, 
        hour_angle,
        return_average_ratio=use_average_ratio,
        sample_duration_seconds=sample_duration_seconds) # half an hour each way
    
    #**************************************************************************
    
    # get the beam irradiation contribution to the global horiz. irradiation
    
    I_horizontal_beam = site_horizontal_total-site_horizontal_diffuse
    
    #**************************************************************************
    
    I_tilted_beam = R_b*I_horizontal_beam
    
    I_tilted_sky_diffuse = (
            site_horizontal_diffuse*
            (1+math.cos(surface.slope))/2
            )
    
    I_tilted_albedo = (
            site_horizontal_total*
            site_ground_reflectance*
            (1-math.cos(surface.slope))/2
            )
    
    I_tilted_total = I_tilted_beam+I_tilted_sky_diffuse+I_tilted_albedo

    #**************************************************************************
    #**************************************************************************

    # return function out
    
    return I_tilted_total, I_tilted_beam, I_tilted_sky_diffuse, I_tilted_albedo

#******************************************************************************
#******************************************************************************