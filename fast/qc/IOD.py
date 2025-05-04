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

def IOD(obsHead, obsData, self = None):
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
    iodData :
        mp DATA in Python Dictionary Format

    Notes
    ----------
        Modified for Python by Chuntao Chang

    Source
    ----------

        Blewitt, Geoffrey. "An automatic editing algorithm for GPS data." 
        Geophysical research letters 17.3 (1990): 199-202.
        Download at: http://www.beidou.gov.cn/zt/bdbz/201911/W020191125788479579263.pdf
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
    iodBandChoose = {}

    if self is not None:
        from PyQt5.QtWidgets import QApplication
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
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
        if gSys not in iodBandChoose :
            iodBandChoose[gSys] = {}
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

                iodBandChoose[gSys][band] = {}
                iodBandChoose[gSys][band]['band1freq'] = band1freq
                iodBandChoose[gSys][band]['band1lambda'] = band1lamda
                iodBandChoose[gSys][band]['band2freq'] = band2freq
                iodBandChoose[gSys][band]['band2lambda'] = band2lamda
                iodBandChoose[gSys][band]['band1C'] = band
                iodBandChoose[gSys][band]['band2C'] = band2
                iodBandChoose[gSys][band]['band1L'] = bandL
                iodBandChoose[gSys][band]['band2L'] = band2L
                
                iodBandChoose[gSys][band]['COEFL1'] = -(band1freq * band1freq + band2freq*band2freq)/(band1freq*band1freq - band2freq*band2freq)
                iodBandChoose[gSys][band]['COEFL2'] = 2*band2freq*band2freq/(band1freq*band1freq - band2freq*band2freq)

                lamdaW = CLIGHT / (band1freq - band2freq)
                iodBandChoose[gSys][band]['lamdaW'] = lamdaW

    iodData = {}
    interval = (list(obsData)[1] - list(obsData)[0]).total_seconds()
    prnIndex = 0
    for prn in satList:
        gSys = prn[0]
        if gSys not in obsFreq:
            continue
        if gSys not in iodBandChoose:
            continue
        if self is not None:
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Calc. IOD of " + prn +  " [" + barPercent + '] ' + percentage)
                QApplication.processEvents()


        for band in iodBandChoose[gSys]:
            bandEpochList = []
            iodList = []
            epochGoodList = []
            iodGoodList = []
            band1L = iodBandChoose[gSys][band]['band1L']
            band2L = iodBandChoose[gSys][band]['band2L']
            band1C = iodBandChoose[gSys][band]['band1C']
            band2C = iodBandChoose[gSys][band]['band2C']
            freq1 = iodBandChoose[gSys][band]['band1freq']
            freq2 = iodBandChoose[gSys][band]['band2freq']
            lamda1 = iodBandChoose[gSys][band]['band1lambda']
            lamda2 = iodBandChoose[gSys][band]['band2lambda']
            lamdaW = iodBandChoose[gSys][band]['lamdaW']
            COEFL1 = iodBandChoose[gSys][band]['COEFL1']
            COEFL2 = iodBandChoose[gSys][band]['COEFL2']
            for epoch in obsData:
                if prn not in obsData[epoch].keys():
                    continue
                if gSys not in iodBandChoose:
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
                nowIOD = COEFL2 / 2 * L_GF
                        
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
                    iodList = [[nowIOD]]
                    continue
                if (epoch - bandEpochList[-1]).total_seconds() > interval:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list = [[0.3]]
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(0)
                    iodList.append([nowIOD])
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
                    iodList.append([nowIOD])
                else:
                    epochGoodList.append(epoch)
                    iodForFreq1 = (nowIOD - iodList[-1][-1])/interval
                    iodGoodList.append(iodForFreq1)
                    bandEpochList.append(epoch)
                    N_MW_list[-1].append(N_MW)
                    MEAN_MW_list[-1].append(N_MW_MEAN)
                    L_GF_list[-1].append(L_GF)
                    SIGMA_list[-1].append(SIGMA)
                    P_GF_list[-1].append(P_GF)
                    iodList[-1].append(nowIOD)
                    slipList.append(0)
            if gSys not in iodData:
                iodData[gSys] = {}
            if prn not in iodData[gSys]:
                iodData[gSys][prn] = {}
            iodData[gSys][prn][band] = {}
            iodData[gSys][prn][band]['epoch'] = epochGoodList
            iodData[gSys][prn][band]['iod'] = iodGoodList
        prnIndex += 1

    return iodData


def writeIon(ionData, ionFile):
    import math
    ionFileWrite = open(ionFile, 'w+')
    ionFileWrite.write('# PGM       : FAST\n')
    ionFileWrite.write('# Author    : Chuntao Chang\n')
    ionFileWrite.write('# Inf       : Derivative of the ionospheric delay\n')
    ionFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    ionFileWrite.write('#             END OF HEADER\n')
    ionFileWrite.write('\n')
    ionFileWrite.write('+SAT\n')
    ionFileWrite.write(' prnFreq    RMS[m]    MIN[m]    MAX[m]\n')
    ionFileWrite.write(38*'-' + '\n')
    ionLines = []
    for gnssSys in ionData:
        for prn in ionData[gnssSys]:
            for band in ionData[gnssSys][prn]:
                if len(ionData[gnssSys][prn][band]['iod']) == 0:
                    continue
                prnFreqLine = ' ' + prn + '_' + band
                # 计算平方和
                square_sum = sum(x ** 2 for x in ionData[gnssSys][prn][band]['iod'])
                # 计算均方根
                rms = math.sqrt(square_sum / len(ionData[gnssSys][prn][band]['iod']))

                prnFreqLine += '%10.6f' % rms + '%10.6f' % min(ionData[gnssSys][prn][band]['iod']) + '%10.6f' % max(ionData[gnssSys][prn][band]['iod']) + '\n'
                ionFileWrite.write(prnFreqLine)

                ionLines.append('+' + prn + '_' + band + '\n')
                ionLines.append('               epoch  iod(m/s)\n')
                for epoch, ion in zip(ionData[gnssSys][prn][band]['epoch'], ionData[gnssSys][prn][band]['iod']):
                    ionLines.append(' ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + '%10.6f' % ion + '\n')
                ionLines.append('-' + prn + '_' + band + '\n')
                ionLines.append('\n')
    ionFileWrite.write(38*'-' + '\n')
    ionFileWrite.write('-SAT\n\n')
    ionFileWrite.writelines(ionLines)

# if __name__ == '__main__':
#     from fast.com.readObs import readObs, readObsHead

#     file = r'test\abpo0010.23o'
#     obsHead = readObsHead(file, needSatList=True)
#     obsData = readObs(file, obsHead=obsHead)

#     import time
#     start_time = time.time()
#     IOD(obsHead, obsData)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print("run : ", execution_time, "s")