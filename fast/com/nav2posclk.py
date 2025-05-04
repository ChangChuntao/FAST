
from numpy import sin, cos, sqrt, arctan2
import datetime

from fast.com.gnssParameter import CLIGHT


def getGME(gnssSys):
    if gnssSys == 'G':
        GMEARTH = 3.986005E14
    elif gnssSys == 'E':
        GMEARTH = 3.986004418E14
    elif gnssSys == 'C':
        GMEARTH = 3.986004418E14
    elif gnssSys == 'J':
        GMEARTH = 3.986005E14
    elif gnssSys == 'R':
        GMEARTH = 3.9860044E14
    else:
        GMEARTH = 3.986004415E14
    return GMEARTH

def getEARTH_ROTATE(gnssSys):
    if gnssSys == 'G':
        EARTH_ROTATE = 7.2921151467E-5
    elif gnssSys == 'E':
        EARTH_ROTATE = 7.2921151467E-5
    elif gnssSys == 'C':
        EARTH_ROTATE = 7.2921150E-5
    elif gnssSys == 'J':
        EARTH_ROTATE = 7.2921150E-5
    elif gnssSys == 'R':
        EARTH_ROTATE = 7.292115E-5
    else:
        EARTH_ROTATE = 7.2921151467E-5
    return EARTH_ROTATE
    

def numbaNav2posG(roota, GME, DeltaN, tk, M0, e, omega, cuc, cus, crc, crs, cic, cis, i0, IDOT, OMEGA_DOT, E_ROTATE, toe, OMEGA0):
    ak = roota * roota
    n0 = sqrt(GME / (ak ** 3))
    nk = n0 + DeltaN
    mk = M0 + nk * tk
    ek = mk
    for _ in range(12):
        ek_new = mk + e * sin(ek)
        if abs(ek - ek_new) < 1e-10:  # 收敛条件
            ek = ek_new
            break
        ek = ek_new
    fk = arctan2(sqrt(1-e**2)*sin(ek),cos(ek)-e)
    # 纬度幅角
    phik = fk + omega
    # 摄动改正项 for 纬度幅角uk 矢径rk 轨道倾角ik
    sin_2_phi = sin(2.0 * phik)
    cos_2_phi = cos(2.0 * phik)
    du = cuc * cos_2_phi + cus * sin_2_phi
    dr = crc * cos_2_phi + crs * sin_2_phi
    di = cic * cos_2_phi + cis * sin_2_phi
    # 改正后的纬度幅角uk 矢径rk 轨道倾角ik
    uk = phik + du
    rk = ak * (1.e0 - e * cos(ek)) + dr # + epochDict['rdot'] * tk
    ik = i0 + di + IDOT * tk
    # 轨道平面坐标系
    xk = rk * cos(uk)
    yk = rk * sin(uk)
    omegaDot = OMEGA_DOT - E_ROTATE
    omegak = OMEGA0 + omegaDot * tk -  E_ROTATE * toe
    #### 地固系
    # 坐标
    x = xk * cos(omegak) - yk * cos(ik) * sin(omegak)
    y = xk * sin(omegak) + yk * cos(ik) * cos(omegak)
    z = yk * sin(ik)

    tkb = tk - 0.001
    mkb = M0 + nk * tkb
    ekb = mkb
    for _ in range(12):
        ekb_new = mkb + e * sin(ekb)
        if abs(ekb - ekb_new) < 1e-10:  # 收敛条件
            ekb_new = ekb_new
            break
        ekb = ekb_new
    fkb = arctan2(sqrt(1-e**2)*sin(ekb),cos(ekb)-e)
    phikb = fkb + omega
    sin_2_phib = sin(2.0 * phikb)
    cos_2_phib = cos(2.0 * phikb)
    dub = cuc * cos_2_phib + cus * sin_2_phib
    drb = crc * cos_2_phib + crs * sin_2_phib
    dib = cic * cos_2_phib + cis * sin_2_phib
    ukb = phikb + dub
    rkb = ak * (1.e0 - e * cos(ekb)) + drb # + epochDict['rdot'] * tk
    ikb = i0 + dib + IDOT * tkb
    xkb = rkb * cos(ukb)
    ykb = rkb * sin(ukb)
    omegakb = OMEGA0 + omegaDot * tkb -  E_ROTATE * toe
    xb = xkb * cos(omegakb) - ykb * cos(ikb) * sin(omegakb)
    yb = xkb * sin(omegakb) + ykb * cos(ikb) * cos(omegakb)
    zb = ykb * sin(ikb)
    vx = (x - xb) / 0.001
    vy = (y - yb) / 0.001
    vz = (z - zb) / 0.001
    return x, y, z, vx, vy, vz


def numbaNav2posC(roota, GME, DeltaN, tk, M0, e, omega, cuc, cus, crc, crs, cic, cis, i0, IDOT, OMEGA_DOT, E_ROTATE, toe, OMEGA0):
    
    ak = roota * roota
    n0 = sqrt(GME / (ak ** 3))
    nk = n0 + DeltaN
    mk = M0 + nk * tk
    ek = mk
    for _ in range(12):
        ek_new = mk + e * sin(ek)
        if abs(ek - ek_new) < 1e-10:  # 收敛条件
            ek = ek_new
            break
        ek = ek_new
    fk = arctan2(sqrt(1-e**2)*sin(ek),cos(ek)-e)
    # 纬度幅角
    phik = fk + omega
    # 摄动改正项 for 纬度幅角uk 矢径rk 轨道倾角ik
    sin_2_phi = sin(2.0 * phik)
    cos_2_phi = cos(2.0 * phik)
    du = cuc * cos_2_phi + cus * sin_2_phi
    dr = crc * cos_2_phi + crs * sin_2_phi
    di = cic * cos_2_phi + cis * sin_2_phi
    # 改正后的纬度幅角uk 矢径rk 轨道倾角ik
    uk = phik + du
    rk = ak * (1.e0 - e * cos(ek)) + dr # + epochDict['rdot'] * tk
    ik = i0 + IDOT * tk + di 
    # 轨道平面坐标系
    xk = rk * cos(uk)
    yk = rk * sin(uk)
    omegaDot = OMEGA_DOT - E_ROTATE
    omegak = OMEGA0 + omegaDot * tk -  E_ROTATE * toe
    #### 地固系
    # 坐标
    x = xk * cos(omegak) - yk * cos(ik) * sin(omegak)
    y = xk * sin(omegak) + yk * cos(ik) * cos(omegak)
    z = yk * sin(ik)

    tkb = tk - 0.001
    mkb = M0 + nk * tkb
    ekb = mkb
    for _ in range(12):
        ekb_new = mkb + e * sin(ekb)
        if abs(ekb - ekb_new) < 1e-10:  # 收敛条件
            ekb_new = ekb_new
            break
        ekb = ekb_new
    fkb = arctan2(sqrt(1-e**2)*sin(ekb),cos(ekb)-e)
    phikb = fkb + omega
    sin_2_phib = sin(2.0 * phikb)
    cos_2_phib = cos(2.0 * phikb)
    dub = cuc * cos_2_phib + cus * sin_2_phib
    drb = crc * cos_2_phib + crs * sin_2_phib
    dib = cic * cos_2_phib + cis * sin_2_phib
    ukb = phikb + dub
    rkb = ak * (1.e0 - e * cos(ekb)) + drb # + epochDict['rdot'] * tk
    ikb = i0 + dib + IDOT * tkb
    xkb = rkb * cos(ukb)
    ykb = rkb * sin(ukb)
    omegakb = OMEGA0 + omegaDot * tkb -  E_ROTATE * toe
    xb = xkb * cos(omegakb) - ykb * cos(ikb) * sin(omegakb)
    yb = xkb * sin(omegakb) + ykb * cos(ikb) * cos(omegakb)
    zb = ykb * sin(ikb)
    vx = (x - xb) / 0.001
    vy = (y - yb) / 0.001
    vz = (z - zb) / 0.001
    return x, y, z, vx, vy, vz



def getPosInNav(navData, prn, epochFind, nowDatetime):
    x = None
    y = None
    z = None
    vx = None
    vy = None
    vz = None
    if prn not in navData:
        return None, None, None, None, None, None
    if prn[0] == 'C':
        nowDatetime -= datetime.timedelta(seconds=14)
        epochFind -= datetime.timedelta(seconds=14)
    
    epochList,epoch_index = binary_search(navData, prn, epochFind)
    if epoch_index == -1:
        return None, None, None, None, None, None
    
    epoch = epochList[epoch_index]

    epochDict = navData[prn][epoch]
    if epochDict['SVhealth'] != 0:
        return None, None, None, None, None, None
    
    if prn[0] == 'G' or prn[0] == 'E' or prn[0] == 'J' or prn[0] == 'I':
        GME = getGME(prn[0])
        E_ROTATE = getEARTH_ROTATE(prn[0])
        tk = (nowDatetime - epoch).total_seconds()
        roota = epochDict['roota']
        DeltaN = epochDict['DeltaN']
        M0 = epochDict['M0']
        omega = epochDict['omega']
        e = epochDict['e']
        cuc = epochDict['cuc']
        cus = epochDict['cus']
        crs = epochDict['crs']
        crc = epochDict['crc']
        cic = epochDict['cic']
        cis = epochDict['cis']
        IDOT = epochDict['IDOT']
        i0 = epochDict['i0']
        OMEGA_DOT = epochDict['OMEGA_DOT']
        OMEGA0 = epochDict['OMEGA0']
        toe = epochDict['toe']
        x, y, z, vx, vy, vz = numbaNav2posG(roota, GME, DeltaN, tk, M0, e, omega, cuc, cus, crc, crs, cic, cis, i0, IDOT, OMEGA_DOT, E_ROTATE, toe, OMEGA0)

        
    elif prn[0] == 'C':
        GME = getGME(prn[0])
        E_ROTATE = getEARTH_ROTATE(prn[0])
        tk = (nowDatetime - epoch).total_seconds()
        roota = epochDict['roota']
        DeltaN = epochDict['DeltaN']
        M0 = epochDict['M0']
        omega = epochDict['omega']
        e = epochDict['e']
        cuc = epochDict['cuc']
        cus = epochDict['cus']
        crs = epochDict['crs']
        crc = epochDict['crc']
        cic = epochDict['cic']
        cis = epochDict['cis']
        IDOT = epochDict['IDOT']
        i0 = epochDict['i0']
        OMEGA_DOT = epochDict['OMEGA_DOT']
        OMEGA0 = epochDict['OMEGA0']
        toe = epochDict['toe']
        x, y, z, vx, vy, vz = numbaNav2posC(roota, GME, DeltaN, tk, M0, e, omega, cuc, cus, crc, crs, cic, cis, i0, IDOT, OMEGA_DOT, E_ROTATE, toe, OMEGA0)


    return x, y, z, vx, vy, vz

def binary_search(navData, prn, nowDatetime):
    epochs = list(navData[prn].keys())
    low, high = 0, len(epochs) - 1

    while low <= high:
        mid = (low + high) // 2
        if epochs[mid] < nowDatetime:
            low = mid + 1
        elif epochs[mid] > nowDatetime:
            high = mid - 1
        else:
            return epochs, mid
    return epochs, high


def numbaNav2clk(a0, a1, a2, tk, GME, roota, DeltaN, M0, e):

    clk = a0 + a1 * tk + a2 * tk * tk
    ak = roota * roota
    n0 = sqrt(GME / (ak ** 3))
    nk = n0 + DeltaN
    mk = M0 + nk * tk
    ek = mk
    for _ in range(12):
        ek_new = mk + e * sin(ek)
        if abs(ek - ek_new) < 1e-10:  # 收敛条件
            ek = ek_new
            break
        ek = ek_new
    dtrel = -2.0*sqrt(GME*ak)*e*sin(ek)/CLIGHT**2
    clk += dtrel
    return clk


def getClkInNav(navData, prn, nowDatetime):
    clk = None
    if prn not in navData:
        return clk
    
    epochList, epoch_index = binary_search(navData, prn, nowDatetime)
    if epoch_index == -1:
        return clk
    
    epoch = epochList[epoch_index]
    tk = (nowDatetime - epoch).total_seconds()

    a0 = navData[prn][epoch]['SVclockBias']
    a1 = navData[prn][epoch]['SVclockDrift']
    a2 = navData[prn][epoch]['SVclockDriftRate']
    DeltaN = navData[prn][epoch]['DeltaN']
    roota = navData[prn][epoch]['roota']
    M0 = navData[prn][epoch]['M0']
    DeltaN = navData[prn][epoch]['DeltaN']
    e = navData[prn][epoch]['e']
    GME = getGME(prn[0])
    clk = numbaNav2clk(a0, a1, a2, tk, GME, roota, DeltaN, M0, e)
    return clk



def getTgdInNav(navData, f1, f2, prn, nowDatetime):
    if prn[0] not in 'C':
        return 0
    tgd = 0
    epochList, epoch_index = binary_search(navData, prn, nowDatetime)
    if epoch_index == -1:
        return None
    
    epoch = epochList[epoch_index]
    if prn[0] == 'C':
        tgd4b1 = navData[prn][epoch]['TGD1']
        tgd = (f1 ** 2) / (f1 ** 2 - f2 ** 2) * tgd4b1 * CLIGHT
    return tgd


# def relativisticByBrd(navData, prn, nowDatetime):
#     for epoch in navData[prn]:
#         if epoch <= nowDatetime:
#             break
#     GME = getGME(prn[0])
#     tk = (nowDatetime - epoch).total_seconds()
#     a0 = navData[prn][epoch]['roota'] * navData[prn][epoch]['roota']
#     ak = a0
#     n0 = sqrt(GME / (a0 ** 3))
#     nk = n0 + navData[prn][epoch]['DeltaN']
#     mk = navData[prn][epoch]['M0'] + nk * tk
#     e = navData[prn][epoch]['e']
#     ek = mk
#     for _ in range(12):
#         ek = mk + e * sin(ek)
#     corr = 2/CLIGHT * sqrt(GME * ak) * e * sin(ek)
#     return corr

