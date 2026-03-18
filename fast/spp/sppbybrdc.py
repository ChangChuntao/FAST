# -*- coding: utf-8 -*-
# SPP               : Standard point positioning  by nav
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.01.00 - 2026.03.18
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2025.07.13 - Version 3.00.04

from fast.com.sat2siteAngle import getEle, sat2siteAngle
from fast.com.gnssParameter import CLIGHT, bandDictGetFreq, bandDictGetFreqPos, bds3MEOList
from fast.com.xyz2neu import xyz2neu
from fast.com.gnssTime import datetime2allgnssTime
from fast.spp.initObs import initObs
from fast.spp.satPos import satPos
from fast.spp.corr import earthRotation, relativistic, satPCO, varerr
from fast.com.xyz2blh import bl2enuRot, geodist, xyz2blh
from fast.com.pub import printPanda, rms
from fast.spp.trop import tropColins
from fast.com.readNav import readNav
from fast.com.nav2posclk import getTgdInNav
import matplotlib.dates as mdate
import datetime
import numpy as np
import time

def spp(obsHead, obsData, navData, bandChoose, startDatetime, endDatetime, cutoff = 7, self = None, posFile = None):
    
    '''
    广播星历计算伪距单点定位
        by ChangChuntao -> 2022.09.24
    '''
    start_time = time.time()

    # 内部策略
    posCoord = 'ALL'
    # cutoff = 10
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
        # 修改为4个子图
        axsppx = figSPP.add_subplot(4,1,1)
        axsppy = figSPP.add_subplot(4,1,2)
        axsppz = figSPP.add_subplot(4,1,3)
        axsppdop = figSPP.add_subplot(4,1,4)  # 新增DOP子图
        
        # 网格样式
        for ax in [axsppx, axsppy, axsppz, axsppdop]:
            ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.5, zorder=0)
        
        axsppx.set_xticklabels([])
        axsppy.set_xticklabels([])
        axsppz.set_xticklabels([])  # 隐藏Z轴的x轴标签
        
        xfmt = mdate.DateFormatter('%dD-%HH')
        axsppdop.xaxis.set_major_formatter(xfmt)  # 只在DOP子图显示x轴标签
        
        figSPP.subplots_adjust(left=0.09, right=0.99, bottom=0.06, top=0.90, hspace=0.3)
        
        axsppdop.tick_params(axis='x', labelsize=12)
        axsppx.tick_params(axis='y', labelsize=12)
        axsppy.tick_params(axis='y', labelsize=12)
        axsppz.tick_params(axis='y', labelsize=12)
        axsppdop.tick_params(axis='y', labelsize=12)

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
                        if np.isnan(tropCorr): 
                            tropCorr = 0
                        
                    # weight
                    weight = 1.0
                    # weight = varerr(ele=Elevation)

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
                # 计算DOP值
                Q = np.linalg.pinv(G.T @ G)
                HDOP = np.sqrt(Q[0,0] + Q[1,1])
                VDOP = np.sqrt(Q[2,2])
                PDOP = np.sqrt(Q[0,0] + Q[1,1] + Q[2,2])
                GDOP = np.sqrt(Q[0,0] + Q[1,1] + Q[2,2] + Q[3,3])
                posData[epoch]['HDOP'] = HDOP
                posData[epoch]['VDOP'] = VDOP
                posData[epoch]['PDOP'] = PDOP
                posData[epoch]['GDOP'] = GDOP
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
                    if abs(l_value[0]) > 1000:
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
            try:
                if  len(list(posData)) % 5 == 0:
                    self.status.showMessage("SPP - " + epoch.strftime('%Y-%m-%d %H:%M:%S'))
                    QApplication.processEvents()
            except:
                pass
        if posFile is not None and len(list(posData)) > 2 and posCoord == 'XYZ':
            posOpen.write(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + ' ' + '%20.3f' % Xi[0][0] + '%20.3f' % Xi[1][0] + '%20.3f' % Xi[2][0] + '%20.3f' % Xi[3][0] + '\n')
            
        posData[epoch]['x'] = Xi[0][0].item()
        posData[epoch]['y'] = Xi[1][0].item()
        posData[epoch]['z'] = Xi[2][0].item()
        posData[epoch]['clk'] = Xi[3][0].item()
        X.append(Xi[0][0].item())
        Y.append(Xi[1][0].item())
        Z.append(Xi[2][0].item())

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
        HDOPList = []
        VDOPList = []
        PDOPList = []
        GDOPList = []
        
        for epoch in posData:
            N,E,U = xyz2neu(XMEAN, YMEAN, ZMEAN, posData[epoch]['x'], posData[epoch]['y'], posData[epoch]['z'], 'WGS84')
            Elist.append(E)
            NList.append(N)
            UList.append(U)
            HDOPList.append(posData[epoch]['HDOP'])
            VDOPList.append(posData[epoch]['VDOP'])
            PDOPList.append(posData[epoch]['PDOP'])
            GDOPList.append(posData[epoch]['GDOP'])
            
        # 配色方案 - 根据背景色设置不同配色
        is_dark = self.fastQtSetting['plotBackgroundColor'] == 'dark'
        
        if is_dark:
            # 暗色模式配色 - Catppuccin Mocha
            color_enu = '#89b4fa'      # 浅蓝 - ENU统一
            color_hdop = '#89b4fa'     # 浅蓝
            color_vdop = '#a6e3a1'     # 浅绿
            color_pdop = '#f9e2af'     # 浅黄
            color_gdop = '#cba6f7'     # 浅紫
            text_bg = '#313244'
            text_edge = '#45475a'
        else:
            # 浅色模式配色 - Tokyo Night Day
            color_enu = '#b36a6f'      # 豆沙红 (Dusty Rose) - 视觉焦点明确且不刺眼
            color_hdop = '#a5a58d'     # 浅咖绿 (Khaki Green)
            color_vdop = '#cb997e'     # 杏瓦色 (Apricot Tile)
            color_pdop = '#ddb892'     # 奶茶色 (Milk Tea)
            color_gdop = '#8b8c89'     # 中性灰 (Neutral Gray)
            text_bg = '#f8f9fa'        # 极浅的灰白背景，比纯白更有质感
            text_edge = '#dee2e6'      # 极细边框
        
        # 绘制位置误差图
        axsppx.set_title('POS: [' + '%.2f' % XMEAN + ', ' + '%.2f' % YMEAN + ', ' + '%.2f' % ZMEAN + ']', fontsize=18, fontweight='bold')
        
        # 东方向误差
        axsppx.scatter(np.array(list(posData)), np.array(Elist), marker='o', s=8, color=color_enu, zorder=10, alpha=0.8)
        axsppx.plot(np.array(list(posData)), np.array(Elist), color=color_enu, alpha=0.5, linewidth=1, zorder=9)
        axsppx.text(0.02, 0.90, 'RMS: ' + '%.3f' % rms(Elist) + ' m',
                transform=axsppx.transAxes, verticalalignment='top',
                horizontalalignment='left',
                bbox=dict(facecolor=text_bg, edgecolor=text_edge, boxstyle='round,pad=0.3'),
                zorder=30, fontsize=12)
        axsppx.set_ylabel('E [m]', fontsize=14)
        
        # 北方向误差
        axsppy.scatter(np.array(list(posData)), np.array(NList), marker='o', s=8, color=color_enu, zorder=10, alpha=0.8)
        axsppy.plot(np.array(list(posData)), np.array(NList), color=color_enu, alpha=0.5, linewidth=1, zorder=9)
        axsppy.text(0.02, 0.90, 'RMS: ' + '%.3f' % rms(NList) + ' m',
                transform=axsppy.transAxes, verticalalignment='top',
                horizontalalignment='left',
                bbox=dict(facecolor=text_bg, edgecolor=text_edge, boxstyle='round,pad=0.3'),
                zorder=30, fontsize=12)
        axsppy.set_ylabel('N [m]', fontsize=14)
        
        # 高程方向误差
        axsppz.scatter(np.array(list(posData)), np.array(UList), marker='o', s=8, color=color_enu, zorder=10, alpha=0.8)
        axsppz.plot(np.array(list(posData)), np.array(UList), color=color_enu, alpha=0.5, linewidth=1, zorder=9)
        axsppz.text(0.02, 0.90, 'RMS: ' + '%.3f' % rms(UList) + ' m',
                transform=axsppz.transAxes, verticalalignment='top',
                horizontalalignment='left',
                bbox=dict(facecolor=text_bg, edgecolor=text_edge, boxstyle='round,pad=0.3'),
                zorder=30, fontsize=12)
        axsppz.set_ylabel('U [m]', fontsize=14)
        
        # 绘制DOP值
        axsppdop.plot(np.array(list(posData)), np.array(HDOPList), label='HDOP', color=color_hdop, linewidth=1.5)
        axsppdop.plot(np.array(list(posData)), np.array(VDOPList), label='VDOP', color=color_vdop, linewidth=1.5)
        axsppdop.plot(np.array(list(posData)), np.array(PDOPList), label='PDOP', color=color_pdop, linewidth=1.5)
        axsppdop.plot(np.array(list(posData)), np.array(GDOPList), label='GDOP', color=color_gdop, linewidth=1.5)
        
        axsppdop.legend(loc='upper right', fontsize=11, ncol=2)
        axsppdop.set_ylabel('DOP', fontsize=14)
        
        # 计算并显示平均DOP值
        avg_hdop = np.mean(HDOPList)
        avg_vdop = np.mean(VDOPList)
        avg_pdop = np.mean(PDOPList)
        avg_gdop = np.mean(GDOPList)
        
        axsppdop.text(0.02, 0.90, f'Avg HDOP: {avg_hdop:.2f}  VDOP: {avg_vdop:.2f}  PDOP: {avg_pdop:.2f}  GDOP: {avg_gdop:.2f}',
                     transform=axsppdop.transAxes, verticalalignment='top',
                     horizontalalignment='left',
                     bbox=dict(facecolor=text_bg, edgecolor=text_edge, boxstyle='round,pad=0.3'),
                     zorder=30, fontsize=11)
        
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
                posOpen.write(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + ' ' + '%20.8f' % N + '%20.8f' % E + '%20.8f' % U + '%20.3f' % posData[epoch]['x'] + '%20.3f' % posData[epoch]['y'] + '%20.3f' % posData[epoch]['z'] + '%20.3f' % posData[epoch]['clk'] + '%10.3f' % posData[epoch]['HDOP'] + '%10.3f' % posData[epoch]['VDOP'] + '%10.3f' % posData[epoch]['PDOP'] + '%10.3f' % posData[epoch]['GDOP'] + '\n')
    
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
    posLines = ['    mjd       sod                 X[m]                Y[m]               Z[m]              CLK[ns]      HDOP      VDOP      PDOP      GDOP\n']
    for epoch in posData:
        nowGnssTime = datetime2allgnssTime(epoch)
        posLines.append(' ' + '%6d' % nowGnssTime.mjd + '%10.2f' % nowGnssTime.sod + 
                        ' ' + '%20.3f' % posData[epoch]['x'] + '%20.3f' % posData[epoch]['y'] 
                        + '%20.3f' % posData[epoch]['z'] + '%20.5f' % (posData[epoch]['clk'] / CLIGHT * 1.e9) 
                        + '%10.3f' % posData[epoch]['HDOP'] + '%10.3f' % posData[epoch]['VDOP'] 
                        + '%10.3f' % posData[epoch]['PDOP'] + '%10.3f' % posData[epoch]['GDOP'] 
                        + '\n')
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
    pass