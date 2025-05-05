# -*- coding: utf-8 -*-
# plotFreq          : plot Freq for each sat in obs
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02


def plotFreq(obsHead, obsData, self = None, pngFile = None):
    import numpy as np
    import matplotlib.dates as mdate
    import matplotlib.pyplot as plt
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        self.figFreq.clf()
        self.axFreq = self.figFreq.add_subplot(111)
        axFreq = self.axFreq
        figFreq = self.figFreq
        satListInObs = [item for item in self.qcChoosePrnBox.currentText().split(',') if item != '']
    else:
        figFreq, axFreq = plt.subplots(figsize=(15, 20))
        satListInObs = obsHead['prn']

    satList = []
    obsType = obsHead['OBS TYPES']
    plotList = {}
    plotListIndex = {}
    satList = satListInObs

    satList.sort(reverse=True)
    satBZ = np.arange(len(satList))

    prnIndex = 0
    for prn in satList:
        plotList[prn] = {}
        plotListIndex[prn] = {}
        plotListIndex[prn]['index'] = prnIndex
        if prn[0] in obsType:
            freqIndex = 0
            for freq in obsType[prn[0]]:
                if 'L' in freq[0]:
                    plotList[prn][freq] = np.empty((0, 2))
                    plotListIndex[prn][freq] = freqIndex
                    freqIndex += 1
        prnIndex += 1

    freqChoose = {}
    if self is not None:
        for sys_freq in self.qcChooseBandBox.currentText().split(','):
            if sys_freq == '':
                continue
            gSys = sys_freq[0]
            if gSys not in freqChoose:
                freqChoose[gSys] = []
            freq = 'L'+sys_freq[2:]
            if freq in obsType[gSys]:
                freqChoose[gSys].append(freq)
    else:
        for gSys in obsType:
            freqChoose[gSys] = []
            for freq in obsType[gSys]:
                if 'L' == freq[0]:
                    freqChoose[gSys].append(freq)

    layerList = [0.0, 0.0, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1]


    axFreq.set_yticks(satBZ)
    axFreq.set_yticklabels(list(plotList))

    axFreq.set_ylim(-0.5,satBZ[-1]+0.5)
    axFreq.set_xlim(list(obsData)[0], list(obsData)[-1])
    if self is not None:
        axFreq.set_xlim(startdatetime, enddatetime)

    
    # if int(len(satBZ)) > 60:
    #     axFreq.tick_params(axis='y', labelsize=6)
    # elif 60 >= int(len(satBZ)) > 30:
    #     axFreq.tick_params(axis='y', labelsize=8)
    # elif 30 >= int(len(satBZ)) > 10:
    #     axFreq.tick_params(axis='y', labelsize=10)
    # else:
    #     axFreq.tick_params(axis='y', labelsize=15)
    axFreq.tick_params(axis='y', labelsize='small')

    axFreq.grid(zorder=0, alpha=0.1)

    colorList = ['orange', 'royalblue', 'tomato', 'g', 'lightpink', 'darkcyan', 'indigo', 'teal']
    markerList = ['o', 'o', '.', '.', '.', '.', '.', '.', '.', '.']
    markerSizeList = [5, 2, 2, 2, 1, 1, 1, 1, 1, 1]
    prnIndex = 0
    freqListTmp = set()
    freqData = {}

    for prn in plotList:
        if self is not None:
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Plot freq of " + prn +  " [" + barPercent + '] ' + percentage)
                QApplication.processEvents()
        gSys = prn[0]
        if gSys not in freqChoose:
            continue
        freqIndex = 0
        freqData[prn] = {}
        for freq in freqChoose[gSys]:
            freqLable = gSys + '_' + freq
            freqList = []
            epochList = []

            for epoch in obsData:
                if prn not in obsData[epoch].keys():
                    continue
                if epoch < startdatetime or epoch > enddatetime:
                    continue
                if obsData[epoch][prn][freq] is not None:
                    freqList.append(prnIndex+layerList[freqIndex])
                    epochList.append(epoch)
            
            freqData[prn][freq] = len(epochList)
            if freqLable not in freqListTmp:
                freqListTmp.add(freqLable)
                axFreq.scatter(epochList, freqList, \
                                    color=colorList[freqIndex], marker=markerList[freqIndex], \
                                        s=markerSizeList[freqIndex],zorder=10, label=freqLable, alpha=0.5)
            else:
                axFreq.scatter(epochList, freqList, \
                                    color=colorList[freqIndex], marker=markerList[freqIndex], \
                                        s=markerSizeList[freqIndex],zorder=10, alpha=0.5)
            freqIndex += 1

        prnIndex += 1

    axFreq.tick_params(axis='x', labelsize='small')

    axFreq.legend(loc='upper right', bbox_to_anchor=(1.16,1),markerscale=3)
    xfmt = mdate.DateFormatter('%dD-%H:%M')
    axFreq.xaxis.set_major_formatter(xfmt)
    figFreq.subplots_adjust(left=0.08, right=0.87, bottom=0.03, top=0.99)
    plt.tight_layout()  # 自动调整布局
    if self is not None:
        figFreq.canvas.draw()
        self.status.showMessage("Plot freq Finished [" + 20*'=' + '] ' + "100% ")
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()
    return freqData

if __name__ == '__main__':
    from fast.com.readObs import readObs, readObsHead

    file = r'D:\Code\FAST\test\de012660.23o'
    obsHead = readObsHead(file, needSatList=True)
    obsData = readObs(file, obsHead=obsHead)
    
    import time
    start_time = time.time()
    plotFreq(obsHead, obsData, pngFile=r'D:\Code\FAST\test\abpo0010.png')
    end_time = time.time()
    execution_time = end_time - start_time
    print("run : ", execution_time, "s")

