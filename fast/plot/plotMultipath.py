# -*- coding: utf-8 -*-
# plotMultipath     : plot Multipath
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02

from fast.com.pub import rms
def plotMultipathBack(mpData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    # mpData[gSys][prn][band]['mp']
    if self is not None:
        self.figMP.clf()
        figMP = self.figMP
    else:
        figMP = plt.figure()
    gnssSysNum = len(mpData)
    nowAxNum = 1
    prnIndex = 0
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot MultiPath...')
        QApplication.processEvents()
    for gnssSys in mpData:
        axMP=figMP.add_subplot(gnssSysNum,1,nowAxNum)
        axMP.set_ylabel(gnssSys + ' [m]', fontdict={'size': 16})  
        axMP.grid(zorder=0) 
        axMP.tick_params(axis='y', labelsize=13)
        if nowAxNum == 1:
            axMP.set_title('Pseudorange Multipath', fontdict={'size': 16})
        bandData = {}
        for prn in mpData[gnssSys]:
            for band in mpData[gnssSys][prn]:
                epochList = mpData[gnssSys][prn][band]['epoch']
                mpList = mpData[gnssSys][prn][band]['mp']
                axMP.scatter(epochList, mpList, marker='+', s=1, zorder=10)
                if band not in bandData:
                    bandData[band] = []
                bandData[band] += mpList
            prnIndex += 1
            
        rmsLine = 'RMS:'
        for band in bandData:
            if len(bandData[band]) == 0:continue
            rmsLine += band + ' (' + '%.2f' % rms(bandData[band]) +  ') '
        axMP.text(0.02, 0.92, rmsLine,
                transform=axMP.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize=15)
        if nowAxNum != gnssSysNum:
            axMP.set_xticklabels([])
        else:
            xfmt = mdate.DateFormatter('%dD-%HH')
            axMP.xaxis.set_major_formatter(xfmt)
            axMP.tick_params(axis='x', labelsize=13)
            # axMP.tick_params(axis='x', labelsize=8)
        nowAxNum += 1


    figMP.subplots_adjust(left=0.12, right=0.99, bottom=0.04, top=0.93)

    if self is not None:
        figMP.canvas.draw()
        self.status.showMessage('Plot MultiPath completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()


def plotMultipath(mpData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    # mpData[gSys][prn][band]['mp']
    if self is not None:
        self.figMP.clf()
        figMP = self.figMP
        # self.figMP = plt.figure(figsize=(84 / 25.4, 84 / 25.4 * 1.5), dpi=300)  # 设置新的尺寸和分辨率
        # self.canvas = FigureCanvas(self.figMP)  # 如果需要,重新创建画布
    else:
        figMP = plt.figure(figsize=(84 / 25.4, 84 / 25.4 * 1.5), dpi=300)

    matplotlib.rcParams['font.family'] = 'Arial'  # 使用 Arial 无衬线字体
    matplotlib.rcParams['font.size'] = 10         # 设置字体大小为 10pt
    gnssSysNum = len(mpData)
    nowAxNum = 1
    prnIndex = 0
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot MultiPath...')
        QApplication.processEvents()
    for gnssSys in mpData:
        axMP=figMP.add_subplot(gnssSysNum,1,nowAxNum)
        axMP.set_ylabel(gnssSys + ' [m]', fontdict={'size': 10})  
        axMP.yaxis.labelpad = 0  # 单位为像素
        axMP.grid(zorder=0) 
        axMP.tick_params(axis='y', labelsize=10)
        axMP.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
        if nowAxNum == 1:
            axMP.set_title('Pseudorange Multipath', fontdict={'size': 10}, pad=1)
        bandData = {}
        for prn in mpData[gnssSys]:
            for band in mpData[gnssSys][prn]:
                epochList = mpData[gnssSys][prn][band]['epoch']
                mpList = mpData[gnssSys][prn][band]['mp']
                axMP.scatter(epochList, mpList, marker='+', s=1, zorder=10)
                if band not in bandData:
                    bandData[band] = []
                bandData[band] += mpList
            prnIndex += 1
            
        rmsLine = 'RMS:'
        bandIndex = 0
        for band in bandData:
            if len(bandData[band]) == 0:continue
            if bandIndex == 3:rmsLine += '\n         '
            rmsLine += band + ' (' + '%.2f' % rms(bandData[band]) +  ') '
            bandIndex += 1
        axMP.text(0.02, 0.92, rmsLine,
                transform=axMP.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize=10)
        
        y_min, y_max = axMP.get_ylim()
        y_min_rounded = (y_min // 5) * 5  # 向下取整到最近的 5 的倍数
        y_max_rounded = ((y_max + 4) // 5) * 5  # 向上取整到最近的 5 的倍数
        y_max = max(abs(y_max_rounded), abs(y_min_rounded))
        axMP.set_ylim(-y_max, y_max)
        if nowAxNum != gnssSysNum:
            axMP.set_xticklabels([])
        else:
            xfmt = mdate.DateFormatter('%dD-%HH')
            axMP.xaxis.set_major_formatter(xfmt)
            axMP.tick_params(axis='x', labelsize=10)
            axMP.xaxis.set_major_formatter(mdate.DateFormatter('%dD-%HH'))
        axMP.xaxis.set_major_locator(mdate.HourLocator(interval=6))
            # axMP.tick_params(axis='x', labelsize=8)
        nowAxNum += 1

    figMP.subplots_adjust(left=0.18, right=0.99, bottom=0.04, top=0.95,hspace=0.1)

    if self is not None:
        # figMP.savefig('D:\Code\FAST\manual\RUN_image\mp.png')
        figMP.canvas.draw()
        self.status.showMessage('Plot MultiPath completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()