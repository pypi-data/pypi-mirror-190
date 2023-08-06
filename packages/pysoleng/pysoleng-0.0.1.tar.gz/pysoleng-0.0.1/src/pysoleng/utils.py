"""
Author: Pedro L. Magalhães
Email: pmlpm@posteo.de
Date: 2023
"""

#******************************************************************************
#******************************************************************************

# import libraries

import datetime as dt

import numpy as np

import math

import csv

#******************************************************************************
#******************************************************************************

# read csv file with tmy data

def read_jrc_tmy_csv(filename, assume_year: int = None):  
    """
    Reads a TMY file formatted according to the EC JRC's PVGIS (2022).
    
    This function reads a TMY CSV file formatted as those made available at the
    European Commission's JRC Photovoltaic Geographical Information System (or
    PVGIS) and returns the metadata and data in standard objects.    
    
    Parameters
    ----------
    
    filename : str
        A string identifying the file that is to be read.
        
    assume_year : int
        If this parameter is set to a non-default value, the dates will be set
        to the year indicated by this parameter ratheer than the original.
    
    Return
    ------
    
    data : numpy.ndarray
        A numpy ndarray containing the data read from the file. The data can be
        identified using the 'names' variable.
        
    names : list
        A list of strings identifying each of the fields in the array, namely:
            'timeUTC': for the datetime objects 
            'T2m': 2-m air temperature (degree Celsius)
            'RH': relative humidity (%)
            'Gh': Global irradiance on the horizontal plane (W/m2)
            'Gbn': Beam/direct irradiance on a plane always normal to sun rays (W/m2)
            'Gdh': Diffuse irradiance on the horizontal plane (W/m2)
            'IRh': Surface infrared (thermal) irradiance on a horizontal plane (W/m2)
            'WS10m': 10-m total wind speed (m/s)
            'WD10m': 10-m wind direction (0 = N, 90 = E) (degree)
            'SP': Surface (air) pressure (Pa)
                
    latitude : float
        The latitude (in radians north) of the place the file refers to.
        The latitude is between -pi/2 (south pole) and pi/2 (north pole).
        
    longitude : float
        The longitude (in radians west) of the place the file refers to.
        The longitude is between -2*pi and 2*pi and so multiple options exist.
        
    elevation : float
        The elevation (in meters) of the place the file refers to.
    
    Examples
    --------
    >>> filename = 'test_file.csv'
    >>> assume_year = 2012
    >>> data, names, lat, long, elev = read_jrc_tmy_csv(filename, assume_year)
        
    """
    
    #**************************************************************************
    
    # read the three first lines to extract the latitude, longitude and elev.
    
    with open(filename, newline='') as csvfile:
        
        reader = csv.reader(csvfile)
        
        # read the first three rows
        
        number_lines = 3
        
        rows = [reader.__next__()[0] for i in range(number_lines)]
        
        # find the location where the numbers start and convert them to floats
                
        number_prefix = ': '
        
        numbers = [
            np.float64(
                rows[i][rows[i].find(number_prefix)+len(number_prefix):])
            for i in range(number_lines)]
        
        # end
        
    # convert the latitude and the latitude
    
    latitude = numbers[0] # degrees north
    
    longitude = numbers[1] # degrees east
    
    elevation = numbers[2] # default: meters
    
    #**************************************************************************
    
    # file specifications
    
    number_header_lines = 16 # 17 but one line is for the names/labels
    
    number_footer_lines = 10 # 12 but two lines are empty
    
    file_encoding = "utf-8"
    
    date_format = '%Y%m%d:%H%M'
    
    tzinfo = dt.timezone.utc
    
    file_dtypes = (dt.datetime,
                   float,float,float,float,float,float,float,float,float)
    
    # handle the dates
    
    # differentiate date conversion depending on input parameters
    
    if assume_year != None and type(assume_year) == int:
        
        # set all entries to be for the same year, if requested
    
        date_converter = {
            0: lambda s: dt.datetime.strptime(
                s.decode(file_encoding),
                date_format).replace(year=assume_year,tzinfo=tzinfo)}
        
    else:
            
        # set the time zone only
    
        date_converter = {
            0: lambda s: dt.datetime.strptime(
                s.decode(file_encoding),
                date_format).replace(tzinfo=tzinfo)}
    
    #**************************************************************************
    
    # read the file
    
    npdata = np.genfromtxt(
        filename, 
        dtype=file_dtypes,
        names=True,
        skip_header=number_header_lines,
        skip_footer=number_footer_lines,
        delimiter=',',
        converters=date_converter)
            
    #**************************************************************************
    
    # get names
        
    names = ['timeUTC',
             'T2m',
             'RH',
             'Gh',
             'Gbn',
             'Gdh',
             'IRh',
             'WS10m',
             'WD10m',
             'SP']
    
    #**************************************************************************
    
    # return statement
    
    return ( 
        npdata, 
        names, 
        latitude, 
        longitude, 
        elevation
        )

    #**************************************************************************

# #******************************************************************************
# #******************************************************************************

# # get the standard longitude in degrees west from the local time

# def get_standard_meridian_longitude(lst_obj):
    
#     # lst_obj must have utc offset data
#     # a positive offset means east of greenwich
#     # a negative offset means west of greenwich
    
#     # every hour of difference is equivalent to 15º of longitude
#     # every second of difference is equivalent to 15ºC/3600 of longitude
#     # the total difference is time_in_seconds*15/3600
    
#     # if there is utc offset data
    
#     if lst_obj.utcoffset() != None:
        
#         # get the local standard meridian
    
#         # return math.radians(lst_obj.utcoffset().total_seconds()*15/3600)
    
#         return convertRealRadiansToPositiveRadians(
#             -math.radians(lst_obj.utcoffset().total_seconds()*15/3600)
#             )
    
#     else: # there is no time difference information
    
#         # print a warning
        
#         print('The local time object does not have timezone information.')
    
#         # return 0
    
#         return 0
    
#     #**************************************************************************
#     #**************************************************************************

# #******************************************************************************
# #******************************************************************************

# def convertRealRadiansToPositiveRadians(angle):
    
#     # angle is a real variable
#     # the output must be equivalent and between 0 and 2*pi
    
#     if angle >= 0: # positive angle
    
#         # longitude has to be between 0 and 2*pi
    
#         return math.fmod(angle,2*math.pi)
    
#     else: # negative angle
    
#         return math.fmod(angle,2*math.pi)+2*math.pi

#******************************************************************************
#******************************************************************************

def simplify_angle(angle: float,
                   angle_in_degrees: bool = True) -> float:
    
    if angle_in_degrees:
    
        return math.fmod(angle, 360)
    
    else:
        
        return math.fmod(angle, 2*math.pi)

#******************************************************************************
#******************************************************************************

def convert_angle(angle_degrees: float,
                  in_angle_positive_only: bool,
                  in_angle_positive_anticlockwise: bool,
                  out_angle_positive_only: bool,
                  out_angle_positive_anticlockwise: bool) -> float:
          
    #**************************************************************************
    
    # input format
    
    (in_format_one, 
     in_format_two, 
     in_format_three, 
     in_format_four) = _get_angle_format(in_angle_positive_only,
                                         in_angle_positive_anticlockwise)
                                          
    #**************************************************************************
    
    # check input angle conformity
    
    if angle_degrees < 0 and in_angle_positive_only:
        
        raise AngleFormatError 
        
    if abs(angle_degrees) > 180 and not in_angle_positive_only:

        raise AngleFormatError 
    
    #**************************************************************************
                                      
    # output format                                             
    
    (out_format_one, 
     out_format_two, 
     out_format_three, 
     out_format_four) = _get_angle_format(out_angle_positive_only,
                                          out_angle_positive_anticlockwise)

    #**************************************************************************
    
    # convert angle: 12 options
    
    # input format one
    
    if in_format_one and out_format_two:
        
        return 360-angle_degrees
    
    if in_format_one and out_format_three:
        
        return (
            angle_degrees 
            if angle_degrees <= 180 else angle_degrees-360)
    
    if in_format_one and out_format_four:
        
        return (
            -angle_degrees
            if angle_degrees < 180 else 360-angle_degrees)
    
    # input format two
    
    if in_format_two and out_format_one:
        
        return 360-angle_degrees
    
    if in_format_two and out_format_three:
        
        return (
            -angle_degrees
            if angle_degrees < 180 else 360-angle_degrees)
    
    if in_format_two and out_format_four:
        
        return (
            angle_degrees
            if angle_degrees <= 180 else angle_degrees-360)
    
    # input format three
    
    if in_format_three and out_format_one:
        
        return (
            angle_degrees
            if angle_degrees > 0 else 360+angle_degrees)
    
    if in_format_three and out_format_two:
        
        return (
            -angle_degrees
            if angle_degrees < 0 else 360-angle_degrees)
    
    if in_format_three and out_format_four:
        
        return -angle_degrees if angle_degrees != 180 else 180
    
    # input format four
    
    if in_format_four and out_format_one:
        
        return (
            -angle_degrees if angle_degrees < 0 else 360-angle_degrees)
    
    if in_format_four and out_format_two:
        
        return (
            angle_degrees if angle_degrees > 0 else 360+angle_degrees)
    
    if in_format_four and out_format_three:
        
        return -angle_degrees if angle_degrees != 180 else 180
    
    #**************************************************************************
    
#******************************************************************************
#******************************************************************************
    
def _get_angle_format(positive_only: bool,
                      positive_anticlockwise: bool) -> tuple:
    
    # format 1: positive only, positive anticlockwise
    # format 2: positive only, positive clockwise
    # format 3: positive or negative, positive anticlockwise
    # format 4: positive or negative, positive clockwise
    
    if positive_only:
        
        if positive_anticlockwise:
            
            format_one = True
            format_two = False
            format_three = False
            format_four = False
        
        else:
            
            format_one = False
            format_two = True
            format_three = False
            format_four = False
            
    else:
        
        if positive_anticlockwise:
            
            format_one = False
            format_two = False
            format_three = True
            format_four = False
        
        else:
            
            format_one = False
            format_two = False
            format_three = False
            format_four = True
            
    return format_one, format_two, format_three, format_four
            
#******************************************************************************
#******************************************************************************
            
class AngleFormatError(Exception):
    
    pass