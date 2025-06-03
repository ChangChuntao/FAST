# -*- coding: utf-8 -*-
# nav2posclk     : get GNSS pos/clk in NAV file
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University 
# Latest Version : 3.00.03
# Creation Date  : 2023.10.06 - Version 3.00.00
# Date           : 2025.06.03 - Version 3.00.03

from numpy import sin, cos, sqrt, arctan2
import datetime
from fast.com.gnssParameter import CLIGHT


def getGME(gnssSys):
    """
    2023.10.06 :    Returns the Earth's gravitational constant (GME) for a specified GNSS system.
                    by ChangChuntao
    
    The gravitational constant is a fundamental parameter used in GNSS calculations,
    representing the product of the gravitational constant and the Earth's mass.

    Parameters:
        gnssSys (str): A single character representing the GNSS system:
                       'G' for GPS, 'E' for Galileo, 'C' for BDS, 'J' for QZSS, 'R' for GLONASS.

    Returns:
        float: The Earth's gravitational constant (GME) in m^3/s^2 for the specified GNSS system.
    """
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

def getEarthRot(gnssSys):
    """
    2023.10.06 :    Returns the Earth's rotation rate for a specified GNSS system.
                    by ChangChuntao
    
    The Earth's rotation rate is a fundamental parameter used in GNSS calculations,
    representing the angular velocity of the Earth's rotation. 

    Parameters:
        gnssSys (str): A single character representing the GNSS system

    Returns:
        float: The Earth's rotation rate in radians per second (rad/s) for the specified GNSS system.

    Note:
        The default value is used for GNSS systems not explicitly listed ('G' or 'E' are most commonly used).
    """
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
    """
    2023.10.06 :    Converts satellite navigation parameters to ECEF position and velocity (GPS/GAL system).
                    by ChangChuntao
    This function takes the satellite's orbital parameters and computes its position and velocity
    in the Earth-Centered Earth-Fixed (ECEF) coordinate system using Keplerian mechanics and
    perturbation corrections.

    Args:
        roota (float): Square root of the semi-major axis (m^0.5).
        GME (float): Earth's gravitational constant (m^3/s^2).
        DeltaN (float): Mean motion difference from computed value (rad/s).
        tk (float): Time from ephemeris reference epoch (s).
        M0 (float): Mean anomaly at reference epoch (rad).
        e (float): Eccentricity.
        omega (float): Argument of perigee (rad).
        cuc (float): Amplitude of the cosine harmonic correction term to the argument of latitude (rad).
        cus (float): Amplitude of the sine harmonic correction term to the argument of latitude (rad).
        crc (float): Amplitude of the cosine harmonic correction term to the radius (m).
        crs (float): Amplitude of the sine harmonic correction term to the radius (m).
        cic (float): Amplitude of the cosine harmonic correction term to the inclination (rad).
        cis (float): Amplitude of the sine harmonic correction term to the inclination (rad).
        i0 (float): Inclination at reference epoch (rad).
        IDOT (float): Rate of right ascension (rad/s).
        OMEGA_DOT (float): Rate of change of the right ascension of the ascending node (rad/s).
        E_ROTATE (float): Earth's rotation rate (rad/s).
        toe (float): Time of ephemeris (s).
        OMEGA0 (float): Longitude of ascending node at reference epoch (rad).

    Returns:
        tuple: (x, y, z, vx, vy, vz) - ECEF position (m) and velocity (m/s) of the satellite.

    Note:
        This function assumes the input parameters are valid and within the expected range.
        The function uses an iterative approach to solve Kepler's equation.
    """
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
    """
    2023.10.06 :    Converts satellite navigation parameters to ECEF position and velocity (BDS system).
                    by ChangChuntao
    
    This function takes the satellite's orbital parameters and computes its position and velocity
    in the Earth-Centered Earth-Fixed (ECEF) coordinate system using Keplerian mechanics and
    perturbation corrections. The main logic is similar to `numbaNav2posG`, but may have slight
    differences in implementation for BDS-specific parameters.

    Args:
        roota (float): Square root of the semi-major axis (m^0.5).
        GME (float): Earth's gravitational constant (m^3/s^2).
        DeltaN (float): Mean motion difference from computed value (rad/s).
        tk (float): Time from ephemeris reference epoch (s).
        M0 (float): Mean anomaly at reference epoch (rad).
        e (float): Eccentricity.
        omega (float): Argument of perigee (rad).
        cuc (float): Amplitude of the cosine harmonic correction term to the argument of latitude (rad).
        cus (float): Amplitude of the sine harmonic correction term to the argument of latitude (rad).
        crc (float): Amplitude of the cosine harmonic correction term to the radius (m).
        crs (float): Amplitude of the sine harmonic correction term to the radius (m).
        cic (float): Amplitude of the cosine harmonic correction term to the inclination (rad).
        cis (float): Amplitude of the sine harmonic correction term to the inclination (rad).
        i0 (float): Inclination at reference epoch (rad).
        IDOT (float): Rate of right ascension (rad/s).
        OMEGA_DOT (float): Rate of change of the right ascension of the ascending node (rad/s).
        E_ROTATE (float): Earth's rotation rate (rad/s).
        toe (float): Time of ephemeris (s).
        OMEGA0 (float): Longitude of ascending node at reference epoch (rad).

    Returns:
        tuple: (x, y, z, vx, vy, vz) - ECEF position (m) and velocity (m/s) of the satellite.

    Note:
        This function assumes the input parameters are valid and within the expected range.
        The function uses an iterative approach to solve Kepler's equation.
    """
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
    """
    2024.09.30 :    Converts satellite navigation parameters to ECEF position and velocity.
                    by Chang Chuntao

    This function takes the satellite's orbital parameters and computes its position and velocity
    in the Earth-Centered Earth-Fixed (ECEF) coordinate system using Keplerian mechanics and
    perturbation corrections. It supports multiple GNSS systems (GPS, Galileo, BDS, QZSS) and
    handles system-specific parameters accordingly.

    Args:
        navData (dict): Dictionary containing navigation data for satellites.
        prn (str): Satellite identifier (e.g., 'G01' for GPS, 'C01' for BDS).
        epochFind (datetime): Time epoch to search for in navigation data.
        nowDatetime (datetime): Current time for which position and velocity are computed.

    Returns:
        tuple: (x, y, z, vx, vy, vz) - ECEF position (m) and velocity (m/s) of the satellite.
            Returns (None, None, None, None, None, None) if data is not available or invalid.

    Note:
        This function assumes the input navigation data is valid and within the expected range.
        The function uses an iterative approach to solve Kepler's equation and applies
        corrections specific to each GNSS system.
    """
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
        E_ROTATE = getEarthRot(prn[0])
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
        E_ROTATE = getEarthRot(prn[0])
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
    """
    2023.10.06 :    Performs a binary search to find the closest epoch in navigation data.
                    by Chang Chuntao

    This function takes a dictionary of navigation data, a satellite identifier (PRN), and a target datetime.
    It returns the list of epochs and the index of the closest epoch to the target datetime.
    If the exact epoch is found, it returns the index directly; otherwise, it returns the index of the closest epoch.

    Args:
        navData (dict): Dictionary containing navigation data for satellites, keyed by PRN and epoch.
        prn (str): Satellite identifier (e.g., 'G01' for GPS, 'C01' for BDS).
        nowDatetime (datetime): Target datetime to search for in the navigation data.

    Returns:
        tuple: (epochs, index) - A list of epochs and the index of the closest epoch to the target datetime.
            If the exact epoch is found, the index points to that epoch; otherwise, it points to the closest one.

    Note:
        This function assumes the input navigation data is sorted by epoch.
    """
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
    """
    2023.09.30 :    Computes the satellite clock correction using navigation data.
                    by Chang Chuntao

    This function calculates the satellite clock correction based on the provided navigation parameters.
    It includes relativistic corrections to account for the satellite's orbital motion.

    Args:
        a0 (float): Clock bias coefficient.
        a1 (float): Clock drift coefficient.
        a2 (float): Clock drift rate coefficient.
        tk (float): Time from ephemeris reference epoch (s).
        GME (float): Earth's gravitational constant (m^3/s^2).
        roota (float): Square root of the semi-major axis (m^0.5).
        DeltaN (float): Mean motion difference from computed value (rad/s).
        M0 (float): Mean anomaly at reference epoch (rad).
        e (float): Eccentricity.

    Returns:
        float: Satellite clock correction (s).

    """
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
    """
    2023.09.30 :    Retrieves the satellite clock correction from navigation data.
                    by Chang Chuntao

    This function finds the closest epoch in the navigation data and computes the satellite clock correction
    using the `numbaNav2clk` function.

    Args:
        navData (dict): Dictionary containing navigation data for satellites.
        prn (str): Satellite identifier (e.g., 'G01' for GPS, 'C01' for BDS).
        nowDatetime (datetime): Current time for which the clock correction is computed.

    Returns:
        float or None: Satellite clock correction (s) or None if data is not available.

    Note:
        This function assumes the input navigation data is valid and sorted by epoch.
        If the satellite identifier is not found in the navigation data, the function returns None.
    """
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
    """
    2023.09.30 :    Retrieves the satellite group delay correction from navigation data.
                    by Chang Chuntao

    This function finds the closest epoch in the navigation data and computes the group delay correction
    for BDS satellites using the provided frequencies.

    Args:
        navData (dict): Dictionary containing navigation data for satellites.
        f1 (float): Frequency 1 (Hz).
        f2 (float): Frequency 2 (Hz).
        prn (str): Satellite identifier (e.g., 'C01' for BDS).
        nowDatetime (datetime): Current time for which the group delay correction is computed.

    Returns:
        float or None: Group delay correction (s) or None if data is not available.

    Note:
        This function assumes the input navigation data is valid and sorted by epoch.
        The function only applies to BDS satellites (identified by 'C' in the PRN).
    """
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
