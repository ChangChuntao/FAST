# -*- coding: utf-8 -*-
# SPP               : Standard point positioning  by nav
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02

from fast.com.sat2siteAngle import getEle, sat2siteAngle
from fast.com.gnssParameter import CLIGHT, bandDictGetFreq, bandDictGetFreqPos, bds3MEOList
from fast.com.xyz2neu import xyz2neu
from fast.com.gnssTime import datetime2allgnssTime
from fast.spp.initObs import initObs
from fast.spp.satPos import satPos
from fast.spp.corr import earthRotation, relativistic, satPCO
from fast.com.xyz2blh import bl2enuRot, geodist, xyz2blh
from fast.com.pub import printPanda, rms
from fast.spp.trop import tropColins
from fast.com.readNav import readNav
from fast.com.nav2posclk import getTgdInNav
import matplotlib.dates as mdate
import datetime
import numpy as np
import time

def spp(obsHead, obsData, navData, bandChoose, startDatetime, endDatetime, self = None, posFile = None):
    start_time = time.time()

    # 内部策略
    posCoord = 'ALL'
    cutoff = 5
    fisrtRun = True

    # 初始坐标
    if obsHead['Approx Position'][0] is not None:
        refCoord = obsHead['Approx Position']

    # 输出文件
    if posFile is not None:
        posOpen = open(posFile, 'w+')

    # cutOff
    cutoff = np.radians(cutoff)

    # 获取频率
    bandChoose = bandDictGetFreqPos(bandChoose)
    gSysNumInEpoch = len(list(bandChoose))

    # 初值
    
    initDict = [1000.0, 1000.0, 1000.0]
    for gSys in bandChoose:
        initDict.append(0)

    X0 = np.asmatrix(initDict).T

    gSysIndex = {}
    gnssCt = 0
    for gSys in bandChoose:
        gSysIndex[gSys] = gnssCt
        gnssCt += 1
    
    # 结果
    posData = {}
    X = []
    Y = []
    Z = []

    # plt
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        self.status.showMessage("Running...")
        QApplication.processEvents()
        self.figSPP.clf()
        figSPP = self.figSPP
        axsppx=figSPP.add_subplot(3,1,1)
        axsppy=figSPP.add_subplot(3,1,2)
        axsppz=figSPP.add_subplot(3,1,3)
        axsppx.grid(zorder=0)
        axsppy.grid(zorder=0)
        axsppz.grid(zorder=0)
        axsppx.set_xticklabels([])
        axsppy.set_xticklabels([])
        xfmt = mdate.DateFormatter('%dD-%HH')
        axsppz.xaxis.set_major_formatter(xfmt)
        figSPP.subplots_adjust(left=0.09, right=0.99, bottom=0.06, top=0.90)
        axsppz.tick_params(axis='x', labelsize=13)
        axsppx.tick_params(axis='y', labelsize=13)
        axsppy.tick_params(axis='y', labelsize=13)
        axsppz.tick_params(axis='y', labelsize=13)


    # 历元循环 最小二乘求解 无电离层组合
    for epoch in obsData:
        if startDatetime > epoch or endDatetime < epoch:
            continue
        satPosInEpoch, satClkInEpoch = satPos(bandChoose, obsData, navData, epoch)
        obsDataInTime, isLess = initObs(bandChoose, obsData, epoch, satPosInEpoch, satClkInEpoch)
        if isLess:
            continue

        less4 = False
        # 历元初始化
        posData[epoch] = {}
        # 时间转换为GNSS
        nowGnssTime = datetime2allgnssTime(epoch)

        # init
        satUse = obsDataInTime['satUse']
        mjds = obsDataInTime['mjds']
        doys = obsDataInTime['doys']
        prnIndex = obsDataInTime['prnIndex']
        satNumInEpoch = len(satUse)

        # init matrix
        gInit = np.zeros((satNumInEpoch, 3 + gSysNumInEpoch))
        wInit = np.zeros((satNumInEpoch, satNumInEpoch))
        yInit = np.zeros((satNumInEpoch, 1))

        iter = 0
        while iter < 12:
            iter += 1
            if less4:
                break
            satNum = 0
            G = np.copy(gInit)
            W = np.copy(wInit)
            y = np.copy(yInit)

            # init pos clk
            sitX_init   = float(X0[0,0])
            sitY_init   = float(X0[1,0])
            sitZ_init   = float(X0[2,0])
            sitClkAll_init = []
            for gSys in gSysIndex:
                sitClkAll_init.append(float(X0[3 + gSysIndex[gSys],0]))
            
            # site pos
            rr = np.array([sitX_init, sitY_init, sitZ_init])
            lat, lon, h = xyz2blh(sitX_init, sitY_init, sitZ_init)
            enuRot = bl2enuRot(lat, lon)
            blh = np.array([lat, lon, h])

            # 卫星循环
            for prn in satUse:
                # 判断系统是否被选择
                gnssSys = prn[0]
                prnIndexInC = prnIndex[prn]

                # init corr
                relativisticCorr = 0.0
                tropCorr = 0.0
                weight = 1
                TGD = 0.0
                shapiroCorr = 0.0
                    
                # sat poss
                rs = np.copy(satPosInEpoch[prn])

                # 获取频率
                P1, P2 = obsDataInTime['obs'][prn]['P1'], obsDataInTime['obs'][prn]['P2']
                f1, f2 = obsDataInTime['gSysInf'][gnssSys]['f1'], obsDataInTime['gSysInf'][gnssSys]['f2']

                # 无电离层组合观测值
                P_IF = (f1 ** 2) / (f1 ** 2 - f2 ** 2) * P1 - (f2 ** 2) / (f1 ** 2 - f2 ** 2) * P2
                
                # dis satDir
                approxDis, satDir = geodist(rs[:3], rr)

                # sat clock
                satClk = satClkInEpoch[prn]
                
                # sit clock
                sitClk_init = np.copy(sitClkAll_init[gSysIndex[gnssSys]])
    
                # TGD
                TGD = getTgdInNav(navData, f1, f2, prn, epoch)

                # trop 
                if not fisrtRun:
                    Zenith, Azimuth, Elevation  = getEle(rs[:3], rr, enuRot)
                    if Elevation < cutoff:
                        continue
                    if h < 200000:
                        tropCorr = tropColins(Elevation, lat, lon, h, doys)
                        
                    # weight
                    weight = 1.0

                
                # power
                W[prnIndexInC, prnIndexInC] = weight
                
                # direction cosines
                G[prnIndexInC, :3] = satDir
                G[prnIndexInC, gSysIndex[gnssSys] + 3] = 1.0
                
                # OMC
                approxDis += relativisticCorr - satClk * CLIGHT + sitClk_init + TGD + tropCorr - shapiroCorr
                ls = P_IF - (approxDis)
                y[prnIndexInC, 0] = ls

                # sat num count
                satNum += 1
            
            less4 = False
            if satNum < 4:
                printPanda('epoch - ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + ' -> The number of satellites is less than ' + str(satNum))
                less4 = True
                continue

            # lsq
            try:
                X_MAT = sppLsq(G,W,y)
            except:
                continue
        
            # 估计值
            Xi = X0 + X_MAT
            fisrtRun = False
            # next epoch init
            X0 = np.copy(Xi)
            # del bad sat
            if iter > 3:
                delSat = {}
                to_remove = None
                for lIndex, l_value in enumerate(y):
                    if abs(l_value[0]) > 10000:
                        delSat[satUse[lIndex]] = abs(l_value[0])
                        X_MAT[0] = 1
                if delSat:
                    max_delSat_key = max(delSat, key=delSat.get)
                    to_remove = satUse.index(max_delSat_key)
                if to_remove is not None:
                    del satUse[to_remove]

            if abs(X_MAT[0]) <= 0.0001 and abs(X_MAT[1]) <= 0.0001 and abs(X_MAT[2]) <= 0.0001:
                break
        
        if less4:
            continue
        if self is not None:
            if  len(list(posData)) % 5 == 0:
                self.status.showMessage("SPP - " + epoch.strftime('%Y-%m-%d %H:%M:%S'))
                QApplication.processEvents()

        if posFile is not None and len(list(posData)) > 2 and posCoord == 'XYZ':
            posOpen.write(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + ' ' + '%20.3f' % Xi[0][0] + '%20.3f' % Xi[1][0] + '%20.3f' % Xi[2][0] + '%20.3f' % Xi[3][0] + '\n')
            
        posData[epoch]['x'] = Xi[0][0].item()
        posData[epoch]['y'] = Xi[1][0].item()
        posData[epoch]['z'] = Xi[2][0].item()
        posData[epoch]['clk'] = Xi[3][0].item()
        X.append(Xi[0][0].item())
        Y.append(Xi[1][0].item())
        Z.append(Xi[2][0].item())
        # print('%20.3f' % Xi[0][0] + '%20.3f' % Xi[1][0] + '%20.3f' % Xi[2][0] + '%20.3f' % Xi[3][0])
    if len(X) == 0:
        return None, None, None, None
    XMEAN = (sum(X)/len(X))
    YMEAN = (sum(Y)/len(Y))
    ZMEAN = (sum(Z)/len(Z))

    printPanda('REF. COORD -> ' + '%20.3f' % XMEAN + '%20.3f' % YMEAN + '%20.3f' % ZMEAN)
    end_time = time.time()
    execution_time = end_time - start_time
    if self is not None:
        Elist = []
        NList = []
        UList = []
        for epoch in posData:
            N,E,U = xyz2neu(XMEAN, YMEAN, ZMEAN, posData[epoch]['x'], posData[epoch]['y'], posData[epoch]['z'], 'WGS84')
            Elist.append(E)
            NList.append(N)
            UList.append(U)
        axsppx.set_title('POS: [' + '%.2f' % XMEAN + ', ' + '%.2f' % YMEAN + ', ' + '%.2f' % ZMEAN + ']',fontsize=20)
        axsppx.scatter(np.array(list(posData)), np.array(Elist), marker='+', s=5, zorder=10)
        axsppy.scatter(np.array(list(posData)), np.array(NList), marker='+', s=5, zorder=10)
        axsppz.scatter(np.array(list(posData)), np.array(UList), marker='+', s=5, zorder=10)
        axsppx.plot(np.array(list(posData)), np.array(Elist), color = 'gray', alpha = 0.7, zorder=10)
        axsppy.plot(np.array(list(posData)), np.array(NList), color = 'gray', alpha = 0.7, zorder=10)
        axsppz.plot(np.array(list(posData)), np.array(UList), color = 'gray', alpha = 0.7, zorder=10)
        axsppx.text(0.02, 0.92, 'RMS: ' + '%.3f' % rms(Elist) + 'm',
                transform=axsppx.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize=15)
        axsppy.text(0.02, 0.92, 'RMS: ' + '%.3f' % rms(NList) + 'm',
                transform=axsppy.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize=15)
        axsppz.text(0.02, 0.92, 'RMS: ' + '%.3f' % rms(UList) + 'm',
                transform=axsppz.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize=15)
        axsppx.set_ylabel('E [m]', fontsize=16)
        axsppy.set_ylabel('N [m]', fontsize=16)
        axsppz.set_ylabel('U [m]', fontsize=16)
        self.status.showMessage("SPP completed.")
        self.status.showMessage('REF. COORD -> ' + '%20.3f' % XMEAN + '%20.3f' % YMEAN + '%20.3f' % ZMEAN)
        figSPP.canvas.draw()
        QApplication.processEvents()
    if posFile is not None:
        if posCoord == 'ENU':
            for epoch in list(posData):
                N,E,U = xyz2neu(XMEAN, YMEAN, ZMEAN, posData[epoch]['x'], posData[epoch]['y'], posData[epoch]['z'], 'WGS84')
                nowGnssTime = datetime2allgnssTime(epoch)
                posOpen.write(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + ' ' + '%20.8f' % N + '%20.8f' % E + '%20.8f' % U + '%20.3f' % posData[epoch]['clk'] + '\n')
        elif posCoord == 'ALL':
            for epoch in list(posData):
                N,E,U = xyz2neu(XMEAN, YMEAN, ZMEAN, posData[epoch]['x'], posData[epoch]['y'], posData[epoch]['z'], 'WGS84')
                nowGnssTime = datetime2allgnssTime(epoch)
                posOpen.write(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + ' ' + '%20.8f' % N + '%20.8f' % E + '%20.8f' % U + '%20.3f' % posData[epoch]['x'] + '%20.3f' % posData[epoch]['y'] + '%20.3f' % posData[epoch]['z'] + '%20.3f' % posData[epoch]['clk'] + '\n')
    
    print("SPP Time : ", execution_time, "s")
    return posData, XMEAN, YMEAN, ZMEAN

def writePosData(posData, posFile):
    posOpen = open(posFile, 'w+')
    posOpen.write('# PGM       : FAST\n')
    posOpen.write('# Author    : Chuntao Chang\n')
    posOpen.write('# Inf       : SPP\n')
    posOpen.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    posOpen.write('#             END OF HEADER\n')
    posOpen.write('\n')
    posLines = ['    mjd       sod                 X[m]                Y[m]               Z[m]              CLK[ns]\n']
    # print(posData)
    for epoch in posData:
        # print(epoch)
        nowGnssTime = datetime2allgnssTime(epoch)
        posLines.append(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + ' ' + '%20.3f' % posData[epoch]['x'] + '%20.3f' % posData[epoch]['y'] + '%20.3f' % posData[epoch]['z'] + '%20.5f' % (posData[epoch]['clk'] / CLIGHT * 1.e9) + '\n')
    posOpen.writelines(posLines)
    posOpen.close()


def sppLsq(G_MAT,W_MAT,y_MAT):
    G_MAT = G_MAT.astype(np.float64)
    W_MAT = W_MAT.astype(np.float64)
    y_MAT = y_MAT.astype(np.float64)
    P_MAT_inv = G_MAT.T @ W_MAT @ G_MAT
    P_MAT = np.linalg.pinv(P_MAT_inv)
    X_MAT = P_MAT @ G_MAT.T @ W_MAT @ y_MAT
    return X_MAT

if __name__ == '__main__':

    obsFile = r'D:\Code\fastpos\test\abpo0910.23o'
    brdFile = r'D:\Code\fastpos\test\brdc0910.23p'

    bandChoose = {'G': {'C1C': {'freq': 1575420000.0, 'lambda': 0.19029367279836487}, 'C2W': {'freq': 1227600000.0, 'lambda': 0.24421021342456825}}, 'E': {'C1C': {'freq': 1575420000.0, 'lambda': 0.19029367279836487}, 'C5Q': {'freq': 1176450000.0, 'lambda': 0.25482804879085386}}, 'C': {'C2I': {'freq': 1561098000.0, 'lambda': 0.19203948631027648}, 'C6I': {'freq': 1268520000.0, 'lambda': 0.2363324646044209}}}

    from fast.com.readObs import readObs, readObsHead
    import datetime
    startDatetime = datetime.datetime(2023,4,1)
    endDatetime = datetime.datetime(2023,4,1,2)
    obsData = readObs(obsFile)
    obsHead = readObsHead(obsFile)
    brdData = readNav(brdFile)
    posFile = r'D:\Code\FAST\fast\spp\sppbybrdc.txt'
    posData, XMEAN, YMEAN, ZMEAN =spp(obsHead, obsData, brdData, bandChoose, startDatetime, endDatetime, self = None, posFile = posFile)
    # spp(obsFile, sp3File, clkFile, bandChoose,startDatetime, endDatetime, posFile=posFile)
    ...