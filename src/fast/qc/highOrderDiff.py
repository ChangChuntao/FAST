from fast.com.gnssParameter import getBandFreq, CLIGHT, bandComb, obsFreq,freq_parts
import numpy as np
import datetime

def culHighOrderDiff(epochOrderData):
    diffCount = len(epochOrderData)
    backDiff = epochOrderData
    while diffCount > 1:
        updateDiff = []
        for diffIndex in range(len(backDiff) - 1, 0, -1):
            updateDiff.append(backDiff[diffIndex] - backDiff[diffIndex-1])
        backDiff = updateDiff[::-1]
        diffCount += -1
    return backDiff[0]


def getObsHighOrderDiff(obsHead, obsData, diffNum = 4, self = None):
    
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
    highBandChoose = {}

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

            if gSys not in highBandChoose:
                highBandChoose[gSys] = {}

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

                highBandChoose[gSys][band] = {}
                highBandChoose[gSys][band]['band1C'] = band
                highBandChoose[gSys][band]['band2C'] = band2
                highBandChoose[gSys][band]['band1L'] = bandL
                highBandChoose[gSys][band]['band2L'] = band2L
                highBandChoose[gSys][band]['band1freq'] = band1freq
                highBandChoose[gSys][band]['band1lambda'] = band1lamda
                highBandChoose[gSys][band]['band2freq'] = band2freq
                highBandChoose[gSys][band]['band2lambda'] = band2lamda
                
                highBandChoose[gSys][band]['COEFL1'] = -(band1freq * band1freq + band2freq*band2freq)/(band1freq*band1freq - band2freq*band2freq)
                highBandChoose[gSys][band]['COEFL2'] = 2*band2freq*band2freq/(band1freq*band1freq - band2freq*band2freq)

                lamdaW = CLIGHT / (band1freq - band2freq)
                highBandChoose[gSys][band]['lamdaW'] = lamdaW

    # print(highBandChoose)
    highData = {}
    interval = (list(obsData)[1] - list(obsData)[0]).total_seconds()
    prnIndex = 0
    for prn in satList:
        gSys = prn[0]
        if gSys not in obsFreq:
            continue
        if gSys not in highBandChoose:
            continue
        if self is not None:
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Calc. High. of " + prn +  " [" + barPercent + '] ' + percentage)
                QApplication.processEvents()


        for band in highBandChoose[gSys]:
            bandEpochList = []
            highList = []
            highGoodList = []
            epochGoodList = []
            band1L = highBandChoose[gSys][band]['band1L']
            band2L = highBandChoose[gSys][band]['band2L']
            band1C = highBandChoose[gSys][band]['band1C']
            band2C = highBandChoose[gSys][band]['band2C']
            freq1 = highBandChoose[gSys][band]['band1freq']
            freq2 = highBandChoose[gSys][band]['band2freq']
            lamda1 = highBandChoose[gSys][band]['band1lambda']
            lamda2 = highBandChoose[gSys][band]['band2lambda']
            lamdaW = highBandChoose[gSys][band]['lamdaW']
            COEFL1 = highBandChoose[gSys][band]['COEFL1']
            COEFL2 = highBandChoose[gSys][band]['COEFL2']
            for epoch in obsData:
                if prn not in obsData[epoch].keys():
                    continue
                if gSys not in highBandChoose:
                    continue
                if epoch < startdatetime or epoch > enddatetime:
                    continue
                L1 = obsData[epoch][prn][band1L]
                L2 = obsData[epoch][prn][band2L]
                P1 = obsData[epoch][prn][band1C]
                P2 = obsData[epoch][prn][band2C]
                if L1 is None or L2 is None or P1 is None or P2 is None:
                    continue
                if abs(P2 - P1) > 100: 
                    continue
                
                N_MW = L1 - L2 - (freq1 * P1 + freq2 * P2) / (freq1 + freq2) / lamdaW
                L_GF = lamda1 * L1 - lamda2 * L2
                P_GF = P2 - P1
                nowL = L1 * lamda1
                        
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
                    highList = [[nowL]]
                    continue
                if (epoch - bandEpochList[-1]).total_seconds() > interval:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list = [[0.3]]
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(0)
                    highList.append([nowL])
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

                if MW_CLIP or GF_CLIP:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list.append([0.15])
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(1)
                    highList.append([nowL])
                else:
                    bandEpochList.append(epoch)
                    N_MW_list[-1].append(N_MW)
                    MEAN_MW_list[-1].append(N_MW_MEAN)
                    L_GF_list[-1].append(L_GF)
                    SIGMA_list[-1].append(SIGMA)
                    P_GF_list[-1].append(P_GF)
                    slipList.append(0)
                    highList[-1].append(nowL)
                    if len(highList[-1]) > diffNum * 2:
                        difIndex = (diffNum + 1)*(-1)

                        nowDiff = culHighOrderDiff(highList[-1][difIndex:])
                        if diffNum == 4:
                            nowDiff = nowDiff / np.sqrt(70)
                        else:
                            nowDiff = nowDiff / np.sqrt(20)
                        if abs(nowDiff) > 100:
                            continue
                        highGoodList.append(nowDiff)
                        epochGoodList.append(epoch)
            if len(highGoodList) == 0:
                continue
            if gSys not in highData:
                highData[gSys] = {}
            if prn not in highData[gSys]:
                highData[gSys][prn] = {}
            highData[gSys][prn][band1L] = {}
            highData[gSys][prn][band1L]['epoch'] = epochGoodList
            highData[gSys][prn][band1L]['highOrder'] = highGoodList
        prnIndex += 1

    return highData


def getObsHighOrderDiffcc(obsHead, obsData, diffNum = 4, self = None):
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
    highBandChoose = {}

    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
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
        if len(bandChoose[gSys]) < 2 or gSys not in obsFreq:
            continue
        if self is not None:
            if gSys not in bandChooseInSelf:
                continue
        if gSys not in highBandChoose :
            highBandChoose[gSys] = {}
        for band in obsType[gSys]:
            if 'C' == band[0] or 'P' == band[0]:
                if self is not None:
                    if band[1:] not in bandChooseInSelf[gSys]:
                        continue
                if band in bandChoose[gSys][list(bandChoose[gSys])[0]]:
                    band2 = bandChoose[gSys][list(bandChoose[gSys])[1]][0]
                else:
                    band2 = bandChoose[gSys][list(bandChoose[gSys])[0]][0]
                
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

                highBandChoose[gSys][band] = {}
                highBandChoose[gSys][band]['band1C'] = band
                highBandChoose[gSys][band]['band2C'] = band2
                highBandChoose[gSys][band]['band1L'] = bandL
                highBandChoose[gSys][band]['band2L'] = band2L
                highBandChoose[gSys][band]['band1freq'] = band1freq
                highBandChoose[gSys][band]['band1lambda'] = band1lamda
                highBandChoose[gSys][band]['band2freq'] = band2freq
                highBandChoose[gSys][band]['band2lambda'] = band2lamda
                
                highBandChoose[gSys][band]['COEFL1'] = -(band1freq * band1freq + band2freq*band2freq)/(band1freq*band1freq - band2freq*band2freq)
                highBandChoose[gSys][band]['COEFL2'] = 2*band2freq*band2freq/(band1freq*band1freq - band2freq*band2freq)

                lamdaW = CLIGHT / (band1freq - band2freq)
                highBandChoose[gSys][band]['lamdaW'] = lamdaW

    # print(highBandChoose)
    highData = {}
    interval = (list(obsData)[1] - list(obsData)[0]).total_seconds()
    prnIndex = 0
    for prn in satList:
        gSys = prn[0]
        if gSys not in obsFreq:
            continue
        if gSys not in highBandChoose:
            continue
        if self is not None:
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Calc. High. of " + prn +  " [" + barPercent + '] ' + percentage)
                QApplication.processEvents()


        for band in highBandChoose[gSys]:
            bandEpochList = []
            highList = []
            highGoodList = []
            epochGoodList = []
            band1L = highBandChoose[gSys][band]['band1L']
            band2L = highBandChoose[gSys][band]['band2L']
            band1C = highBandChoose[gSys][band]['band1C']
            band2C = highBandChoose[gSys][band]['band2C']
            freq1 = highBandChoose[gSys][band]['band1freq']
            freq2 = highBandChoose[gSys][band]['band2freq']
            lamda1 = highBandChoose[gSys][band]['band1lambda']
            lamda2 = highBandChoose[gSys][band]['band2lambda']
            lamdaW = highBandChoose[gSys][band]['lamdaW']
            COEFL1 = highBandChoose[gSys][band]['COEFL1']
            COEFL2 = highBandChoose[gSys][band]['COEFL2']
            for epoch in obsData:
                if prn not in obsData[epoch].keys():
                    continue
                if gSys not in highBandChoose:
                    continue
                L1 = obsData[epoch][prn][band1L]
                L2 = obsData[epoch][prn][band2L]
                P1 = obsData[epoch][prn][band1C]
                P2 = obsData[epoch][prn][band2C]
                if L1 is None or L2 is None or P1 is None or P2 is None:
                    continue
                if abs(P2 - P1) > 100: 
                    continue
                nowL = L1 * lamda1
                
                if bandEpochList == []:
                    bandEpochList.append(epoch)
                    highList = [[nowL]]
                    continue
                if (epoch - bandEpochList[-1]).total_seconds() > interval:
                    highList.append([nowL])
                    bandEpochList.append(epoch)
                    continue
                highList[-1].append(nowL)
                bandEpochList.append(epoch)
                if len(highList[-1]) > diffNum * 2:
                    difIndex = (diffNum + 1)*(-1)

                    nowDiff = culHighOrderDiff(highList[-1][difIndex:])
                    if diffNum == 4:
                        nowDiff = nowDiff / np.sqrt(70)
                    else:
                        nowDiff = nowDiff / np.sqrt(20)
                    if abs(nowDiff) > 100:
                        continue
                    highGoodList.append(nowDiff)
                    epochGoodList.append(epoch)
            if len(highGoodList) == 0:
                continue
            if gSys not in highData:
                highData[gSys] = {}
            if prn not in highData[gSys]:
                highData[gSys][prn] = {}
            highData[gSys][prn][band1L] = {}
            highData[gSys][prn][band1L]['epoch'] = epochGoodList
            highData[gSys][prn][band1L]['highOrder'] = highGoodList
        prnIndex += 1

    return highData

def writeHod(highData, highFile):
    import math
    highFileWrite = open(highFile, 'w+')
    highFileWrite.write('# PGM       : FAST\n')
    highFileWrite.write('# Author    : Chuntao Chang\n')
    highFileWrite.write('# Inf       : Fourth-order diff\n')
    highFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    highFileWrite.write('#             END OF HEADER\n')
    highFileWrite.write('\n')
    highLines = ['\n']
    highFileWrite.write('+SAT\n')
    highFileWrite.write(' prnFreq    RMS[m]    MIN[m]    MAX[m]\n')
    highFileWrite.write(38*'-' + '\n')
    for gnssSys in highData:
        for prn in highData[gnssSys]:
            for band in highData[gnssSys][prn]:
                if len(highData[gnssSys][prn][band]['highOrder']) == 0:
                    continue
                prnFreqLine = ' ' + prn + '_' + band
                # 计算平方和
                square_sum = sum(x ** 2 for x in highData[gnssSys][prn][band]['highOrder'])
                # 计算均方根
                rms = math.sqrt(square_sum / len(highData[gnssSys][prn][band]['highOrder']))
                
                prnFreqLine += '%10.6f' % rms + '%10.6f' % min(highData[gnssSys][prn][band]['highOrder']) + '%10.6f' % max(highData[gnssSys][prn][band]['highOrder']) + '\n'
                highFileWrite.write(prnFreqLine)
                
                highLines.append('+' + prn + '_' + band + '\n')
                highLines.append('               epoch   diff(m)\n')
                for epoch, highOrder in zip(highData[gnssSys][prn][band]['epoch'], highData[gnssSys][prn][band]['highOrder']):
                    highLines.append(' ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + '%10.6f' % highOrder + '\n')
                highLines.append('-' + prn + '_' + band + '\n')
                highLines.append('\n')
    highFileWrite.write(38*'-' + '\n')
    highFileWrite.write('-SAT\n\n')
    highFileWrite.writelines(highLines)
    
if __name__ == '__main__':
    from fast.com.readObs import readObs, readObsHead

    file = r'test\unsa0010.23o'
    obsHead = readObsHead(file, needSatList=True)
    obsData = readObs(file, obsHead=obsHead)

    import time
    start_time = time.time()
    getObsHighOrderDiff(obsHead, obsData)
    end_time = time.time()
    execution_time = end_time - start_time
    print("run : ", execution_time, "s")
