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
        axCMC.set_ylabel(gnssSys + '_P [m]', fontsize=16)
        axCMC.grid(zorder=0) 
        axCMC.tick_params(axis='y', labelsize=13)
        cmcall = []
        for prn in cmcData[gnssSys]:
            for band in cmcData[gnssSys][prn]:
                epochList = cmcData[gnssSys][prn][band]['epoch']
                cmcList = cmcData[gnssSys][prn][band]['cmc']
                cmcall += cmcList
                axCMC.scatter(epochList, cmcList, marker='+', s=1, zorder=10, alpha=0.8)
            prnIndex += 1
        sortcmc = sorted(cmcall)
        axCMC.set_ylim(sortcmc[10], sortcmc[-10])
        if nowAxNum != gnssSysNum:
            axCMC.set_xticklabels([])
        else:
            # xfmt = mdate.DateFormatter('%dD-%H:%M')
            xfmt = mdate.DateFormatter('%dD-%HH')
            axCMC.xaxis.set_major_formatter(xfmt)
            axCMC.tick_params(axis='x', labelsize=13)
            # axCMC.tick_params(axis='x', labelsize=8)
        nowAxNum += 1


    figCMC.subplots_adjust(left=0.12, right=0.99, bottom=0.1, top=0.99)

    if self is not None:
        figCMC.canvas.draw()
        self.status.showMessage('Plot CMC completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()