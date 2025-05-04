#!/usr/bin/python3
# gnssbox        : The most complete GNSS Python toolkit ever

# xy2azi         : Calculate coordinate azimuth
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.03
# Latest Version : 2022.06.03


def xy2azi(x1, y1, x2, y2):
    '''
    ------------------------------------------------------------------------------------
    2022.06.03  :xy转方位角 - by ChangChuntao
    input : 
            x1          :站点1x
            y1          :站点1y
            x2          :站点2x
            y2          :站点2y
    output: 
            Azimuth     :方位角(弧度)
    ------------------------------------------------------------------------------------
    '''
    import math
    azimuth = 0.0
    dy = y2 - y1
    dx = x2 - x1
    if dx == 0.0 and dy > 0.0:
        azimuth = 0.0
    if dx == 0.0 and dy < 0.0:
        azimuth = 180.0
    if dy == 0.0 and dx > 0.0:
        azimuth = 90.0
    if dy == 0.0 and dx < 0.0:
        azimuth = 270.0
    if dx > 0.0 and dy > 0.0:
        azimuth = math.atan(dx / dy) * 180.0 / math.pi
    elif dx < 0.0 and dy > 0.0:
        azimuth = 360.0 + math.atan(dx / dy) * 180.0 / math.pi
    elif dx < 0.0 and dy < 0:
        azimuth = 180.0 + math.atan(dx / dy) * 180.0 / math.pi
    elif dx > 0.0 and dy < 0:
        azimuth = 180.0 + math.atan(dx / dy) * 180.0 / math.pi
    azimuth = math.radians(azimuth)
    return azimuth