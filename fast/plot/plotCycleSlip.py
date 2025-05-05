# -*- coding: utf-8 -*-
# plotCycleSlip     : plot CycleSlip
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02


def plotCycleSlip(mwgfData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot Slip...')
        QApplication.processEvents()
        self.figCycleSlip.clf()
        figCycleSlip = self.figCycleSlip
    else:
        figCycleSlip = plt.figure()
    plt.subplots_adjust(wspace=1, hspace=1)
    gnssSysNum = len(mwgfData)
    nowAxNum = 1
    for gnssSys in mwgfData:
        axcnr=figCycleSlip.add_subplot(gnssSysNum,1,nowAxNum)
        axcnr.set_ylabel(gnssSys + '_CSR')
        axcnr.grid(zorder=0) 
        axcnr.tick_params(axis='y', labelsize=10)
        prnNum = 1
        X = []
        X_PRN = []
        CSR_LIST = []
        for prn in mwgfData[gnssSys]:
            if sum(mwgfData[gnssSys][prn]) == 0:
                CSR = 0
            else:
                CSR = len(mwgfData[gnssSys][prn])/sum(mwgfData[gnssSys][prn])
            CSR_LIST.append(CSR)
            prnNum += 1
            X.append(prnNum)
            X_PRN.append(prn)

        axcnr.bar(X, CSR_LIST, width=0.5, color = 'tomato', zorder=10)
        axcnr.set_xticks(X, X_PRN)
        axcnr.tick_params(axis='x', labelsize=10,labelrotation= 90)
        nowAxNum += 1
    figCycleSlip.subplots_adjust(hspace=0.35, wspace=0.5)
    figCycleSlip.subplots_adjust(left=0.12, right=0.99, bottom=0.1, top=0.99)
    plt.tight_layout()
    if self is not None:
        figCycleSlip.canvas.draw()
        self.status.showMessage('Plot Slip completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()