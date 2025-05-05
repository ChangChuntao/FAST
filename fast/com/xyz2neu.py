# -*- coding: utf-8 -*-
# xyz2neu        : Convert ECEF coordinates to local coordinates
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.06
# Latest Version : 2022.06.06

def xyz2neu(originX, originY, originZ, X, Y, Z, System):
    """
    2022.06.06 :    Converts differences in ECEF coordinates to North-East-Up (NEU) components.
                    by Chang Chuntao
    
    This function takes the origin point's ECEF coordinates (X, Y, Z) and the target point's ECEF coordinates,
    then computes the differences in the North, East, and Up directions relative to the origin point.
    It uses the latitude and longitude of the origin point, which are computed using the xyz2blh function.
    
    Args:
    originX (float): X-coordinate of the origin point in ECEF (m).
    originY (float): Y-coordinate of the origin point in ECEF (m).
    originZ (float): Z-coordinate of the origin point in ECEF (m).
    X (float): X-coordinate of the target point in ECEF (m).
    Y (float): Y-coordinate of the target point in ECEF (m).
    Z (float): Z-coordinate of the target point in ECEF (m).
    System (str): Coordinate system identifier (not used in this function).
    
    Returns:
    tuple: (north, east, up) - Differences in the North, East, and Up directions (m).
    
    Note:
    This function assumes the input coordinates are valid ECEF coordinates.
    The function uses the xyz2blh function to convert ECEF coordinates to geodetic coordinates (latitude, longitude).
    """
    import math
    from fast.com.xyz2blh import xyz2blh
    deltaX = X - originX
    deltaY = Y - originY
    deltaZ = Z - originZ
    [lat, lon, h] = xyz2blh(originX, originY, originZ)
    north = (-math.sin(lat) * math.cos(lon) * deltaX -
             math.sin(lat) * math.sin(lon) * deltaY +
             math.cos(lat) * deltaZ)
    east = -math.sin(lon) * deltaX + math.cos(lon) * deltaY
    up = (math.cos(lat) * math.cos(lon) * deltaX +
          math.cos(lat) * math.sin(lon) * deltaY +
          math.sin(lat) * deltaZ)
    return north, east, up