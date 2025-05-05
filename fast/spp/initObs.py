# -*- coding: utf-8 -*-
# initObs           : initObs in SPP module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02



from itertools import islice
from fast.com.gnssTime import datetime2doys, datetime2mjds


def initObs(bandChoose, obsData, epoch, satPosInEpoch, satClkInEpoch):
    # time
    doys = datetime2doys(epoch)
    mjds = datetime2mjds(epoch)
    
    # init data
    obsDataInTime = {}
    obsDataInTime['gSysInf'] = {}
    obsDataInTime['obs'] = {}
    obsDataInTime['prnIndex'] = {}
    obsDataInTime['satUse'] = []
    obsDataInTime['doys'] = doys
    obsDataInTime['mjds'] = mjds
    
    # check data
    prni = 0
    for prn in obsData[epoch]:
        gnssSys = prn[0]
        if gnssSys not in bandChoose:
            continue
        BAND1, BAND2 = list(islice(bandChoose[gnssSys].keys(), 2))
        P1, P2 = obsData[epoch][prn][BAND1], obsData[epoch][prn][BAND2]
        if prn not in satPosInEpoch or prn not in satClkInEpoch:
            continue
        if None in [P1, P2]:
            continue
        if abs(P1 - P2) > 30:
            continue
        obsDataInTime['prnIndex'][prn] = prni
        prni += 1
        obsDataInTime['satUse'].append(prn)
        obsDataInTime['obs'][prn] = {}
        obsDataInTime['obs'][prn]['P1'] = P1
        obsDataInTime['obs'][prn]['P2'] = P2
        if gnssSys not in obsDataInTime['gSysInf']:
            obsDataInTime['gSysInf'][gnssSys] = {}
            obsDataInTime['gSysInf'][gnssSys]['lambda1'] = bandChoose[gnssSys][BAND1]['lambda']
            obsDataInTime['gSysInf'][gnssSys]['lambda2'] = bandChoose[gnssSys][BAND2]['lambda']
            obsDataInTime['gSysInf'][gnssSys]['f1'] = bandChoose[gnssSys][BAND1]['freq']
            obsDataInTime['gSysInf'][gnssSys]['f2'] = bandChoose[gnssSys][BAND2]['freq']
    isLess = False
    if len(obsDataInTime['satUse']) < 4:
        isLess = True
    return obsDataInTime, isLess