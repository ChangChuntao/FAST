#!/usr/bin/python3
# gnssbox        : The most complete GNSS Python toolkit ever

# xyz2neu        : Convert ECEF coordinates to local coordinates
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.06
# Latest Version : 2022.06.06

def xyz2neu(originX, originY, originZ, X, Y, Z, System):
    '''
    ------------------------------------------------------------------------------------
    2022.06.06  :XYZ转NEU - by ChangChuntao
    input : 
            originX     :基准X
            originY     :基准Y
            originZ     :基准Z
            X           :X
            Y           :Y
            Z           :Z
            System      :坐标系统，见gnssbox.lib.gnssParameter.coordSystem
    output: 
            north       :北
            east        :东
            up          :天
    ------------------------------------------------------------------------------------
    '''
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