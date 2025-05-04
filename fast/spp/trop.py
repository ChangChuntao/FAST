#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np

def tropColins(elevation, lat,lon,height, doy):

    """
    Calculates tropospheric delay using Colins(1999) method
    Input:
        Cartesian coordinates of receiver in ECEF frame (x,y,z)
        Elevation Angle [unit: radians] of satellite vehicle
    Output:
        Tropospheric delay [unit: m]
    
    Reference: 
    Collins, J. P. (1999). Assessment and Development of a Tropospheric Delay Model for
    Aircraft Users of the Global Positioning System. M.Sc.E. thesis, Department of
    Geodesy and Geomatics Engineering Technical Report No. 203, University of
    New Brunswick, Fredericton, New Brunswick, Canada, 174 pp
    """

    # Constants
    k1 = 77.604  # K/mbar
    k2 = 382000  # K^2/mbar
    Rd = 287.054  # J/Kg/K
    g = 9.80665  # m/s^2
    gm = 9.784  # m/s^2

    # Meteorological parameters
    ave_params = np.array([
        [1013.25, 299.65, 26.31, 6.30e-3, 2.77],
        [1017.25, 294.15, 21.79, 6.05e-3, 3.15],
        [1015.75, 283.15, 11.66, 5.58e-3, 2.57],
        [1011.75, 272.15, 6.78, 5.39e-3, 1.81],
        [1013.00, 263.65, 4.11, 4.53e-3, 1.55]
    ])

    sea_params = np.array([
        [0.00, 0.00, 0.00, 0.00e-3, 0.00],
        [-3.75, 7.00, 8.85, 0.25e-3, 0.33],
        [-2.25, 11.00, 7.24, 0.32e-3, 0.46],
        [-1.75, 15.00, 5.36, 0.81e-3, 0.74],
        [-0.50, 14.50, 3.39, 0.62e-3, 0.30]
    ])

    Latitude = np.array([15, 30, 45, 60, 75])
    indexLat = np.searchsorted(Latitude, abs(lat), side='right') - 1

    if indexLat == 0:
        ave_meteo = ave_params[0, :]
        svar_meteo = sea_params[0, :]
    elif indexLat == 4:
        ave_meteo = ave_params[4, :]
        svar_meteo = sea_params[4, :]
    else:
        ratio = (abs(lat) - Latitude[indexLat]) / (Latitude[indexLat + 1] - Latitude[indexLat])
        ave_meteo = ave_params[indexLat, :] + (ave_params[indexLat + 1, :] - ave_params[indexLat, :]) * ratio
        svar_meteo = sea_params[indexLat, :] + (sea_params[indexLat + 1, :] - sea_params[indexLat, :]) * ratio

    doy_min = 28 if lat >= 0.0 else 211
    param_meteo = ave_meteo - svar_meteo * np.cos((2 * np.pi * (doy - doy_min)) / 365.25)
    pressure, temperature, e, beta, lamda = param_meteo

    ave_dry = 1e-6 * k1 * Rd * pressure / gm
    ave_wet = 1e-6 * k2 * Rd / (gm * (lamda + 1) - beta * Rd) * e / temperature

    beta_times_ortHeight_over_temp = beta * height / temperature
    factor = 1 - beta_times_ortHeight_over_temp
    power_dry = g / Rd / beta
    power_wet = ((lamda + 1) * g / Rd / beta) - 1

    d_dry = ave_dry * np.power(factor, power_dry)
    d_wet = ave_wet * np.power(factor, power_wet)

    sin_elev_squared = np.sin(elevation) ** 2
    m_elev = 1.001 / np.sqrt(0.002001 + sin_elev_squared)
    # dryM, wetM = tropmapfNiell(doy, lat, height, elevation)
    tropCorr = (d_dry + d_wet) * m_elev
    # tropCorr = d_dry * dryM + d_wet * wetM
    return tropCorr