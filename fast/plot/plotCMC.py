# -*- coding: utf-8 -*-
# plotCMC           : plot timediff code - phase
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02

from fast.com.pub import rms
def plotCMC(cmcData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    # cmcData[gSys][prn][band]['mp']
    if self is not None:
        self.figCMC.clf()
        figCMC = self.figCMC
    else:
        figCMC = plt.figure()
    gnssSysNum = len(cmcData)
    nowAxNum = 1
    prnIndex = 0
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot CMC...')
        QApplication.processEvents()
    for gnssSys in cmcData:
        axCMC=figCMC.add_subplot(gnssSysNum,1,nowAxNum)
        axCMC.set_ylabel(gnssSys + '_P [m]', fontsize='medium')
        axCMC.grid(zorder=0) 
        axCMC.tick_params(axis='y', labelsize='medium')
        cmcall = []
        bandData = {}
        for prn in cmcData[gnssSys]:
            for band in cmcData[gnssSys][prn]:
                epochList = cmcData[gnssSys][prn][band]['epoch']
                cmcList = cmcData[gnssSys][prn][band]['cmc']
                cmcall += cmcList
                axCMC.scatter(epochList, cmcList, marker='+', s=1, zorder=10, alpha=0.8)
                if band not in bandData:
                    bandData[band] = []
                bandData[band] += cmcList
            prnIndex += 1
        rmsLine = 'RMS:'
        bandIndex = 0
        for band in bandData:
            if len(bandData[band]) == 0:continue
            if bandIndex == 3:rmsLine += '\n         '
            rmsLine += band + ' (' + '%.2f' % rms(bandData[band]) +  ') '
            bandIndex += 1
        axCMC.text(0.02, 0.92, rmsLine,
                transform=axCMC.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize='medium')
        sortcmc = sorted(cmcall)
        y_min = sortcmc[-5]
        y_max = sortcmc[5]
        y_min_rounded = (y_min // 5) * 5  # 向下取整到最近的 5 的倍数
        y_max_rounded = ((y_max + 4) // 5) * 5  # 向上取整到最近的 5 的倍数
        y_max = max(abs(y_max_rounded), abs(y_min_rounded))
        if y_max < 5: y_max = 5
        axCMC.set_ylim(-y_max, y_max)
        if nowAxNum != gnssSysNum:
            axCMC.set_xticklabels([])
        else:
            # xfmt = mdate.DateFormatter('%dD-%H:%M')
            xfmt = mdate.DateFormatter('%dD-%HH')
            axCMC.xaxis.set_major_formatter(xfmt)
            axCMC.tick_params(axis='x', labelsize='medium')
            # axCMC.tick_params(axis='x', labelsize=8)
        nowAxNum += 1


    figCMC.subplots_adjust(left=0.08, right=0.99, bottom=0.04, top=0.99)

    if self is not None:
        figCMC.canvas.draw()
        self.status.showMessage('Plot CMC completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()