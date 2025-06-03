# -*- coding: utf-8 -*-
# FAST              : Flexible And Swift Toolkit for GNSS Data
# noise             : Analyzes noise using the third-order time difference of the GF combination
# Author            : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)      : The GNSS Center, Wuhan University
# Creation Date     : 2023.10.16
# Latest Version    : 2023.10.16


from fast.com.gnssParameter import getBandFreq, CLIGHT, obsFreq
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

def phaseNoise(obsHead, obsData, self = None):
    """
    Analyzes phase noise using the third-order time difference of the Geometry-Free (GF) phase combination.

    This function processes GNSS observation data to calculate phase noise by analyzing the third-order
    difference of the GF phase combination. The GF combination helps isolate ionospheric effects, and
    the third-order difference provides insights into high-frequency noise components. The function
    supports multiple GNSS systems (e.g., GPS, BDS) and can be integrated with a graphical user interface (GUI)
    for real-time updates.

    Args:
        obsHead (dict): Observation header containing metadata (e.g., OBS TYPES, prn).
        obsData (dict): Observation data dictionary with epochs as keys.
        self (object, optional): Reference to the parent object (e.g., GUI). Defaults to None.
            If provided, the function will update the GUI status and process events.

    Returns:
        dict: Phase noise data dictionary containing the third-order differences for each satellite and band.

    Note:
        - This function assumes that the input observation data is valid and formatted correctly.
        - The function uses the `getBandFreq` function to retrieve band frequencies.
        - If `self` is provided, the function will use PyQt5 to update the GUI status.
        - The function supports multiple GNSS systems and bands, as specified in the observation header.

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
                print('band1freq:', band1freq, 'band2freq:', band2freq)
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

    phaseNoiseData = {}
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
                self.status.showMessage("Calc. PhaseNoise of " + prn +  " [" + barPercent + '] ' + percentage)
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
                nowGF = L_GF

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
                    iodList = [[nowGF]]
                    continue
                if (epoch - bandEpochList[-1]).total_seconds() > interval:
                    bandEpochList.append(epoch)
                    N_MW_list.append([N_MW])
                    MEAN_MW_list.append([N_MW])
                    SIGMA_list = [[0.3]]
                    L_GF_list.append([L_GF])
                    P_GF_list.append([P_GF])
                    slipList.append(0)
                    iodList.append([nowGF])
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
                    iodList.append([nowGF])
                else:
                    bandEpochList.append(epoch)
                    N_MW_list[-1].append(N_MW)
                    MEAN_MW_list[-1].append(N_MW_MEAN)
                    L_GF_list[-1].append(L_GF)
                    SIGMA_list[-1].append(SIGMA)
                    P_GF_list[-1].append(P_GF)
                    iodList[-1].append(nowGF)
                    slipList.append(0)
                    if len(iodList[-1]) > 3:
                        epochGoodList.append(epoch)
                        nowDiff = culHighOrderDiff(iodList[-1][-4:])/np.sqrt(40)
                        iodGoodList.append(nowDiff)

            if gSys not in phaseNoiseData:
                phaseNoiseData[gSys] = {}
            if prn not in phaseNoiseData[gSys]:
                phaseNoiseData[gSys][prn] = {}
            phaseNoiseData[gSys][prn][band] = {}
            phaseNoiseData[gSys][prn][band]['epoch'] = epochGoodList
            phaseNoiseData[gSys][prn][band]['phaseNoise'] = iodGoodList
        prnIndex += 1

    return phaseNoiseData


def writePhaseNoise(phaseNoiseData, phaseNoiseFile):
    import math
    phaseNoiseFileWrite = open(phaseNoiseFile, 'w+')
    phaseNoiseFileWrite.write('# PGM       : FAST\n')
    phaseNoiseFileWrite.write('# Author    : Chuntao Chang\n')
    phaseNoiseFileWrite.write('# Inf       : PhaseNoise\n')
    phaseNoiseFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    phaseNoiseFileWrite.write('#             END OF HEADER\n')
    phaseNoiseFileWrite.write('\n')
    phaseNoiseFileWrite.write('+SAT\n')
    phaseNoiseFileWrite.write(' prnFreq    RMS[m]    MIN[m]    MAX[m]\n')
    phaseNoiseFileWrite.write(38*'-' + '\n')
    ionLines = []
    for gnssSys in phaseNoiseData:
        for prn in phaseNoiseData[gnssSys]:
            for band in phaseNoiseData[gnssSys][prn]:
                if len(phaseNoiseData[gnssSys][prn][band]['phaseNoise']) == 0:
                    continue
                prnFreqLine = ' ' + prn + '_' + band
                # 计算平方和
                square_sum = sum(x ** 2 for x in phaseNoiseData[gnssSys][prn][band]['phaseNoise'])
                # 计算均方根
                rms = math.sqrt(square_sum / len(phaseNoiseData[gnssSys][prn][band]['phaseNoise']))

                prnFreqLine += '%10.6f' % rms + '%10.6f' % min(phaseNoiseData[gnssSys][prn][band]['phaseNoise']) + '%10.6f' % max(phaseNoiseData[gnssSys][prn][band]['phaseNoise']) + '\n'
                phaseNoiseFileWrite.write(prnFreqLine)

                ionLines.append('+' + prn + '_' + band + '\n')
                ionLines.append('               epoch  PhaseNoise\n')
                for epoch, ion in zip(phaseNoiseData[gnssSys][prn][band]['epoch'], phaseNoiseData[gnssSys][prn][band]['phaseNoise']):
                    ionLines.append(' ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + '%10.6f' % ion + '\n')
                ionLines.append('-' + prn + '_' + band + '\n')
                ionLines.append('\n')
    phaseNoiseFileWrite.write(38*'-' + '\n')
    phaseNoiseFileWrite.write('-SAT\n\n')
    phaseNoiseFileWrite.writelines(ionLines)