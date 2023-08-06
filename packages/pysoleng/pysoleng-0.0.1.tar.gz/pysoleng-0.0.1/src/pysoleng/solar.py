"""
Author: Pedro L. Magalhães
Email: pmlpm@posteo.de
Date: 2023
"""

#******************************************************************************
#******************************************************************************

# libraries

# standard

import math

import datetime as dt

from zoneinfo import ZoneInfo

# local, external

from numpy import sign as np_sign

# local, internal

from .timeplace import Location, day_of_the_year

from .utils import simplify_angle

#******************************************************************************
#******************************************************************************
    
def cosine_incidence_angle(
        declination_angle: float,       # delta: -23.5 deg <= ... <= 23.5 deg
        latitude: float,                # phi?
        plane_slope_horizontal: float,  # beta: -180 <= ... <= 180
        plane_azimuth_south: float,     # gamma: -180 <= ... <= 180 deg
        hour_angle: float,              # omega: 
        ):
    """Returns the cosine of the incidence angle on a given surface."""
    
    # The angle θ may exceed 90 ◦ , which means that the sun is behind the surface. Also, when
    # using Equation 1.6.2, it is necessary to ensure that the earth is not blocking the sun (i.e.,
    # that the hour angle is between sunrise and sunset).
    
    # angles in radians
    
    return (
        math.sin(declination_angle)*
        math.sin(latitude)*
        math.cos(plane_slope_horizontal)
        -
        math.sin(declination_angle)*
        math.cos(latitude)*
        math.sin(plane_slope_horizontal)*
        math.cos(plane_azimuth_south)
        +
        math.cos(declination_angle)*
        math.cos(latitude)*
        math.cos(plane_slope_horizontal)*
        math.cos(hour_angle)
        +
        math.cos(declination_angle)*
        math.sin(latitude)*
        math.sin(plane_slope_horizontal)*
        math.cos(plane_azimuth_south)*
        math.cos(hour_angle)
        +
        math.cos(declination_angle)*
        math.sin(plane_slope_horizontal)*
        math.sin(plane_azimuth_south)*
        math.sin(hour_angle)
        )

#******************************************************************************
#******************************************************************************

def declination_angle(day_year: int or float):
    """Returns the declination angle in degrees using the day of the year."""
    
    # day of the year, d: 1 (1st of January) <= d <= 365 (31st of December)
    
    return (
        23.45*math.sin(math.pi*2*(284+day_year)/365)
        )

#******************************************************************************
#******************************************************************************
    
def declination_angle_spencer1971(day_year: int or float):
    """Returns the declination angle in degrees using the day of the year."""
    
    # day of the year, d: 1 (1st of January) <= d <= 365 (31st of December)
    
    B = math.radians((day_year-1)*360/365)
    
    return (180/math.pi)*(
        0.006918
        -
        0.399912*math.cos(B)
        +
        0.070257*math.sin(B)
        -
        0.006758*math.cos(2*B)
        +
        0.000907*math.sin(2*B)
        -
        0.002697*math.cos(3*B)
        +
        0.00148*math.sin(3*B)
        )

#******************************************************************************
#******************************************************************************

# cosine of the solar zenith angle

def cosine_zenith_angle(latitude, declination_angle, hour_angle):
    """Returns the cosine of the zenith angle for a given time and location."""
    
    return (
        math.cos(latitude)*
        math.cos(declination_angle)*
        math.cos(hour_angle)
        +
        math.sin(latitude)*
        math.sin(declination_angle)
        )

#******************************************************************************
#******************************************************************************

def solar_altitude_angle(latitude, declination_angle, hour_angle) -> float:
    """Returns the solar altitude angle in radians for a given time and place."""
    
    return (
        math.pi/2-
        math.acos(
            cosine_zenith_angle(latitude,
                                declination_angle,
                                hour_angle)
            )
        )

#******************************************************************************
#******************************************************************************

def solar_azimuth_angle(latitude: float or int, 
                        declination_angle: float or int, 
                        zenith_angle: float or int, 
                        hour_angle: float or int,
                        abs_tol: float = 1e-3) -> float:
    """Returns the solar azimuth angle in radians for a given time and place."""
    
    # Duffie and Beckman (2013), page 15
    # TODO: verify if all this is really necessary
    cos_angle = (
        math.cos(zenith_angle)*
        math.sin(latitude)-
        math.sin(declination_angle)
        )/(math.sin(zenith_angle)*
           math.cos(latitude))
           
    # if this cosine exceeds 1 plus the tolerance
           
    if abs(cos_angle) > 1+abs_tol:
        
        # raise error
        
        raise ValueError(
            'The inputs violate the trigonometric relations underpinning this '
            +'equation.')
        
    elif cos_angle > 1: 
        
        # if the cosine is above 1 in amplitude but does not exceed the tolera-
        # nce, then round it
        
        cos_angle = round(cos_angle)
        
    # otherwise, the cosine is fine
    
    return (
        np_sign(hour_angle)*
        abs(
            math.acos(
                cos_angle
                )
            )
        )

#******************************************************************************
#******************************************************************************

def sunset_hour_angle(declination_angle: float or int, 
                      latitude: float or int) -> float:
    """Returns the hour angle when sunset occurs for a given day and place."""
    
    return (
        math.acos(
            -math.tan(latitude)*
            math.tan(declination_angle)
            )
        )

#******************************************************************************
#******************************************************************************

def sunrise_hour_angle(declination_angle: float or int, 
                       latitude: float or int) -> float:
    """Returns the hour angle when sunrise occurs for a given day and place."""
    
    return (
        -math.acos(
            -math.tan(latitude)*
            math.tan(declination_angle)
            )
        )

#******************************************************************************
#******************************************************************************

def sunrise_hour_angle_meeus(declination_angle_radians: float or int, 
                             latitude_radians: float or int) -> float:
    """Returns the hour angle for when the sun is rising."""
    
    # Source: J. Meeus (1998) via https://gml.noaa.gov/grad/solcalc/
    
    # the function has an extra "-" (minus) to render hour angles negative east
    # of Greenwich
    
    return -math.acos(
        math.cos(math.radians(90.833))/
        (math.cos(latitude_radians)*math.cos(declination_angle_radians))
        -math.tan(latitude_radians)*math.tan(declination_angle_radians)
        )

#******************************************************************************
#******************************************************************************

def sunset_hour_angle_meeus(declination_angle_radians: float or int, 
                            latitude_radians: float or int) -> float:
    """Returns the hour angle for when the sun is setting."""
    
    # Source: J. Meeus (1998) via https://gml.noaa.gov/grad/solcalc/
    
    return -sunrise_hour_angle_meeus(
        declination_angle_radians, 
        latitude_radians)

#******************************************************************************
#******************************************************************************

def number_sunlight_hours(declination_angle: float or int, 
                          latitude: float or int) -> float:
    """
    Returns the number of sunlight hours for a location as a function of the
    declination angle and the latitude, which should be provided in degrees.

    Parameters
    ----------
    declination_angle : float
        The Earth\'s declination angle in degrees.
    latitude : float
        The location\'s latitude in degrees (positive North of the equator).

    Returns
    -------
    float
        The number of sunlight hours according to the input data.

    """
    # Duffie and Beckman (2013): page 17
    
    # 15º is 1 hour
    # 15*math.pi/180 is 1 hour
    
    return (
        math.acos(-math.tan(math.radians(declination_angle))*
                  math.tan(math.radians(latitude)))*
        2/
        (15*math.pi/180)
        )

#******************************************************************************
#******************************************************************************

# ratio between the tilted and horizontal irradiation, instantaneous

def beam_irradiation_ratio(declination_angle, 
                           latitude,   
                           plane_slope_horizontal, 
                           plane_azimuth_south, 
                           hour_angle,
                           return_average_ratio: bool = True,
                           sample_duration_seconds: int = 3600):
    
    # calculate the sunrise and sunset hour angles
    
    sunrise_ha = sunrise_hour_angle(declination_angle, latitude)
    
    sunset_ha = sunset_hour_angle(declination_angle, latitude)
    
    # check which method is to be used
    
    if return_average_ratio:
        
        # one instant is before sunset adjust and use sunrise as the first inst.
        # one instant is past sunset: adjust and use sunset as the second inst.
        # both instants are past sunset: rb = 0
        # both instants are before sunrise: rb = 0      
        
        # 3600 seconds equals 15º
        
        ha_init = hour_angle - .5*sample_duration_seconds*(15*math.pi/180)/3600
        
        ha_fin = hour_angle + .5*sample_duration_seconds*(15*math.pi/180)/3600
    
        # both instants are past sunset: rb = 0
        
        if ha_init > sunset_ha and ha_fin > sunset_ha:
            
            return 0
                
        # both instants are before sunrise: rb = 0
        
        if ha_init < sunrise_ha and ha_fin < sunrise_ha:
            
            return 0
            
        # one instant is past sunset: adjust and use sunset as the second inst.
        
        if ha_fin > sunset_ha:
            
            ha_fin = sunset_ha
            
        # one instant is before sunset adjust and use sunrise as the first inst.
            
        if ha_init < sunrise_ha:
            
            ha_init = sunrise_ha

        #**********************************************************************
        #**********************************************************************
            
        rb = average_beam_irradiation_ratio(
            declination_angle, 
            latitude,   
            plane_slope_horizontal, 
            plane_azimuth_south, 
            ha_init, 
            ha_fin)
        
        #**********************************************************************
        #**********************************************************************
    
    else:
        
        # instantaneous method
        
        # before sunrise
        
        if hour_angle < sunrise_ha:
            
            # no direct radiation
            
            return 0 # TODO: reach this statement
        
        # after sunset
        
        if hour_angle > sunset_ha:
            
            # no direct radiation
            
            return 0 # TODO: reach this statement
        
        # between sunrise and sunset
        
        rb = instantaneous_beam_irradiation_ratio(
            declination_angle, 
            latitude,
            plane_slope_horizontal, 
            plane_azimuth_south, 
            hour_angle)
        
        #**********************************************************************
        #**********************************************************************
        
    #**************************************************************************
    #**************************************************************************
    
    # adjust output
    
    if rb < 0:
        
        return 0 # TODO: reach this statement
        
    else:
        
        return rb

#******************************************************************************
#******************************************************************************

# ratio between the tilted and horizontal irradiation, instantaneous

def instantaneous_beam_irradiation_ratio(declination_angle, 
                                         latitude,   
                                         plane_slope_horizontal, 
                                         plane_azimuth_south, 
                                         hour_angle):
    """Returns the instantaneous tilted-plane-to-horizontal beam irradiation ratio."""
    
    rb = (
        cosine_incidence_angle(
            declination_angle,
            latitude, 
            plane_slope_horizontal, 
            plane_azimuth_south, 
            hour_angle
            )/
        cosine_zenith_angle(
            latitude, 
            declination_angle, 
            hour_angle)
        )
    
    # adjust output
    
    if rb < 0:
        
        return 0 # TODO: reach this statement
        
    else:
        
        return rb

#******************************************************************************
#******************************************************************************

# ratio between the tilted and horizontal irradiation, average

def average_beam_irradiation_ratio(declination_angle, 
                                   latitude,   
                                   plane_slope_horizontal, 
                                   plane_azimuth_south, 
                                   initial_hour_angle, 
                                   final_hour_angle):
    """Returns the average tilted-plane-to-horizontal beam irradiation ratio."""
    
    # Source: Duffie and Beckman, 2013, page 88
                                       
    a = ((math.sin(declination_angle)*
          math.sin(latitude)*
          math.cos(plane_slope_horizontal)
          -
          math.sin(declination_angle)*
          math.cos(latitude)*
          math.sin(plane_slope_horizontal)*
          math.cos(plane_azimuth_south))*
         (final_hour_angle-initial_hour_angle)
         +
         (math.cos(declination_angle)*
          math.cos(latitude)*
          math.cos(plane_slope_horizontal)
          +
          math.cos(declination_angle)*
          math.sin(latitude)*
          math.sin(plane_slope_horizontal)*
          math.cos(plane_azimuth_south))*
         (math.sin(final_hour_angle)-math.sin(initial_hour_angle))
         -
         (math.cos(declination_angle)*
          math.sin(plane_slope_horizontal)*
          math.sin(plane_azimuth_south))*
         (math.cos(final_hour_angle)-math.cos(initial_hour_angle))
         )
    
    b = (
        math.cos(latitude)*
        math.cos(declination_angle)*
        (math.sin(final_hour_angle)-math.sin(initial_hour_angle))
        +
        math.sin(latitude)*
        math.sin(declination_angle)*
        (final_hour_angle-initial_hour_angle)
        )
    
    rb = a/b

    # adjust output
    
    if rb < 0:
        
        return 0
        
    else:
        
        return rb
    
#******************************************************************************
#******************************************************************************

# extraterrestrial irradiation according to spencer 1971, as cited by iqbal 1983

def extraterrestrial_radiation_normal_spencer1971(day_year: float or int,
                                                  Gsc: float = 1367.0):
    """Returns the extraterrestrial radiation using the Spencer approximation."""
    
    # Source: Duffie and Beckman, 2013, page 9
    # Credited to: Spencer (1971) via Iqbal (1983)
    
    # Gsc = 1367 # W/m2
        
    # spencer approximation
    
    B = math.radians((day_year-1)*360/365)
    
    return (
        Gsc*
        (1.000110+
         0.034221*math.cos(B)+
         0.001280*math.sin(B)+
         0.000719*math.cos(2*B)+
         0.000077*math.sin(2*B)
         )
        )
                                      
#******************************************************************************
#******************************************************************************

# extraterrestrial irradiation

def extraterrestrial_radiation_normal_duffie2013(day_year: float or int,
                                                 Gsc: float = 1367.0):
    """Returns the extraterrestrial radiation using a sinusoidal approximation."""
    
    # Duffie and Beckman (2013): page 9
    
    # Gsc = 1367 # W/m2
    
    # default

    return (
        Gsc*
        (1+
         0.033*
         math.cos(
             math.radians(
                 day_year*360/365)
             )
         )
        )
    
#******************************************************************************
#******************************************************************************

def get_air_mass(zenith_angle, altitude, approx=''):
    
    if approx == 'kandy':
        
        # Kasten and Young (1989)
        
        return (
            math.exp(-0.0001184*altitude)
            /
            (math.cos(zenith_angle)+
             0.5057*(96.080-math.degrees(zenith_angle))**-1.634)
            )
    
        #**********************************************************************
        #**********************************************************************
    
    else:
        
        # should only be used for zenith angles between 0 and 70
        
        return 1/math.cos(zenith_angle)

        #**********************************************************************
        #**********************************************************************
    
#******************************************************************************
#******************************************************************************

# apparent solar time

def ast(hour_angle_radians: float or int,
        year: int,
        month: int, 
        day: int,
        tzinfo: ZoneInfo = None) -> dt.datetime:
    """Returns the apparent solar time based on the hour angle."""
    
    # relationship between the ast and the hour angles:    
    # 00:00 >> -pi rad
    # 12:00 >> 0 rad
    # 24:00 >> pi rad
    
    hours_24 = 12+hour_angle_radians/(math.pi/12)
    
    hours = math.floor(hours_24)
    
    minutes_unrounded = (hours_24-hours)*60
    
    minutes = math.floor(minutes_unrounded)
    
    seconds = math.floor((minutes_unrounded-minutes)*60)
    
    if type(tzinfo) == type(None):
        
        # no time zone information provided
        
        return dt.datetime(
            year=year,
            month=month,
            day=day,
            hour=hours,
            minute=minutes,
            second=seconds)
    
    else: # time zone information provided
    
        return dt.datetime(
            year=year,
            month=month,
            day=day,
            hour=hours,
            minute=minutes,
            second=seconds,
            tzinfo=tzinfo)
    
    #**************************************************************************
    #**************************************************************************
    
#******************************************************************************
#******************************************************************************

# hour angle

def hour_angle(ast: dt.datetime):
    """Returns the hour angle using the apparent solar time."""
    
    # return the hour angle in radians:    
    # 00:00 >> -pi rad
    # 12:00 >> 0 rad
    # 24:00 >> pi rad
    
    solar_time_hours = (
        (ast.hour-12)+
        ast.minute/60+
        ast.second/3600
        )
    
    return solar_time_hours*math.pi/12

#******************************************************************************
#******************************************************************************

def lst_to_ast_timedelta(lst: dt.datetime, 
                         place: Location, 
                         use_integer_doty: bool = False,
                         equation_time_minutes: float = None) -> dt.timedelta:
    """Returns the time difference between AST and LST."""
    
    # identify the type of crs
    
    if place.crs_string != 'epsg:4326':
        
        raise ValueError('The location is defined using an unsupported CRS.')
        
    # get the longitudes ([-180,180] range) and convert (to [0, 360] range)
        
    # get the local longitude (range: [-180,180]) and convert (range: [0,360])
    
    local_longitude = simplify_angle(place.longitude+360)
    
    # get the local standard meridian longitude and convert
    
    local_meridian_longitude = simplify_angle(
        place.local_standard_meridian_longitude(lst)+360)
    
    # if degrees west are positive:
    # i) delta > 0 means the meridian is to the west (more minutes)
    # ii) delta < 0 means the meridian is to the east (less minutes)
    
    day_year = day_of_the_year(lst, as_integer=use_integer_doty)
    
    if type(equation_time_minutes) == type(None):
        
        equation_time_minutes = equation_of_time_minutes(
            day_year
            )
    
    return dt.timedelta(
        seconds=(
            -4*60*(local_meridian_longitude-local_longitude)
            +
            60*equation_time_minutes
            )
        )

    #**************************************************************************
    #**************************************************************************
    
#******************************************************************************
#******************************************************************************

def lst_to_ast(lst: dt.datetime, 
               place: Location, 
               use_integer_doty: bool = False,
               equation_time_minutes: float = None) -> dt.datetime:
    """Convert the local standard time to the apparent solar time."""

    return lst + lst_to_ast_timedelta(lst, 
                                      place, 
                                      use_integer_doty,
                                      equation_time_minutes)

#******************************************************************************
#******************************************************************************

def ast_to_lst(ast: dt.datetime, 
               place: Location, 
               use_integer_doty: bool = False,
               equation_time_minutes: float = None) -> dt.datetime:
    """Convert the apparent solar time to the local standard time."""

    return ast - lst_to_ast_timedelta(ast, 
                                      place, 
                                      use_integer_doty,
                                      equation_time_minutes)

#******************************************************************************
#******************************************************************************

# equation of time

def equation_of_time_minutes(day_year):
    """Returns the time difference known as the equation of time, in minutes."""
    
    # Kalogirou (2009): 
        
    B = math.radians((day_year-81)*360/364)
    
    # returns the time difference in minutes
    
    return (
        9.87*math.sin(2*B)
        -
        7.53*math.cos(B)
        -
        1.5*math.sin(B)
        )

#******************************************************************************
#******************************************************************************

# equation of time

def equation_of_time_minutes_spencer1971(day_year):
    """Returns the time difference known as the equation of time, in minutes."""
    
    # Duffie and Beckman (2013), page 9 and 11
        
    B = math.radians((day_year-1)*360/365)
    
    # returns the time difference in minutes
    
    return 229.2*(
        0.000075
        +
        0.001868*math.cos(B)
        -
        0.032077*math.sin(B)
        -
        0.014615*math.cos(2*B)
        -
        0.04089*math.sin(2*B)
        )
    
#******************************************************************************
#******************************************************************************

def equation_of_time_radians_Smart(mean_solar_anomaly: float,
                                   earth_orbits_eccentricity: float,
                                   mean_solar_longitude: float,
                                   obliquity_ecliptic: float) -> float:
    """Returns the time difference known as the equation of time, in radians."""
    
    y = math.tan(obliquity_ecliptic/2)**2
    
    return (
        y*math.sin(2*mean_solar_longitude)
        -
        2*earth_orbits_eccentricity*math.sin(mean_solar_anomaly)
        +
        4*earth_orbits_eccentricity*y*math.sin(mean_solar_anomaly)*math.cos(2*mean_solar_longitude)
        -
        0.5*(y**2)*math.sin(4*mean_solar_longitude)
        -
        (5/4)*(earth_orbits_eccentricity**2)*math.sin(2*mean_solar_anomaly)
        )   

#******************************************************************************
#******************************************************************************

def julian_day(year, 
               month, 
               day_month, 
               calendar: str = 'gregorian'):
    """Returns the Julian Day (JD) for a given date and calendar."""
    
    M = month
    
    Y = year
    
    D = day_month
    
    # adjustments
    
    if M == 1 or M == 2:
        
        Y = Y    -1
        
        M = M + 12
        
    if calendar == 'gregorian':
        
        A = math.floor(Y/100)
        
        B = 2 - A + math.floor(A/4)
        
    elif calendar == 'julian':
        
        B = 0
    
    else:
        
        raise NotImplementedError
        
    # function
    
    return (
        math.floor(365.25*(Y+4716))
        +
        math.floor(30.6001*(M+1))
        +
        D
        +
        B
        -
        1524.5
        )

#******************************************************************************
#******************************************************************************

def julian_day_zero(year,  
                    calendar: str = 'gregorian'):
    
    if calendar != 'gregorian':
        
        raise NotImplementedError
    
    Y = year - 1
    
    A = math.floor(Y/100)
    
    return (
        math.floor(365.25*Y)
        -
        A
        +
        math.floor(A/4)
        +
        1721424.5)

#******************************************************************************
#******************************************************************************

def modified_julian_day(julian_day: float or int):
    """Returns the Modified Julian Day (MJD) from the Julian Day (JD)."""
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 63
    
    return julian_day-2400000.5

#******************************************************************************
#******************************************************************************

def time_in_julian_centuries_since_j2000(julian_ephemeris_day: float):
    
    return (julian_ephemeris_day-2451545)/36525

#******************************************************************************
#******************************************************************************

def calendar_date(julian_day: float):
    """Returns the calendar date for positive Julian Day (JD) numbers."""
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 63
    
    if julian_day < 0:
        
        raise ValueError(
            'This method is only valid for non-negative Julian Day numbers.')

    #**************************************************************************
    
    Z = math.floor(julian_day+0.5)
    
    F = math.fmod(julian_day+0.5,1)

    #**************************************************************************
    
    if Z < 2299161:
        
        A = Z
        
    else: # >= 2299161
    
        alpha = math.floor((Z-1867216.25)/36524.25)
        
        A = Z + 1 + alpha - math.floor(alpha/4)
    
    #**************************************************************************
    
    B = A + 1524
    C = math.floor((B-122.1)/365.25)
    D = math.floor(365.25*C)
    E = math.floor((B-D)/30.6001)
    
    #**************************************************************************
    
    day_month = B - D - math.floor(30.6001*E) + F
    
    # month
    
    if E < 14:
        
        month_number = E - 1
        
    elif E == 14 or E == 15:
        
        month_number = E -13 # = 1 or 2
        
    # else:
        
    #     # might not be reachable
        
    #     raise NotImplementedError 
        
    # year
        
    if month_number > 2:
        
        year = C - 4716
        
    elif month_number == 1 or month_number == 2:
        
        year = C - 4715
        
    # else:
        
    #     # might not be reachable
        
    #     raise NotImplementedError
        
    # return statement
    
    return year, month_number, day_month

#******************************************************************************
#******************************************************************************

def mean_elongation_moon_from_sun(julian_centuries_since_j2000: float)-> float:
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 144
    
    return (
        297.85036
        +
        445267.111480*julian_centuries_since_j2000
        -
        0.0019142*(julian_centuries_since_j2000**2)
        +
        (julian_centuries_since_j2000**3)/189474
        )

#******************************************************************************
#******************************************************************************

def mean_anomaly_sun(julian_centuries_since_j2000: float) -> float:
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 144
    
    return (
        357.52772
        +
        35999.050340*julian_centuries_since_j2000
        -
        0.0001603*(julian_centuries_since_j2000**2)
        -
        (julian_centuries_since_j2000**3)/300000
        )

#******************************************************************************
#******************************************************************************

def mean_anomaly_sun_simpler(julian_centuries_since_j2000: float) -> float:
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 163
    
    return (
        357.52911
        +
        35999.05029*julian_centuries_since_j2000
        -
        0.0001537*(julian_centuries_since_j2000**2)
        )

#******************************************************************************
#******************************************************************************

def mean_anomaly_moon(julian_centuries_since_j2000: float) -> float:
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 144
    
    return (
        134.96298
        +
        477198.867398*julian_centuries_since_j2000
        +
        0.0086972*(julian_centuries_since_j2000**2)
        +
        (julian_centuries_since_j2000**3)/56250
        )

#******************************************************************************
#******************************************************************************

def moon_argument_latitude(julian_centuries_since_j2000: float) -> float:
    
    return (
        93.27191
        +
        483202.017538*julian_centuries_since_j2000
        -
        0.0036825*(julian_centuries_since_j2000**2)
        +
        (julian_centuries_since_j2000**3)/327270
        )

#******************************************************************************
#******************************************************************************

def longitude_ascending_node_moon_mean_orbit_ecliptic_from_mean_equinox(
        julian_centuries_since_j2000: float) -> float:
    
    return (
        125.04452
        -
        1934.136261*julian_centuries_since_j2000
        +
        0.0020708*(julian_centuries_since_j2000**2)
        +
        (julian_centuries_since_j2000**3)/450000
        )


#******************************************************************************
#******************************************************************************

def equation_of_time_degrees_meeus1998(mean_solar_longitude: float,
                                       apparent_right_ascension_sun: float,
                                       obliquity_ecliptic: float,
                                       nutation_longitude: float):
    """Returns the equation of time in degrees, as found in Meeus (1998)."""
        
    return (
        mean_solar_longitude
        -
        0.0057183
        -
        apparent_right_ascension_sun
        +
        nutation_longitude*math.cos(obliquity_ecliptic)
        )

#******************************************************************************
#******************************************************************************

def mean_solar_longitude_vsop87(julian_day: float) -> float:
    """Returns the Sun's mean longitude in degrees according to VSOP87 theory."""
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 163
    
    tau = (julian_day-2451545.0)/365250
    
    base_angle = simplify_angle(
        280.4664567
        +
        360007.6982779*tau
        +
        0.03032028*(tau**2)
        +
        (1/49931)*(tau**3)
        -
        (1/15300)*(tau**4)
        -
        (1/2000000)*(tau**5),
        angle_in_degrees=True        
        )
    
    return base_angle if base_angle >= 0 else base_angle+360

#******************************************************************************
#******************************************************************************

def mean_longitude_sun(julian_centuries_since_j2000: float) -> float:
    """Returns the Sun's mean longitude in degrees."""
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 163
    
    return (
        280.46646
        +
        36000.76983*julian_centuries_since_j2000
        +
        0.0003032*(julian_centuries_since_j2000**2)
        )

#******************************************************************************
#******************************************************************************

def mean_longitude_sun_simple(julian_centuries_since_j2000: float) -> float:
    """Returns the Sun's mean longitude in degrees using a linear function."""
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 144
    
    base_angle = simplify_angle(
        280.4665+36000.7698*julian_centuries_since_j2000,
        angle_in_degrees=True        
        )
    
    return base_angle if base_angle >= 0 else base_angle+360

#******************************************************************************
#******************************************************************************

def mean_longitude_moon_simple(julian_centuries_since_j2000: float) -> float:
    
    # Source: J. Meeus, Astronomical Algorithms, 1998, page 144
    
    return 218.3165+481267.8813*julian_centuries_since_j2000

#******************************************************************************
#******************************************************************************

def nutation_obliquity(julian_centuries_since_j2000: float) -> float:
    """Returns the Earth's nutation in obliquity."""
    
    D = mean_elongation_moon_from_sun(julian_centuries_since_j2000)
    
    M = mean_anomaly_sun(julian_centuries_since_j2000)
    
    M_line = mean_anomaly_moon(julian_centuries_since_j2000)
    
    F = moon_argument_latitude(julian_centuries_since_j2000)
    
    sigma = (
        longitude_ascending_node_moon_mean_orbit_ecliptic_from_mean_equinox(
            julian_centuries_since_j2000)
        )
    
    cos_args = [D, M, M_line, F, sigma]
    
    cos_coef = [
        (92025 + 8.9*julian_centuries_since_j2000),
        (5736 - 3.1*julian_centuries_since_j2000),
        (977 - 0.5*julian_centuries_since_j2000),
        (0.5*julian_centuries_since_j2000 - 895),
        (54 - 0.1*julian_centuries_since_j2000),
        (224 - 0.6*julian_centuries_since_j2000),
        (129 - 0.1*julian_centuries_since_j2000),
        (0.3*julian_centuries_since_j2000 - 95),
        200,
        -70,
        -53,
        -33,
        +26,
        +32,
        +27,
        -24,
        +16,
        +13,
        -12,
        -10,
        -8,
        +7,
        -7,
        +9,
        +7,
        +6,
        +5,
        +3,
        -3,
        +3,
        +3,
        -3,
        -3,
        +3,
        +3,
        +3,
        +3,
        +3,
        ]
    
    arguments_table = [
        (0,0,0,0,1),# w = cos(w5)*(92025 + 8.9*T)
        (-2,0,0,2,2),# w = w + cos(2*(w4 - w1 + w5))*(5736 - 3.1*T)
        (0,0,0,2,2),# w = w + cos(2*(w4 + w5))*(977 - 0.5*T)
        (0,0,0,0,2),# w = w + cos(2*w5)*(0.5*T - 895)
        (0,1,0,0,0),# w = w + cos(w2)*(54 - 0.1*T)
        (-2,1,0,2,2),# w = w + cos(w2 + 2*(w4 - w1 + w5))*(224 - 0.6*T)
        (0,0,1,2,2),# w = w + cos(w3 + 2*(w4 + w5))*(129 - 0.1*T)
        (-2,-1,0,2,2),# w = w + cos(2*(w4 - w1 + w5) - w2)*(0.3*T - 95)
        (0,0,0,2,1),# w = w + 200*cos(2*w4 + w5)
        (-2,0,0,2,1),# w = w - 70*cos(2*(w4 - w1) + w5)
        (0,0,0,2,2),# w = w - 53*cos(2*(w4 + w5) - w3)
        (0,0,1,0,1),# w = w - 33*cos(w3 + w5)
        (2,0,-1,2,2),# w = w + 26*cos(2*(w1 + w4 + w5) - w3)
        (0,0,-1,0,1),# w = w + 32*cos(w5 - w3)
        (0,0,1,2,1),# w = w + 27*cos(w3 + 2*w4 + w5)
        (0,0,-2,2,1),# w = w - 24*cos(2*(w4 - w3) + w5)
        (2,0,0,2,2),# w = w + 16*cos(2*(w1 + w4 + w5))
        (0,0,2,2,2),# w = w + 13*cos(2*(w3 + w4 + w5))
        (-2,0,1,2,2),# w = w - 12*cos(w3 + 2*(w4 - w1 + w5))
        (0,0,-1,2,1),# w = w - 10*cos(2*w4 + w5 - w3)
        (2,0,-1,0,1),# w = w - 8*cos(2*w1 - w3 + w5)
        (-2,2,0,2,2),# w = w + 7*cos(2*(w2 - w1 + w4 + w5))
        (0,0,1,0,0),# w = w - 7*cos(w3)
        (0,1,0,0,1),# w = w + 9*cos(w2 + w5)
        (-2,0,1,0,1),# w = w + 7*cos(w3 + w5 - 2*w1)
        (0,-1,0,0,1),# w = w + 6*cos(w5 - w2)
        (2,0,-1,2,1),# w = w + 5*cos(2*(w1 + w4) - w3 + w5)
        (2,0,1,2,2),# w = w + 3*cos(w3 + 2*(w4 + w1 + w5))
        (0,1,0,2,2),# w = w - 3*cos(w2 + 2*(w4 + w5))
        (0,-1,0,2,2),# w = w + 3*cos(2*(w4 + w5) - w2)
        (2,0,0,2,1),# w = w + 3*cos(2*(w1 + w4) + w5)
        (-2,0,2,2,2),# w = w - 3*cos(2*(w3 + w4 + w5 - w1))
        (-2,0,1,2,1),# w = w - 3*cos(w3 + 2*(w4 - w1) + w5)
        (2,0,-2,0,1),# w = w + 3*cos(2*(w1 - w3) + w5)
        (2,0,0,0,1),# w = w + 3*cos(2*w1 + w5)
        (-2,-1,0,2,1),# w = w + 3*cos(2*(w4 - w1) + w5 - w2)
        (-2,0,0,0,1),# w = w + 3*cos(w5 - 2*w1)
        (0,0,2,2,1),# w = w + 3*cos(2*(w3 + w4) + w5)
        ]
    
    # assert len(sin_coef) == len(arguments_table)
    
    return sum(
        cos_coef[i]*math.cos(
            sum(
                arguments_table[i][j]*cos_args[j]
                for j in range(5)
                )   *
            math.pi/180)
        for i in range(len(cos_coef))
        )/36000000

#******************************************************************************
#******************************************************************************

def nutation_longitude(julian_centuries_since_j2000: float) -> float:
    """Returns the Earth's nutation in longitude."""
    
    D = mean_elongation_moon_from_sun(julian_centuries_since_j2000)
    
    M = mean_anomaly_sun(julian_centuries_since_j2000)
    
    M_line = mean_anomaly_moon(julian_centuries_since_j2000)
    
    F = moon_argument_latitude(julian_centuries_since_j2000)
    
    sigma = (
        longitude_ascending_node_moon_mean_orbit_ecliptic_from_mean_equinox(
            julian_centuries_since_j2000)
        )
    
    sin_args = [D, M, M_line, F, sigma]
    
    sin_coef = [
        (-174.2*julian_centuries_since_j2000 - 171996),
        (-1.6*julian_centuries_since_j2000 - 13187),
        (-2274 - 0.2*julian_centuries_since_j2000),
        (0.2*julian_centuries_since_j2000 + 2062),
        (1426 - 3.4*julian_centuries_since_j2000),
        (0.1*julian_centuries_since_j2000 + 712),
        (1.2*julian_centuries_since_j2000 - 517),
        (-0.4*julian_centuries_since_j2000 - 386),
        (217 - 0.5*julian_centuries_since_j2000),
        (129 + 0.1*julian_centuries_since_j2000),
        (0.1*julian_centuries_since_j2000 + 63),
        (-0.1*julian_centuries_since_j2000 - 58),
        (17 - 0.1*julian_centuries_since_j2000),
        (0.1*julian_centuries_since_j2000 - 16),
        -301,
        -158,
        123,
        63,
        -59,
        -51,
        48,
        46,
        -38,
        -31,
        29,
        29,
        26,
        -22,
        21,
        16,
        -15,
        -13,
        -12,
        11,
        -10,
        -8,
        7,
        -7,
        -7,
        -7,
        6,
        6,
        6,
        -6,
        -6,
        5,
        -5,
        -5,
        -5,
        4,
        4,
        4,
        -4,
        -4,
        -4,
        3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        ]
    
    arguments_table = [
        (0,0,0,0,1),
        (-2,0,0,2,2),
        (0,0,0,2,2),
        (0,0,0,0,2),
        (0,1,0,0,0),
        (0,0,1,0,0),
        (-2,1,0,2,2),
        (0,0,0,2,1),
        (-2,-1,0,2,2),
        (-2,0,0,2,1),
        (0,0,1,0,1),
        (0,0,-1,0,1),
        (0,2,0,0,0),
        (-2,2,0,2,2),
        (0,0,1,2,2),
        (-2,0,1,0,0),
        (0,0,-1,2,2),
        (2,0,0,0,0),
        (2,0,-1,2,2),
        (0,0,2,2,2),
        (-2,0,2,0,0),
        (0,0,-2,2,1),
        (2,0,0,2,2),
        (0,0,2,2,2),
        (0,0,2,0,0),
        (-2,0,1,2,2),
        (0,0,0,2,0),
        (-2,0,0,2,0),
        (0,0,-1,2,1),
        (2,0,-3,0,1),
        (0,1,0,0,1),
        (-2,0,1,0,1),
        (0,-1,0,0,1),
        (0,0,2,-2,0),
        (2,0,-1,2,1),
        (2,0,1,2,2),
        (0,1,0,2,2),
        (-2,1,1,0,0),
        (0,-1,0,2,2),
        (2,0,0,2,1),
        (2,0,1,0,0),
        (-2,0,2,2,2),
        (-2,0,1,2,1),
        (2,0,-2,0,1),
        (2,0,0,0,1),
        (0,-1,1,0,0),
        (-2,-1,0,2,1),
        (-2,0,0,0,1),
        (0,0,2,2,1),
        (-2,0,2,0,1),
        (-2,1,0,2,1),
        (0,0,1,-2,0),
        (-1,0,1,0,0),
        (-2,1,0,0,0),
        (1,0,0,0,0),
        (0,0,1,2,0),
        (0,0,-2,2,2),
        (-1,-1,1,0,0),
        (0,1,1,0,0),
        (0,-1,1,2,2),
        (2,-1,-1,2,2),
        (0,0,3,2,2),
        (2,-1,0,2,2),
        ]
    
    # assert len(sin_coef) == len(arguments_table)
    
    return sum(
        
        sin_coef[i]*math.sin(
            sum(
                arguments_table[i][j]*sin_args[j]
                for j in range(5)
                )*
            math.pi/180)
        for i in range(len(sin_coef))
        )/36000000

#******************************************************************************
#******************************************************************************

def mean_obliquity_ecliptic_IAU(julian_centuries_since_j2000: float):
    """Returns the mean obliquity of the ecliptic using an IAU-adopted function."""
        
    A = 23+26/60+21.448/3600
    
    B = 46.8150/3600
    
    C = 0.00059/3600
    
    D = 0.001813/3600
    
    return (
        A
        -
        B*julian_centuries_since_j2000
        -
        C*(julian_centuries_since_j2000)**2
        +
        D*(julian_centuries_since_j2000)**3
        )

#******************************************************************************
#******************************************************************************

def mean_obliquity_ecliptic_Laskar(julian_centuries_since_j2000: float):
    """
    Returns the mean obliquity of the ecliptic, in degrees, according to the
    formula proposed by Laskar (1986).
    """
    
    # Source: J. Laskar, Astronomy and Astrophysics, Vol. 157, page 68 (1986)
    
    U = julian_centuries_since_j2000/100
    
    if U >= 1:
        
        raise ValueError('Input time is out of range for this expression.')
        
    return (
        23+26/60+21.448/3600
        -
        (4680.93/3600)*U
        -
        1.55*U**2
        +
        1999.25*U**3
        -
        51.38*U**4
        -
        249.67*U**5
        -
        39.05*U**6
        +
        7.12*U**7
        +
        27.87*U**8
        +
        5.79*U**9
        +
        2.45*U**10
        )

#******************************************************************************
#******************************************************************************

def true_obliquity_ecliptic(julian_centuries_since_j2000: float):
    """Returns the true obliquity of the ecliptic, in degrees."""
    
    # Source:  Meeus (1998), Astronomical Algorithms, page 147
    
    return (
        mean_obliquity_ecliptic_IAU(julian_centuries_since_j2000)
        +
        nutation_obliquity(julian_centuries_since_j2000)
        )

#******************************************************************************
#******************************************************************************

def eccentricity_earths_orbit(julian_centuries_since_j2000: float):
    
    # Source:  Meeus (1998), Astronomical Algorithms, page 163
    
    return (
        0.016708634
        -
        0.000042037*julian_centuries_since_j2000
        -
        0.0000001267*(julian_centuries_since_j2000**2)
        )

#******************************************************************************
#******************************************************************************