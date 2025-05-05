# -*- coding: utf-8 -*-
# satPos            : get satPos / clk by nav
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02


from itertools import islice
import numpy as np
import datetime

from fast.com.gnssParameter import CLIGHT, bds3MEOList
from fast.com.nav2posclk import getClkInNav, getPosInNav

def satPos(bandChoose, obsData, navData, epoch):
    satPosInEpoch = {}
    satClkInEpoch = {}
    for prn in obsData[epoch]:
        gnssSys = prn[0]
        if gnssSys not in bandChoose:
            continue
        if gnssSys == 'C' and (prn not in bds3MEOList):
            continue
        if prn not in navData:
            continue
        BAND1, BAND2 = list(islice(bandChoose[gnssSys].keys(), 2))
        C1, C2 = obsData[epoch][prn][BAND1], obsData[epoch][prn][BAND2]
        if C1 is None or C2 is None:
            continue
        bandDif = abs(C1 - C2)
        if bandDif > 100:
            continue
        aveP = (C1 + C2) / 2
        epochFind = epoch - datetime.timedelta(seconds=aveP/CLIGHT)
        satClk = getClkInNav(navData, prn, epochFind)
        if satClk is None:
            continue
        epochFind = epochFind - datetime.timedelta(seconds=satClk)
        satX, satY, satZ, satVX, satVY, satVZ = getPosInNav(navData, prn, epochFind, epochFind)
        if satX is not None and satClk is not None:
            satPosInEpoch[prn] = np.array([satX, satY, satZ, satVX, satVY, satVZ])
            satClkInEpoch[prn] = satClk
    return satPosInEpoch, satClkInEpoch