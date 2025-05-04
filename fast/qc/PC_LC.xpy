# -*- coding: utf-8 -*-
# FAST              : Flexible And Swift Toolkit for GNSS Data
# multipath         : Calculate multipath of GNSS observation data
# Author            : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)      : The GNSS Center, Wuhan University
# Creation Date     : 2023.10.16
# Latest Version    : 2023.10.16


from fast.com.gnssParameter import getBandFreq, CLIGHT, obsFreq
import numpy as np
import datetime

def PCLC(obsHead, obsData, self = None):
    """
    This subroutine calculates the multipath for each satellite from GNSS 
    observation data, using Turboedit method to detect cycle slips.

    Parameters:
    ----------
    obsHead :
        Observation File Header in Python Dictionary Format

    obsData :
        Observation File Data in Python Dictionary Format

    self :
        Python QT object

    Returns:
    ----------
    pclcData :
        mp DATA in Python Dictionary Format

    Notes
    ----------
        Modified for Python by Chuntao Chang

    Source
    ----------

        Blewitt, Geoffrey. "An automatic editing algorithm for GPS data." 
        Geophysical research letters 17.3 (1990): 199-202.
        Download at: https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=7e30122e9d5e599cc3b954111e0f19c978a51e35
    """
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
    pclcBandChoose = {}

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
        if len(bandChoose[gSys]) < 2 or gSys not in obsFreq:
            continue
        if self is not None:
            if gSys not in bandChooseInSelf:
                continue
        if gSys not in pclcBandChoose :
            pclcBandChoose[gSys] = {}
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
                if band1freq is None:
                    continue
                band1freq = band1freq* 1.e6
                band2freq = getBandFreq(gSys, band2)
                if band2freq is None:
                    continue
                band2freq = band2freq* 1.e6
                pclcBandChoose[gSys][band] = {}
                pclcBandChoose[gSys][band]['band1C'] = band
                pclcBandChoose[gSys][band]['band2C'] = band2
                pclcBandChoose[gSys][band]['band1L'] = bandL
                pclcBandChoose[gSys][band]['band2L'] = band2L
                print(gSys, band)
                1.e6
                band1lamda = CLIGHT / band1freq
                pclcBandChoose[gSys][band]['band1freq'] = band1freq
                pclcBandChoose[gSys][band]['band1lambda'] = band1lamda

                band2lamda = CLIGHT / band2freq
                pclcBandChoose[gSys][band]['band2freq'] = band2freq
                pclcBandChoose[gSys][band]['band2lambda'] = band2lamda
                
                pclcBandChoose[gSys][band]['COEFL1'] = band1freq * band1freq / (band1freq * band1freq - band2freq * band2freq)
                pclcBandChoose[gSys][band]['COEFL2'] = band2freq * band2freq / (band1freq * band1freq - band2freq * band2freq)

                lamdaW = CLIGHT / (band1freq - band2freq)
                pclcBandChoose[gSys][band]['lamdaW'] = lamdaW

    pclcData = {}
    interval = 60
    prnIndex = 0
    for prn in satList:
        gSys = prn[0]
        if gSys not in obsFreq:
            continue
        if gSys not in pclcBandChoose:
            continue
        if self is not None:
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Calc. PC-LC of " + prn +  " [" + barPercent + '] ' + percentage)
                QApplication.processEvents()


        for band in pclcBandChoose[gSys]:
            bandEpochList = []
            pclcList = []
            band1L = pclcBandChoose[gSys][band]['band1L']
            band2L = pclcBandChoose[gSys][band]['band2L']
            band1C = pclcBandChoose[gSys][band]['band1C']
            band2C = pclcBandChoose[gSys][band]['band2C']
            freq1 = pclcBandChoose[gSys][band]['band1freq']
            freq2 = pclcBandChoose[gSys][band]['band2freq']
            lamda1 = pclcBandChoose[gSys][band]['band1lambda']
            lamda2 = pclcBandChoose[gSys][band]['band2lambda']
            lamdaW = pclcBandChoose[gSys][band]['lamdaW']
            COEFL1 = pclcBandChoose[gSys][band]['COEFL1']
            COEFL2 = pclcBandChoose[gSys][band]['COEFL2']
            for epoch in obsData:
                if prn not in obsData[epoch].keys():
                    continue
                if gSys not in pclcBandChoose:
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
                nowPCLC = (P1*COEFL1 - P2*COEFL2) - (L1*COEFL1*lamda1 - L2*COEFL2*lamda2)
                
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
                    pclcList = [[nowPCLC]]
                    continue
                if (epoch - bandEpochList[-1]).total_seconds() > interval:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list = [[0.3]]
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(0)
                    meanPCLC_N = sum(pclcList[-1]) / len(pclcList[-1])
                    pclcList[-1] = [element - meanPCLC_N for element in pclcList[-1]]
                    pclcList.append([nowPCLC])
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
                    meanPCLC_N = sum(pclcList[-1]) / len(pclcList[-1])
                    pclcList[-1] = [element - meanPCLC_N for element in pclcList[-1]]
                    pclcList.append([nowPCLC])
                else:
                    bandEpochList.append(epoch)
                    N_MW_list[-1].append(N_MW)
                    MEAN_MW_list[-1].append(N_MW_MEAN)
                    L_GF_list[-1].append(L_GF)
                    SIGMA_list[-1].append(SIGMA)
                    P_GF_list[-1].append(P_GF)
                    slipList.append(0)
                    pclcList[-1].append(nowPCLC)
            if pclcList != []:
                meanPCLC_N = sum(pclcList[-1]) / len(pclcList[-1])
                pclcList[-1] = [element - meanPCLC_N for element in pclcList[-1]]
            if gSys not in pclcData:
                pclcData[gSys] = {}
            if prn not in pclcData[gSys]:
                pclcData[gSys][prn] = {}
            pclcData[gSys][prn][band] = {}
            pclcData[gSys][prn][band]['epoch'] = bandEpochList
            pclcData[gSys][prn][band]['pclc'] = [item for sublist in pclcList for item in sublist]
        prnIndex += 1

    return pclcData

def writePCLC(pclcData, pclcFile):
    import math
    pclcFileWrite = open(pclcFile, 'w+')
    pclcFileWrite.write('# PGM       : FAST\n')
    pclcFileWrite.write('# Author    : Chuntao Chang\n')
    pclcFileWrite.write('# Inf       : Multipath\n')
    pclcFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    pclcFileWrite.write('#             END OF HEADER\n')
    pclcFileWrite.write('\n')
    pclcFileWrite.write('+SAT\n')
    pclcFileWrite.write(' prnFreq    RMS[m]    MIN[m]    MAX[m]\n')
    pclcFileWrite.write(38*'-' + '\n')
    pclcLines = []
    for gnssSys in pclcData:
        for prn in pclcData[gnssSys]:
            for band in pclcData[gnssSys][prn]:
                if len(pclcData[gnssSys][prn][band]['pclc']) == 0:
                    continue
                prnFreqLine = ' ' + prn + '_' + band
                # 计算平方和
                square_sum = sum(x ** 2 for x in pclcData[gnssSys][prn][band]['pclc'])
                # 计算均方根
                rms = math.sqrt(square_sum / len(pclcData[gnssSys][prn][band]['pclc']))

                prnFreqLine += '%10.4f' % rms + '%10.4f' % min(pclcData[gnssSys][prn][band]['pclc']) + '%10.4f' % max(pclcData[gnssSys][prn][band]['pclc']) + '\n'
                pclcFileWrite.write(prnFreqLine)
                pclcLines.append('+' + prn + '_' + band + '\n')
                pclcLines.append('               epoch   pclc(m)\n')
                for epoch, pclcOrder in zip(pclcData[gnssSys][prn][band]['epoch'], pclcData[gnssSys][prn][band]['pclc']):
                    pclcLines.append(' ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + '%10.2f' % pclcOrder + '\n')
                pclcLines.append('-' + prn + '_' + band + '\n')
                pclcLines.append('\n')
    pclcFileWrite.write(38*'-' + '\n')
    pclcFileWrite.write('-SAT\n\n')
    pclcFileWrite.writelines(pclcLines)

# if __name__ == '__main__':
#     from fast.com.readObs import readObs, readObsHead

#     file = r'D:\Code\FAST\test\de012660.23o'
#     obsHead = readObsHead(file, needSatList=True)
#     obsData = readObs(file, obsHead=obsHead)

#     import time
#     start_time = time.time()
#     multipath(obsHead, obsData)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print("run : ", execution_time, "s")