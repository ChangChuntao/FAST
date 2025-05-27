# -*- coding: utf-8 -*-
# gnssParameter  : gnss Parameter
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University 
# Latest Version : 3.00.00
# Creation Date  : 2022.03.27 - Version 1.00.00
# Date           : 2023.10.02 - Version 3.00.00

# 1. 坐标系统
# 1.1 椭球参数类
class coordSystemPara:
    def __init__(self, a, f, GM, omega):
        import math
        self.a = a
        self.f = f
        self.GM = GM
        self.omega = omega
        self.e2 = f * (2.0 - f)
        self.e = math.sqrt(self.e2)
        self.b = a * math.sqrt(1.0 - self.e2)
        self.eprime = math.sqrt(a ** 2 - self.b ** 2) / self.b


# 椭球参数, 对应class coordSystemPara
coordSystem = {'WGS84': coordSystemPara(6378137.0, 1.0 / 298.257223563, 3.986004415e14, 7.2921151467e-5),
               'CGCS2000': coordSystemPara(6378137.0, 1.0 / 298.257222101, 3.986004418e14, 7.292115e-5),
               'BDS': coordSystemPara(6378137.0, 1.0 / 298.257222101, 3.986004418e14, 7.292115e-5),
               'PZ90': coordSystemPara(6378136.0, 1.0 / 298.257840000, 3.986004418e14, 7.2921151467e-5),
               'GTRF': coordSystemPara(6378136.5, 1.0 / 298.257690000, 3.986004415e14, 7.292115e-5),
               'GRS80':coordSystemPara(6378137, 1.0 / 298.257222100882711243, 3.986005e14, 7.292115e-5),
               'BJ54':coordSystemPara(6378245.0, 1.0 / 298.3, 3.986004418e14, 7.292115e-5),
               'XIAN80':coordSystemPara(6378140.0, 1.0 / 298.257223563, 3.986004418e14, 7.292115e-5),}


# 北斗轨道类型 http://www.csno-tarc.cn/system/constellation
BDSoribtType = {"C01": "GEO", 
            "C02": "GEO", 
            "C03": "GEO", 
            "C04": "GEO", 
            "C05": "GEO", 
            "C06": "IGSO", 
            "C07": "IGSO",
            "C08": "IGSO", 
            "C09": "IGSO", 
            "C10": "IGSO", 
            "C11": "MEO", 
            "C12": "MEO", 
            "C13": "IGSO", 
            "C14": "MEO",
            "C16": "IGSO", 
            "C18": "IGSO", 
            "C19": "MEO", 
            "C20": "MEO", 
            "C21": "MEO", 
            "C22": "MEO", 
            "C23": "MEO",
            "C24": "MEO", 
            "C25": "MEO", 
            "C26": "MEO", 
            "C27": "MEO", 
            "C28": "MEO", 
            "C29": "MEO", 
            "C30": "MEO",
            "C31": "IGSO", 
            "C32": "MEO", 
            "C33": "MEO", 
            "C34": "MEO", 
            "C35": "MEO", 
            "C36": "MEO", 
            "C37": "MEO",
            "C38": "IGSO", 
            "C39": "IGSO", 
            "C40": "IGSO", 
            "C41": "MEO", 
            "C42": "MEO", 
            "C43": "MEO", 
            "C44": "MEO",
            "C45": "MEO", 
            "C46": "MEO", 
            "C57": "MEO", 
            "C58": "MEO", 
            "C59": "GEO", 
            "C60": "GEO", 
            "C61": "GEO"}

bds3MEOList = ['C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25',\
                'C26', 'C27', 'C28', 'C29', 'C30', 'C32', 'C33',\
                      'C34', 'C35', 'C36', 'C37', 'C41', 'C42',\
                          'C43', 'C44', 'C45', 'C46', 'C57', 'C58']

CLIGHT = 299792458.0

obsCodes = {}
obsCodes['G'] = {}
obsCodes['G']['L1'] = ['L1C', 'L1S', 'L1L', 'L1X', 'L1P', 'L1W', 'L1Y', 'L1M', 'L1N', 'L1']
obsCodes['G']['L2'] = ['L2C', 'L2D', 'L2S', 'L2L', 'L2X', 'L2P', 'L2W', 'L2Y', 'L2M', 'L2N', 'L2']
obsCodes['G']['L5'] = ['L5I', 'L5Q', 'L5X',  'L5']
obsCodes['C'] = {}
obsCodes['C']['B1'] = ['L2I', 'L2Q', 'L2X', 'L2']
obsCodes['C']['B3'] = ['L6I', 'L6Q', 'L6X', 'L6']
obsCodes['C']['B1C'] = ['L1D', 'L1P', 'L1X', 'L1']
obsCodes['C']['B2a'] = ['L5D', 'L5P', 'L5X', 'L5Q', 'L5']
obsCodes['C']['B1A'] = ['L1S', 'L1L', 'L1Z', 'L1I', 'L1Q', 'L1']
obsCodes['C']['B2'] = ['L7I', 'L7Q', 'L7X', 'L7']
obsCodes['C']['B2b'] = ['L7D', 'L7P', 'L7Z', 'L7']
obsCodes['C']['B2a+B2b'] = ['L8D', 'L8P', 'L8X', 'L8']
obsCodes['C']['B3A'] = ['L6D', 'L6P', 'L6Z', 'L6']
obsCodes['E'] = {}
obsCodes['E']['E1'] = ['L1A', 'L1B', 'L1C', 'L1X', 'L1Z', 'L1']
obsCodes['E']['E5a'] = ['L5I', 'L5Q', 'L5X', 'L5']
obsCodes['E']['E5b'] = ['L7I', 'L7Q', 'L7X', 'L7']
obsCodes['E']['E5a+E5b'] = ['L8I', 'L8Q', 'L8X', 'L8']
obsCodes['E']['E6'] = ['L6A', 'L6B', 'L6C', 'L6X', 'L6Z', 'L6']
obsCodes['S'] = {}
obsCodes['S']['L1'] = ['L1C', 'L1']
obsCodes['S']['L5'] = ['L5I', 'L5Q', 'L5X', 'L5']
obsCodes['I'] = {}
obsCodes['I']['L5'] = ['L5A', 'L5B', 'L5C', 'L5X', 'L5']
obsCodes['I']['S'] = ['L9A', 'L9B', 'L9C', 'L9X', 'L9']
obsCodes['J'] = {}
obsCodes['J']['L1'] = ['L1C', 'L1S', 'L1L', 'L1X', 'L1Z', 'L1B', 'L1']
obsCodes['J']['L2'] = ['L2S', 'L2L', 'L2X', 'L2']
obsCodes['J']['L5'] = ['L5I', 'L5Q', 'L5X', 'L5D', 'L5P', 'L5Z', 'L5']
obsCodes['J']['L6'] = ['L6S', 'L6L', 'L6X', 'L6E', 'L6Z', 'L6']
obsCodes['W'] = {}
obsCodes['W']['L1'] = ['L1I', 'L1Q', 'L1X', 'L1']
obsCodes['W']['L5'] = ['L5I', 'L5Q', 'L5X', 'L5']
obsCodes['W']['L6'] = ['L6I', 'L6Q', 'L6X', 'L6']


obsFreq = {}
obsFreq['G'] = {}
obsFreq['G']['L1'] = 1575.42
obsFreq['G']['L2'] = 1227.60
obsFreq['G']['L5'] = 1176.45
obsFreq['C'] = {}
obsFreq['C']['B1'] = 1561.098
obsFreq['C']['B1C'] = 1575.42
obsFreq['C']['B1A'] = 1575.42
obsFreq['C']['B2a'] = 1176.45
obsFreq['C']['B2'] = 1207.14
obsFreq['C']['B2b'] = 1207.14
obsFreq['C']['B2a+B2b'] = 1191.795
obsFreq['C']['B3'] = 1268.52
obsFreq['C']['B3A'] = 1268.52
obsFreq['E'] = {}
obsFreq['E']['E1'] = 1575.42
obsFreq['E']['E5a'] = 1176.45
obsFreq['E']['E5b'] = 1207.14
obsFreq['E']['E5a+E5b'] = 1191.795
obsFreq['E']['E6'] = 1278.75
obsFreq['S'] = {}
obsFreq['S']['L1'] = 1575.42
obsFreq['S']['L5'] = 1176.45
obsFreq['I'] = {}
obsFreq['I']['S'] = 2492.028
obsFreq['I']['L5'] = 1176.45
obsFreq['J'] = {}
obsFreq['J']['L1'] = 1575.42
obsFreq['J']['L2'] = 1227.60
obsFreq['J']['L5'] = 1176.45
obsFreq['J']['L6'] = 1278.75
obsFreq['W'] = {}
obsFreq['W']['L1'] = 1575.42
obsFreq['W']['L5'] = 1176.45
obsFreq['W']['L6'] = 1288.98

bandComb = {}
bandComb['G'] = [[1, 2], [1, 5]]
bandComb['C'] = [[2, 6], [1, 5]]
bandComb['E'] = [[1, 5]]
bandComb['S'] = [[1, 5]]
bandComb['I'] = [[5, 9]]
bandComb['J'] = [[1, 2], [1, 5]]
bandComb['W'] = [[1, 2], [1, 5]]

def getBandName(sys, phaseBand):
    if len(phaseBand) <3:
        phaseBand = 'L' + phaseBand[1] + phaseBand[0]
    else:
        phaseBand = 'L' + phaseBand[1:]
    nowBand = None
    for band in obsCodes[sys]:
        if phaseBand in obsCodes[sys][band]:
            nowBand = band
            
    return nowBand

def getBandFreq(sys, phaseBand):
    nowBand = getBandName(sys, phaseBand)
    if nowBand is None:
        print(sys, phaseBand, 'is None')
        return None
    return obsFreq[sys][nowBand]


def getBandFreqLambda(sys, phaseBand):
    nowBand = getBandName(sys, phaseBand)
    if nowBand is None:
        return None
    freq = obsFreq[sys][nowBand] * 1e6
    lambda1 = CLIGHT / freq
    return freq, lambda1

def bandDictGetFreq(bandChoose):
    bandDict = {}
    for sys in bandChoose:
        bandDict[sys] = {}
        for band in bandChoose[sys]:
            nowFreq = getBandFreq(sys, band)
            if nowFreq is not None:
                bandDict[sys][band] = getBandFreq(sys, band)
    return bandDict


def bandDictGetFreqPos(bandChoose):
    bandDict = {}
    for sys in bandChoose:
        bandDict[sys] = {}
        for band in bandChoose[sys]:
            freq, lambda1 = getBandFreqLambda(sys, band)
            if freq is not None:
                bandDict[sys][band] = {}
                bandDict[sys][band]['freq'] = freq
                bandDict[sys][band]['lambda'] = lambda1
    return bandDict

bandTypeChoose = 'PCWIXSAQLDBYMZN'

def getCode(obsHead, freqInCfg):
    codeChoose = {}
    for gSys in freqInCfg:
        if gSys not in obsHead['OBS TYPES']:
            continue
        codeChoose[gSys] = []
        for freq in freqInCfg[gSys]:
            for band in bandTypeChoose:
                if 'L' + freq + band in obsHead['OBS TYPES'][gSys] and 'C' + freq + band in obsHead['OBS TYPES'][gSys]:
                    codeChoose[gSys].append('C' + freq + band)
                    break
    return bandDictGetFreqPos(codeChoose)