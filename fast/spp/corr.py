# -*- coding: utf-8 -*-
# corr              : error correction for SPP
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02


def earthRotation(satX_init, satY_init, satZ_init, SignalDeltaTimeInit):
    from fast.com.gnssParameter import coordSystem
    omega = coordSystem['WGS84'].omega
    import numpy as np
    satX =  np.cos(omega * SignalDeltaTimeInit) * satX_init + np.sin(omega * SignalDeltaTimeInit) * satY_init
    satY = -np.sin(omega * SignalDeltaTimeInit) * satX_init + np.cos(omega * SignalDeltaTimeInit) * satY_init
    satZ =  satZ_init
    return satX, satY, satZ


def relativistic(x, y, z, vx, vy, vz):
    from fast.com.gnssParameter import CLIGHT
    """ Calculate relativistic clock correction
    Input: Coordinates [m] (x,y,z) and Velocities (vx,vy,vz) [m/s]
           of satellites in ECEF frame
    Output: Relativistic clock correction in seconds unit
    """
    return 2*(x*vx + y*vy + z*vz)/CLIGHT

def orb2ecef(satPos, sunPosECEF):
    import numpy as np
    """
    Rotation matrix from satellite antenna frame to ECEF frame assuming
    standard yaw attitude law
    """
    rs = np.array(satPos)
    rsun = np.array(sunPosECEF)
    r = -np.array(satPos)
    ez = r/np.linalg.norm(r)
    r = rsun-rs
    es = r/np.linalg.norm(r)
    r = np.cross(ez, es)
    ey = r/np.linalg.norm(r)
    ex = np.cross(ey, ez)
    return ex, ey, ez

def satPCO(prn, atxData, satPos, sunPosECEF, band1, band2, lamda1, lamda2):
    # from gnssbox.com.coordTran.eph import orb2ecef
    import numpy as np
    ex, ey, ez = orb2ecef(satPos, sunPosECEF)
    north1, east1, up1 = atxData['sat'][prn][band1[1]]['north'], atxData['sat'][prn][band1[1]]['east'], atxData['sat'][prn][band1[1]]['up']
    north2, east2, up2 = atxData['sat'][prn][band2[1]]['north'], atxData['sat'][prn][band2[1]]['east'], atxData['sat'][prn][band2[1]]['up']

    gamma = lamda2 ** 2 / lamda1 ** 2
    C1 = gamma / (gamma - 1.0)
    C2 = -1.0 / (gamma - 1.0)

    dant = np.zeros(3)
    
    for i in range(3):
        dant1 = np.dot(north1, ex[i]) + np.dot(east1, ey[i]) + np.dot(up1, ez[i])
        dant2 = np.dot(north2, ex[i]) + np.dot(east2, ey[i]) + np.dot(up2, ez[i])
        dant[i] = C1 * dant1 + C2 * dant2

    return satPos[0] + dant[0], satPos[1] + dant[1], satPos[2] + dant[2]
    

def remove_zero_columns(matrix):
    import numpy as np
    matrix = np.asarray(matrix)  # 转换为普通的 NumPy 数组
    non_zero_columns = np.any(matrix, axis=0)
    removed_columns = np.where(~non_zero_columns)[0]  # 获取被删除的零列的索引
    return matrix[:, non_zero_columns], removed_columns

def insert_zeros(arr, positions):
    import numpy as np
    # 对位置列表进行逆序,这样才能从后往前插入,避免影响前面的索引位置
    # positions = sorted(positions, reverse=True)
    zeros = np.zeros((len(positions), 1))  # 创建与位置数量相匹配的全为0的数组
    
    for pos, val in zip(positions, zeros):
        # 在指定位置插入值
        arr = np.insert(arr, pos, val, axis=0)
    
    return arr