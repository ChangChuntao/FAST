# -*- coding: utf-8 -*-
# CMC               : Time diff Code minus Phase
# Author            : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)      : The GNSS Center, Wuhan University
# Creation Date     : 2023.10.16
# Latest Version    : 3.01.00 - 2026.03.18


from fast.com.gnssParameter import getBandFreq, CLIGHT, obsFreq, freq_parts
import numpy as np
import datetime

def CMC(obsHead, obsData, self = None):
    obsType = obsHead['OBS TYPES']
    bandChoose = {}
    for gSys in obsType:
        if gSys not in bandChoose:
            bandChoose[gSys] = {}
        for band in obsType[gSys]:
            if 'C' == band[0] or 'P' == band[0]:
                if band[1] not in bandChoose[gSys]:
                    bandChoose[gSys][band[1]] = []
                bandChoose[gSys][band[1]].append(band)
    cmcBandChoose = {}

    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        satList = [item for item in self.qcChoosePrnBox.currentText().split(',') if item != '']
        bandChooseInSelf = {}
        for sys_band in self.qcChooseBandBox.currentText().split(','):
            if sys_band == '':
                continue
            nowSys = sys_band[0]
            if nowSys not in bandChooseInSelf:
                bandChooseInSelf[nowSys] = []
            bandChooseInSelf[nowSys].append(sys_band[2:])
    else:
        satList = obsHead['prn']


    for gSys in obsType:
            # 基本校验：必须有两个频段且在频率表 obsFreq 中
            if gSys not in bandChoose or len(bandChoose[gSys]) < 2 or gSys not in obsFreq:
                continue
            if self is not None:
                if gSys not in bandChooseInSelf:
                    continue
            
            # 2. 【核心逻辑】根据优先级确定本次计算要使用的两个频点键 (k1, k2)
            k1, k2 = None, None
            if gSys in freq_parts:
                for p1, p2 in freq_parts[gSys]:
                    # 检查数据中是否同时具备这两个频点数字
                    if p1 in bandChoose[gSys] and p2 in bandChoose[gSys]:
                        k1, k2 = p1, p2
                        break
            
            # 如果优先级列表里没配上，则取当前系统已有的前两个频点
            if k1 is None:
                sorted_keys = sorted(bandChoose[gSys].keys())
                k1, k2 = sorted_keys[0], sorted_keys[1]

            if gSys not in cmcBandChoose:
                cmcBandChoose[gSys] = {}

            # 3. 遍历 obsType 匹配观测码
            for band in obsType[gSys]:
                # 只处理伪距观测值 (C 或 P 开头)
                if band[0] not in ['C', 'P']:continue
                if band.startswith('C') or band.startswith('P'):
                    if self is not None:
                        if band[1:] not in bandChooseInSelf[gSys]:
                            continue
                    
                    # --- 沿用并修正你的匹配逻辑 ---
                    # 如果当前观测码属于选定的频点 k1，则配对的 band2 取自频点 k2 的第一个码
                    if band in bandChoose[gSys][k1]:
                        band2 = bandChoose[gSys][k2][0]
                    # 如果当前观测码属于选定的频点 k2，则配对的 band2 取自频点 k1 的第一个码
                    elif band in bandChoose[gSys][k2]:
                        band2 = bandChoose[gSys][k1][0]
                    else:
                        # 如果是该系统其他的频点（如北斗已选 2&6，碰到频点 1），则跳过
                        continue
                
                bandL = 'L' + band[1:]
                band2L = 'L' + band2[1:]
                if bandL not in obsType[gSys] or band2 not in obsType[gSys] or band2L not in obsType[gSys]:
                    continue

                band1freq = getBandFreq(gSys, band)
                band2freq = getBandFreq(gSys, band2)

                if band1freq is None or band2freq is None:
                    continue

                band1freq = band1freq * 1.e6
                band1lamda = CLIGHT / band1freq

                band2freq = band2freq * 1.e6
                band2lamda = CLIGHT / band2freq

                cmcBandChoose[gSys][band] = {}
                cmcBandChoose[gSys][band]['band1freq'] = band1freq
                cmcBandChoose[gSys][band]['band1lambda'] = band1lamda
                cmcBandChoose[gSys][band]['band2freq'] = band2freq
                cmcBandChoose[gSys][band]['band2lambda'] = band2lamda
                cmcBandChoose[gSys][band]['band1C'] = band
                cmcBandChoose[gSys][band]['band2C'] = band2
                cmcBandChoose[gSys][band]['band1L'] = bandL
                cmcBandChoose[gSys][band]['band2L'] = band2L
                
                cmcBandChoose[gSys][band]['COEFL1'] = -(band1freq * band1freq + band2freq*band2freq)/(band1freq*band1freq - band2freq*band2freq)
                cmcBandChoose[gSys][band]['COEFL2'] = 2*band2freq*band2freq/(band1freq*band1freq - band2freq*band2freq)

                lamdaW = CLIGHT / (band1freq - band2freq)
                cmcBandChoose[gSys][band]['lamdaW'] = lamdaW

    cmcData = {}
    interval = (list(obsData)[1] - list(obsData)[0]).total_seconds()
    prnIndex = 0
    for prn in satList:
        gSys = prn[0]
        if gSys not in obsFreq:
            continue
        if gSys not in cmcBandChoose:
            continue
        if self is not None:
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Calc. CMC of " + prn +  " [" + barPercent + '] ' + percentage)
                QApplication.processEvents()

        for band in cmcBandChoose[gSys]:
            bandEpochList = []
            cmcList = []
            epochGoodList = []
            cmcGoodList = []
            band1L = cmcBandChoose[gSys][band]['band1L']
            band2L = cmcBandChoose[gSys][band]['band2L']
            band1C = cmcBandChoose[gSys][band]['band1C']
            band2C = cmcBandChoose[gSys][band]['band2C']
            freq1 = cmcBandChoose[gSys][band]['band1freq']
            freq2 = cmcBandChoose[gSys][band]['band2freq']
            lamda1 = cmcBandChoose[gSys][band]['band1lambda']
            lamda2 = cmcBandChoose[gSys][band]['band2lambda']
            lamdaW = cmcBandChoose[gSys][band]['lamdaW']
            COEFL1 = cmcBandChoose[gSys][band]['COEFL1']
            COEFL2 = cmcBandChoose[gSys][band]['COEFL2']
            for epoch in obsData:
                if prn not in obsData[epoch].keys():
                    continue
                if gSys not in cmcBandChoose:
                    continue
                if epoch < startdatetime or epoch > enddatetime:
                    continue
                L1 = obsData[epoch][prn][band1L]
                L2 = obsData[epoch][prn][band2L]
                P1 = obsData[epoch][prn][band1C]
                P2 = obsData[epoch][prn][band2C]
                if L1 is None or L2 is None or P1 is None or P2 is None:
                    continue
                if abs(P2 - P1) > 30:
                    continue
                
                N_MW = L1 - L2 - (freq1 * P1 + freq2 * P2) / (freq1 + freq2) / lamdaW
                L_GF = lamda1 * L1 - lamda2 * L2
                P_GF = P2 - P1
                nowCmc = P1 - lamda1 * L1
                # nowCmc = lamda1 * L1 - lamda2 * L2
                # nowCmc = P2 - P1
                
                MW_CLIP = False
                GF_CLIP = False
                if bandEpochList == []:
                    bandEpochList = [epoch]
                    N_MW_list = [[N_MW]]
                    MEAN_MW_list = [[N_MW]]
                    SIGMA_list = [[0.3]]
                    L_GF_list = [[L_GF]]
                    P_GF_list = [[P_GF]]
                    slipList = [0]
                    cmcList = [[nowCmc]]
                    continue
                if (epoch - bandEpochList[-1]).total_seconds() > interval:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list = [[0.3]]
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(0)
                    cmcList.append([nowCmc])
                    continue

                if len(N_MW_list[-1]) < 2 :
                    SIGMA_I_BACK = 0.15
                else:
                    SIGMA_I_BACK = SIGMA_list[-1][-1]

                N_MW_MEAN_BACK = MEAN_MW_list[-1][-1]
                N_MW_MEAN = N_MW_MEAN_BACK + (N_MW - N_MW_MEAN_BACK)/(len(MEAN_MW_list[-1]) + 1)
                SIGMA2 = SIGMA_I_BACK * SIGMA_I_BACK + ((N_MW - N_MW_MEAN_BACK) ** 2 - SIGMA_I_BACK*SIGMA_I_BACK) / (len(MEAN_MW_list[-1]) + 1)
                SIGMA = np.sqrt(SIGMA2)
                if abs(N_MW - N_MW_MEAN) >= 4 * SIGMA_I_BACK:
                    MW_CLIP = True

                # GF-CHECK
                if not MW_CLIP and len(L_GF_list[-1]) > 1:
                    if abs(L_GF - L_GF_list[-1][-1]) > 0.15:
                        GF_CLIP = True

                MW_CLIP = False
                GF_CLIP = False
                deltCMC = (nowCmc - cmcList[-1][-1])/np.sqrt(2)

                if MW_CLIP or GF_CLIP or abs(deltCMC) > 1000:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list.append([0.15])
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(1)
                    cmcList.append([nowCmc])
                else:
                    epochGoodList.append(epoch)
                    cmcGoodList.append(deltCMC)
                    bandEpochList.append(epoch)
                    N_MW_list[-1].append(N_MW)
                    MEAN_MW_list[-1].append(N_MW_MEAN)
                    L_GF_list[-1].append(L_GF)
                    SIGMA_list[-1].append(SIGMA)
                    P_GF_list[-1].append(P_GF)
                    cmcList[-1].append(nowCmc)
                    slipList.append(0)
            if gSys not in cmcData:
                cmcData[gSys] = {}
            if prn not in cmcData[gSys]:
                cmcData[gSys][prn] = {}
            cmcData[gSys][prn][band] = {}
            cmcData[gSys][prn][band]['epoch'] = epochGoodList
            cmcData[gSys][prn][band]['cmc'] = cmcGoodList
        prnIndex += 1

    return cmcData

def writeCmc(cmcData, cmcFile):
    import math
    cmcFileWrite = open(cmcFile, 'w+')
    cmcFileWrite.write('# PGM       : FAST\n')
    cmcFileWrite.write('# Author    : Chuntao Chang\n')
    cmcFileWrite.write('# Inf       : Time-differenced code minus phase\n')
    cmcFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    cmcFileWrite.write('#             END OF HEADER\n')
    cmcFileWrite.write('\n')
    cmcLines = []
    cmcFileWrite.write('+SAT\n')
    cmcFileWrite.write(' prnFreq    RMS[m]    MIN[m]    MAX[m]\n')
    cmcFileWrite.write(38*'-' + '\n')
    for gnssSys in cmcData:
        for prn in cmcData[gnssSys]:
            for band in cmcData[gnssSys][prn]:
                if len(cmcData[gnssSys][prn][band]['cmc']) == 0:
                    continue
                prnFreqLine = ' ' + prn + '_' + band
                # 计算平方和
                square_sum = sum(x ** 2 for x in cmcData[gnssSys][prn][band]['cmc'])
                # 计算均方根
                rms = math.sqrt(square_sum / len(cmcData[gnssSys][prn][band]['cmc']))

                prnFreqLine += '%10.4f' % rms + '%10.4f' % min(cmcData[gnssSys][prn][band]['cmc']) + '%10.4f' % max(cmcData[gnssSys][prn][band]['cmc']) + '\n'
                cmcFileWrite.write(prnFreqLine)
                cmcLines.append('+' + prn + '_' + band + '\n')
                cmcLines.append('               epoch   diff(m)\n')
                for epoch, cmc in zip(cmcData[gnssSys][prn][band]['epoch'], cmcData[gnssSys][prn][band]['cmc']):
                    cmcLines.append(' ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + '%10.3f' % cmc + '\n')
                cmcLines.append('-' + prn + '_' + band + '\n')
                cmcLines.append('\n')
    cmcFileWrite.write(38*'-' + '\n')
    cmcFileWrite.write('-SAT\n\n')
    cmcFileWrite.writelines(cmcLines)

if __name__ == '__main__':
    from fast.com.readObs import readObs, readObsHead

    file = r'test\abpo0010.23o'
    obsHead = readObsHead(file, needSatList=True)
    obsData = readObs(file, obsHead=obsHead)

    import time
    start_time = time.time()
    CMC(obsHead, obsData)
    end_time = time.time()
    execution_time = end_time - start_time
    print("run : ", execution_time, "s")