


def plotHighOrderDiff(highOrderDiffData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    # highOrderDiffData[gSys][prn][band]['mp']
    if self is not None:
        self.fighighorder.clf()
        fighighorder = self.fighighorder
    else:
        fighighorder = plt.figure()
    gnssSysNum = len(highOrderDiffData)
    nowAxNum = 1
    prnIndex = 0
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot highOrderDiff...')
        QApplication.processEvents()
    print(list(highOrderDiffData))
    for gnssSys in highOrderDiffData:
        print(list(highOrderDiffData[gnssSys]))
        axHOD=fighighorder.add_subplot(gnssSysNum,1,nowAxNum)
        axHOD.set_ylabel(gnssSys + '_L [m]')
        axHOD.grid(zorder=0) 
        axHOD.tick_params(axis='y', labelsize=10)

        for prn in highOrderDiffData[gnssSys]:
            for band in highOrderDiffData[gnssSys][prn]:
                
                epochList = highOrderDiffData[gnssSys][prn][band]['epoch']
                highList = highOrderDiffData[gnssSys][prn][band]['highOrder']
                # print(band, highList[:5])

                axHOD.scatter(epochList, highList, marker='+', s=1, zorder=10, alpha=0.8)
            prnIndex += 1
        if nowAxNum != gnssSysNum:
            axHOD.set_xticklabels([])
        else:
            xfmt = mdate.DateFormatter('%dD-%H:%M')
            axHOD.xaxis.set_major_formatter(xfmt)
            axHOD.tick_params(axis='x', labelsize=10)
            # axHOD.tick_params(axis='x', labelsize=8)
        nowAxNum += 1


    fighighorder.subplots_adjust(left=0.12, right=0.99, bottom=0.1, top=0.99)

    if self is not None:
        fighighorder.canvas.draw()
        self.status.showMessage('Plot highOrderDiff completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()

if __name__ == '__main__':
    from fast.com.readObs import readObs, readObsHead
    from fast.qc.highOrderDiff import getObsHighOrderDiff

    file = r'test\unsa0010.23o'
    obsHead = readObsHead(file, needSatList=True)
    obsData = readObs(file, obsHead=obsHead)

    import time
    start_time = time.time()
    h = getObsHighOrderDiff(obsHead, obsData)
    plotHighOrderDiff(h)
    end_time = time.time()
    execution_time = end_time - start_time
    print("run : ", execution_time, "s")
