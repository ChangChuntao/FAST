#!/usr/bin/python3
# gnssbox        : The most complete GNSS Python toolkit ever
# sat2siteAngle  : Calculate the Angle between site and satellite
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.03
# Latest Version : 2022.06.03
import numpy as np

def sat2siteAngle(satX, satY, satZ, siteX, siteY, siteZ):
    '''
    ------------------------------------------------------------------------------------
    2022.06.06  :获取站星角度 - by ChangChuntao
    input : 
            satX        :卫星X
            satY        :卫星Y
            satZ        :卫星Z
            siteX       :站点X
            siteX       :站点Y
            siteX       :站点Z
    output: 
            Zenith      :天顶角(弧度)
            Azimuth     :方位角(弧度)
            Elevation   :高度角(弧度)
    ------------------------------------------------------------------------------------
    '''
    import math
    from fast.com.xyz2neu import xyz2neu
    from fast.com.xyz2blh import xyz2blh
    from fast.com.xy2azi import xy2azi
    System = 'WGS84'
    north, east, up = xyz2neu(siteX, siteY, siteZ, satX, satY, satZ, System)
    siteB, siteL, H = xyz2blh(siteX, siteY, siteZ, System)
    satB, satL, H = xyz2blh(satX, satY, satZ, System)
    Azimuth = xy2azi(siteL, siteB, satL, satB)
    Elevation = math.atan(up / math.sqrt(north * north + east * east))
    Zenith = math.pi / 2 - Elevation
    return Zenith, Azimuth, Elevation


def getEle(rs, rr, enuRot):
    '''
    ------------------------------------------------------------------------------------
    2022.06.06  :获取高度角 - by ChangChuntao
    input : 
            satX        :卫星X
            satY        :卫星Y
            satZ        :卫星Z
            siteX       :站点X
            siteX       :站点Y
            siteX       :站点Z
    output: 
            Elevation   :高度角(弧度)
    ------------------------------------------------------------------------------------
    '''
    deltaPos = rs - rr
    east, north, up = enuRot@deltaPos
    Azimuth = np.arctan2(east,north)
    Elevation = np.arctan(up / np.sqrt(north * north + east * east))
    Zenith = np.pi / 2 - Elevation
    return Zenith, Azimuth, Elevation