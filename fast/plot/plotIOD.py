# -*- coding: utf-8 -*-
# plotIOD           : plot Ionospheric delay rate
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02



def plotIOD(iodData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    # iodData[gSys][prn][band]['mp']
    if self is not None:
        self.figIOD.clf()
        figIOD = self.figIOD
    else:
        figIOD = plt.figure()
    gnssSysNum = len(iodData)
    nowAxNum = 1
    prnIndex = 0
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot IOD...')
        QApplication.processEvents()
    for gnssSys in iodData:
        axIOD=figIOD.add_subplot(gnssSysNum,1,nowAxNum)
        axIOD.set_ylabel(gnssSys + '_L [m/s]', fontsize='medium')
        axIOD.grid(zorder=0) 
        axIOD.tick_params(axis='y', labelsize='medium')

        for prn in iodData[gnssSys]:
            for band in iodData[gnssSys][prn]:
                epochList = iodData[gnssSys][prn][band]['epoch']
                iodList = iodData[gnssSys][prn][band]['iod']
                axIOD.scatter(epochList, iodList, marker='+', s=1, zorder=10, alpha=0.8)
            prnIndex += 1
        if nowAxNum != gnssSysNum:
            axIOD.set_xticklabels([])
        else:
            xfmt = mdate.DateFormatter('%dD-%HH')
            axIOD.xaxis.set_major_formatter(xfmt)
            axIOD.tick_params(axis='x', labelsize='medium')
            # axIOD.tick_params(axis='x', labelsize=8)
        nowAxNum += 1


    figIOD.subplots_adjust(left=0.12, right=0.99, bottom=0.04, top=0.96)

    if self is not None:
        figIOD.canvas.draw()
        self.status.showMessage('Plot IOD completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()