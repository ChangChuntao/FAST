# -*- coding: utf-8 -*-
# thinning          : downsampling settings for Station selection
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.03
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2025.08.02 - Version 3.00.03

import numpy as np

def thinning(chooseSite, thinningValue,
             lmin=-180.0, lmax=180.0, bmin=-90.0, bmax=90.0):
    """
    在每个格网内只保留离几何中心最近的站点。 
        update 20250802 by chang chuntao

    Parameters
    ----------
    chooseSite : dict
        {sta_name: {'L': lon, 'B': lat, ...}}
    thinningValue : float
        格网边长（度）
    lmin/lmax/bmin/bmax : float
        研究区域经纬度范围

    Returns
    -------
    dict
        保留后的站点字典
    """

    # 用字典保存每个格网内的候选站列表
    grid2stations = {}

    for sta, info in chooseSite.items():
        lon = info['L']
        lat = info['B']

        # 计算站点所属格网的行列号
        col = int(np.floor((lon - lmin) / thinningValue))
        row = int(np.floor((lat - bmin) / thinningValue))

        key = (row, col)          # 格网唯一索引
        grid2stations.setdefault(key, []).append((sta, info))

    outSite = {}
    for (row, col), stas in grid2stations.items():
        # 格网几何中心
        center_lon = lmin + (col + 0.5) * thinningValue
        center_lat = bmin + (row + 0.5) * thinningValue

        # 找离中心最近的站
        def dist(item):
            _, info = item
            return (info['L'] - center_lon) ** 2 + (info['B'] - center_lat) ** 2

        best_sta, best_info = min(stas, key=dist)
        outSite[best_sta] = best_info

    return outSite