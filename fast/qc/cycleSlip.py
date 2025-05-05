# -*- coding: utf-8 -*-
# FAST              : Flexible And Swift Toolkit for GNSS Data
# cycleSlip         : Calculate cycle slips ratio of GNSS observation data
# Author            : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)      : The GNSS Center, Wuhan University
# Creation Date     : 2023.10.16
# Latest Version    : 2023.10.16

from fast.com.gnssParameter import getBandFreq, CLIGHT, bandComb
import numpy as np
import time
import datetime

def turboedit(obsHead, obsData, self = None):
    """
    This subroutine calculates the Cycle Slips Ratio (CSR) for each satellite from GNSS 
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
    slipData :
        slip DATA in Python Dictionary Format

    Notes
    ----------
        Modified for Python by Chuntao Chang

    """

    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        satListInSelf = [item for item in self.qcChoosePrnBox.currentText().split(',') if item != '']
        nowSys = self.qcChooseSysBox.currentText()
        gnssSystem = []
        for gnssSys in nowSys.split(','):
            if '' != gnssSys:
                gnssSystem.append(gnssSys)
        satList = satListInSelf
    else:
        satList = obsHead['prn']

    obsType = obsHead['OBS TYPES']
    bandChoose = {}
    for gSys in obsType:
        if gSys not in bandChoose:
            bandChoose[gSys] = {}
        for band in obsType[gSys]:
            if 'L' == band[0]:
                if band[1] not in bandChoose[gSys]:
                    bandChoose[gSys][band[1]] = []
                bandC = 'C' + band[1:]
                if bandC in obsType[gSys]:
                    bandChoose[gSys][band[1]].append(band)
                elif 'P' + band[1:] in obsType[gSys]:
                    bandChoose[gSys][band[1]].append(band)
    cycleSlipBandChoose = {}
    for gSys in bandComb:
        if gSys in bandChoose:
            for comb in bandComb[gSys]:
                band1 = str(comb[0])
                band2 = str(comb[1])
                if band1 in bandChoose[gSys] and band2 in bandChoose[gSys]:
                    if len(bandChoose[gSys][band1]) == 0  or len(bandChoose[gSys][band2]) == 0:
                        continue
                    if bandChoose[gSys][band1][0] is None or bandChoose[gSys][band2][0] is None:
                        continue
                    freq1 = getBandFreq(gSys, bandChoose[gSys][band1][0])
                    freq2 = getBandFreq(gSys, bandChoose[gSys][band2][0])
                    if freq1 is None or freq2 is None:
                        continue
                    cycleSlipBandChoose[gSys] = {}
                    freq1 = freq1 * 1.e6
                    freq2 = freq2 * 1.e6
                    cycleSlipBandChoose[gSys][bandChoose[gSys][band1][0]] = {}
                    cycleSlipBandChoose[gSys][bandChoose[gSys][band2][0]] = {}
                    cycleSlipBandChoose[gSys][bandChoose[gSys][band1][0]]['freq'] = freq1
                    cycleSlipBandChoose[gSys][bandChoose[gSys][band2][0]]['freq'] = freq2
                    cycleSlipBandChoose[gSys][bandChoose[gSys][band1][0]]['lambda'] = CLIGHT / freq1
                    cycleSlipBandChoose[gSys][bandChoose[gSys][band2][0]]['lambda'] = CLIGHT / freq2
                    cycleSlipBandChoose[gSys]['lambdaW'] = CLIGHT / (freq1 - freq2)
                    break
    
    slipData = {}
    interval = (list(obsData)[1] - list(obsData)[0]).total_seconds()
    prnData = []
    prnIndex = 0
    for prn in satList:
        slipList = []
        prnEpochList = []
        for epoch in obsData:
            if prn not in obsData[epoch].keys():
                continue
            gSys = prn[0]
            if gSys not in cycleSlipBandChoose:
                continue
            if epoch < startdatetime or epoch > enddatetime:
                continue
            if self is not None:
                if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                    completed = int(20 * prnIndex / len(satList)) - 1
                    remaining = 20 - completed
                    barPercent = '=' * completed + '>' + '+' * remaining
                    percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                    self.status.showMessage("Calc. Slip of " + prn +  " [" + barPercent + '] ' + percentage)
                    QApplication.processEvents()
            band1L = list(cycleSlipBandChoose[gSys])[0]
            band2L = list(cycleSlipBandChoose[gSys])[1]
            band1C = 'C' + band1L[1:]
            band2C = 'C' + band2L[1:]
            if band1C not in obsData[epoch][prn]:
                band1C = 'P' + band1L[1:]
            if band2C not in obsData[epoch][prn]:
                band2C = 'P' + band2L[1:]
            L1 = obsData[epoch][prn][band1L]
            L2 = obsData[epoch][prn][band2L]
            P1 = obsData[epoch][prn][band1C]
            P2 = obsData[epoch][prn][band2C]
            if L1 is None or L2 is None or P1 is None or P2 is None:
                continue

            freq1 = cycleSlipBandChoose[gSys][band1L]['freq']
            freq2 = cycleSlipBandChoose[gSys][band2L]['freq']
            lambdaW = cycleSlipBandChoose[gSys]['lambdaW']
            lambda1 = cycleSlipBandChoose[gSys][band1L]['lambda']
            lambda2 = cycleSlipBandChoose[gSys][band2L]['lambda']
            N_MW = L1 - L2 - (freq1 * P1 + freq2 * P2) / (freq1 + freq2) / lambdaW
            L_GF = lambda1 * L1 - lambda2 * L2
            P_GF = P2 - P1

            MW_CLIP = False
            GF_CLIP = False
            if prnEpochList == []:
                prnEpochList = [epoch]
                prn_N_MW_list = [[N_MW]]
                prn_M_MW_list = [[N_MW]]
                SIGMA_list = [[0.3]]
                L_GF_list = [[L_GF]]
                P_GF_list = [[P_GF]]
                slipList = [0]
                continue
            if (epoch - prnEpochList[-1]).total_seconds() > interval:
                prnEpochList.append(epoch)
                prn_N_MW_list.append([N_MW])
                prn_M_MW_list.append([N_MW])
                SIGMA_list = [[0.3]]
                L_GF_list.append([L_GF])
                P_GF_list.append([P_GF])
                slipList.append(0)
                continue
            
            if len(prn_N_MW_list[-1]) < 2 :
                SIGMA_I_BACK = 0.15
            else:
                SIGMA_I_BACK = SIGMA_list[-1][-1]

            N_MW_MEAN_BACK = prn_M_MW_list[-1][-1]
            N_MW_MEAN = N_MW_MEAN_BACK + (N_MW - N_MW_MEAN_BACK)/(len(prn_M_MW_list[-1]) + 1)
            SIGMA2 = SIGMA_I_BACK * SIGMA_I_BACK + ((N_MW - N_MW_MEAN_BACK) ** 2 - SIGMA_I_BACK*SIGMA_I_BACK) / (len(prn_M_MW_list[-1]) + 1)
            SIGMA = np.sqrt(SIGMA2)
            if abs(N_MW - N_MW_MEAN) >= 4 * SIGMA_I_BACK:
                MW_CLIP = True

            # GF-CHECK
            if not MW_CLIP and len(L_GF_list[-1]) > 1:
                if abs(L_GF - L_GF_list[-1][-1]) > 0.15:
                    GF_CLIP = True

            if MW_CLIP or GF_CLIP:
                prnEpochList.append(epoch)
                prn_N_MW_list.append([N_MW])
                prn_M_MW_list.append([N_MW])
                SIGMA_list.append([0.15])
                L_GF_list.append([L_GF])
                P_GF_list.append([P_GF])
                slipList.append(1)
            else:
                prnEpochList.append(epoch)
                prn_N_MW_list[-1].append(N_MW)
                prn_M_MW_list[-1].append(N_MW_MEAN)
                L_GF_list[-1].append(L_GF)
                SIGMA_list[-1].append(SIGMA)
                P_GF_list[-1].append(P_GF)
                slipList.append(0)
        prnData.append(slipList)
        prnIndex += 1

    for prn, result in zip(satList, prnData):
        if result == []:
            continue
        gnssSys = prn[0]
        if gnssSys not in slipData:
            slipData[gnssSys] = {}
        slipData[gnssSys][prn] = result
    
    return slipData


def writeSlip(slipData, slipFile):
    # slipData[gnssSys][prn]
    slipFileWrite = open(slipFile, 'w+')
    slipFileWrite.write('# PGM       : FAST\n')
    slipFileWrite.write('# Author    : Chuntao Chang\n')
    slipFileWrite.write('# Inf       : Slip\n')
    slipFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    slipFileWrite.write('#             END OF HEADER\n')
    slipFileWrite.write('\n')
    # CSR = len(mwgfData[gnssSys][prn])/sum(mwgfData[gnssSys][prn])
    satLines = ['+SAT\n']
    satLines.append('  PRN  ObsNum   Slip   O/Slip\n')
    satLines.append('  ---------------------------\n')
    for gnssSys in slipData:
        for prn in slipData[gnssSys]:
            if sum(slipData[gnssSys][prn]) == 0:
                CSR = '   NoSlip'
            else:
                CSR = '%9.2f' % (len(slipData[gnssSys][prn])/sum(slipData[gnssSys][prn]))
            line = str(prn).rjust(5) + '%8d' % len(slipData[gnssSys][prn]) + '%7d' % sum(slipData[gnssSys][prn]) + CSR + '\n'
            satLines.append(line)
    satLines.append('  ---------------------------\n')
    satLines.append('-SAT\n')
    slipFileWrite.writelines(satLines)



    
    
if __name__ == '__main__':
    from fast.com.readObs import readObs, readObsHead

    file = r'D:\Code\FAST\test\phone\18082380.23o'
    obsHead = readObsHead(file, needSatList=True)
    obsData = readObs(file, obsHead=obsHead)

    import time
    start_time = time.time()
    slipData = turboedit(obsHead, obsData)
    end_time = time.time()
    execution_time = end_time - start_time
    print("run : ", execution_time, "s")