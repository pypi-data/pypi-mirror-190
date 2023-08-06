"""
Author: Pedro L. Magalhães
Email: pmlpm@posteo.de
Date: 2023
"""

#******************************************************************************
#******************************************************************************

import datetime as dt

from pyproj import CRS, Transformer

# import math

#******************************************************************************
#******************************************************************************

class Location:
    """A class to specify a location on Earth."""
    
    crs = CRS.from_string('epsg:4326') 
    
    #crs = CRS.from_string('epsg:4326') 
    
    def __init__(self,
                 coordinates: tuple,
                 crs_string: str,
                 check_for_errors: bool = True
                 ):
        
        # check the number of coordinates
        
        if len(coordinates) != 2:
            
            raise ValueError('Incorrect number of coordinates.')
             
        # create internal CRS string
             
        self.crs_string = str.lower(self.crs.to_string())
        
        # verify type of CRS
        
        if (crs_string == self.crs_string or 
            crs_string == str.upper(self.crs_string)):
            
            # check the coordinates
            
            if not self.coordinates_are_within_bounds(*coordinates):
            
                raise ValueError('The coordinates are out of bounds.')
                
            # store them
            
            self.latitude, self.longitude = coordinates[0:2]
        
        else:
            
            # convert crs
            
            transformer = Transformer.from_crs(
                crs_from=crs_string, 
                crs_to=self.crs_string,
                always_xy=True)
            
            # convert coordinates
            
            self.latitude, self.longitude = transformer.transform(
                *coordinates,
                errcheck=check_for_errors)
            
    #**************************************************************************
            
    def coordinates_are_within_bounds(self, x: float, y: float):
        """
        Check if the coordinates are within the CRS\'s bounds.

        Parameters
        ----------
        x : float
            The first coordinate (e.g., the latitude with unprojected CRSs\').
        y : float
            The second coordinate (e.g., the longitude with unprojected CRSs\').

        Returns
        -------
        bool
            True if the coordinates within the bounds and False otherwise.

        """
        y_min, x_min, y_max, x_max = self.crs.area_of_use.bounds
        
        if x_min > x or x_max < x:
            
            return False
        
        if y_min > y or y_max < y:
            
            return False
        
        return True
    
    #**************************************************************************
    
    def local_standard_meridian_longitude(
            self, 
            local_time: dt.datetime, 
            dst_offset_seconds: float = 0.0) -> float:
        """
        Returns the longitude for the local standard meridian via local time.
        
        This longitude is determined via the time difference between the local
        time and UTC. The datetime object containing the time must be aware.

        Parameters
        ----------
        local_time : dt.datetime
            The datetime object containing the local time. It must be aware.
        dst_offset_seconds : float, optional
            The daylight savings time offset in seconds. The default is 0.0.
            This offset is only meant to provide a way to bypass the behaviour
            of datetime objects that do not have detailed daylight savings time
            information (e.g., objects merely with the correct UTC offset). Lo-
            cal times defined from an ISO string will tend to be incorrect for
            Summer months unless such an offset is used, since that is when an
            offset is added to the normal (i.e., Winter) UTC offset.

        Raises
        ------
        ValueError
            This exception is raised if the datetime object is not aware.

        Returns
        -------
        float
            The longitude for the local standard meridian in degrees.

        """
        
        # the object must be aware (e.g., to include the utcoffset method)
        
        if not is_datetime_aware(local_time):
            
            raise ValueError('The input datetime object is not aware.')

        # local_time must have utc offset data
        # a positive offset means east of greenwich
        # a negative offset means west of greenwich
        
        # every hour of difference is equivalent to 15º of longitude
        # every second of difference is equivalent to 15ºC/3600 of longitude
        # the total difference is time_in_seconds*15/3600
        
        return (
            (local_time.utcoffset().total_seconds()-dst_offset_seconds)*15/3600
            )

    #**************************************************************************
    #**************************************************************************

#******************************************************************************
#******************************************************************************

def day_of_the_year(my_time: dt.datetime,
                    as_integer: bool = True) -> int or float:
    """
    Returns the day of the year for a given datetime object.
    
    Since the actual day of the year differs, depending on the location, it is
    assumed that the day is determined according to UTC time.

    Parameters
    ----------
    my_time : dt.datetime
        The datetime object that defines the date/time under consideration.
    as_integer : bool, optional
        If True, returns the day of the year as an integer. If False, returns
        a float which also takes hours, minutes and seconds into account.
        The default is True.

    Returns
    -------
    int or float
        The day of the year corresponding to the date/time specified.

    """
    
    if as_integer:
    
        return my_time.utctimetuple().tm_yday
    
    else:
        
        return (
            my_time.utctimetuple().tm_yday+
            my_time.utctimetuple().tm_hour/24+
            my_time.utctimetuple().tm_min/(1440)+
            my_time.utctimetuple().tm_sec/(86400)
            )

#******************************************************************************
#******************************************************************************

def is_datetime_aware(my_time: dt.datetime) -> bool:
    """
    Verifies whether a datetime object is aware or not (naive).
    
    An aware object represents a specific moment in time that is not open to 
    interpretation. In turn, a naive object does not contain enough information
    to unambiguously locate itself relative to other date/time objects. 
    
    Thus, a datetime object d is aware if both of the following hold:
    1) d.tzinfo is not None
    2) d.tzinfo.utcoffset(d) does not return None
    Otherwise, d is naive.
    
    Source: https://docs.python.org/3/library/datetime.html

    Parameters
    ----------
    my_time : dt.datetime
        The datetime object under consideration.

    Returns
    -------
    bool
        A variable indicating the object is aware (True) or naive (False).

    """
    
    # A datetime object d is aware if both of the following hold:
    # d.tzinfo is not None
    # d.tzinfo.utcoffset(d) does not return None
    # Otherwise, d is naive.
    
    if my_time.tzinfo is not None:
        
        if my_time.tzinfo.utcoffset(my_time) != None:
            
            return True
        
    return False
    
#******************************************************************************
#******************************************************************************

class Plane:
    """A class for planes defined using azimuths and slopes."""
    
    def __init__(self,
                 azimuth_zero_south_positive_west: float,
                 slope_zero_horizontal_positive_south: float):
        
        self.azimuth = azimuth_zero_south_positive_west
        
        self.slope = slope_zero_horizontal_positive_south
    
#******************************************************************************
#******************************************************************************