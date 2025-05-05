# -*- coding: utf-8 -*-
# plotLnoise        : plot Phase Noise
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02


def plotPhaseNoise(PhaseNoiseData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    from fast.com.pub import rms
    if self is not None:
        self.figPhaseNoise.clf()
        figPhaseNoise = self.figPhaseNoise
    else:
        figPhaseNoise = plt.figure()
    gnssSysNum = len(PhaseNoiseData)
    nowAxNum = 1
    prnIndex = 0
    
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot PhaseNoise...')
        QApplication.processEvents()
    for gnssSys in PhaseNoiseData:
        axPhaseNoise=figPhaseNoise.add_subplot(gnssSysNum,1,nowAxNum)
        # if nowAxNum == 1:
        #     axPhaseNoise.set_title('Phase Noise', fontdict={'size': 18})
        axPhaseNoise.set_ylabel(gnssSys + ' [cm]', fontsize='medium')
        axPhaseNoise.grid(zorder=0) 
        axPhaseNoise.tick_params(axis='y', labelsize='medium')
        bandData = {}
        for prn in PhaseNoiseData[gnssSys]:
            for band in PhaseNoiseData[gnssSys][prn]:
                epochList = PhaseNoiseData[gnssSys][prn][band]['epoch']
                PhaseNoiseList = PhaseNoiseData[gnssSys][prn][band]['phaseNoise']
                PhaseNoiseList = [x * 100.0 for x in PhaseNoiseList]
                axPhaseNoise.scatter(epochList, PhaseNoiseList, marker='+', s=1, zorder=10, alpha=0.8)
                if band not in bandData:
                    bandData[band] = []
                bandData[band] += PhaseNoiseList
            prnIndex += 1
        rmsLine = 'RMS:'
        for band in bandData:
            if len(bandData[band]) == 0:continue
            rmsLine += 'L' + band[1:] + ' (' + '%.2f' % rms(bandData[band]) +  ') '
        axPhaseNoise.text(0.02, 0.92, rmsLine,
                transform=axPhaseNoise.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize='medium')
        if nowAxNum != gnssSysNum:
            axPhaseNoise.set_xticklabels([])
        else:
            xfmt = mdate.DateFormatter('%dD-%HH')
            axPhaseNoise.xaxis.set_major_formatter(xfmt)
            axPhaseNoise.tick_params(axis='x', labelsize='medium')
        nowAxNum += 1


    figPhaseNoise.subplots_adjust(left=0.12, right=0.99, bottom=0.04, top=0.93)
    if self is not None:
        figPhaseNoise.canvas.draw()
        self.status.showMessage('Plot PhaseNoise completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()


def plotPhaseNoisePaper(PhaseNoiseData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib
    from fast.com.pub import rms
    if self is not None:
        self.figPhaseNoise.clf()
        figPhaseNoise = self.figPhaseNoise
        self.figPhaseNoise = plt.figure(figsize=(84 / 25.4, 84 / 25.4 * 1.5), dpi=300)  # 设置新的尺寸和分辨率
        self.canvas = FigureCanvas(self.figPhaseNoise)  # 如果需要,重新创建画布
    else:
        figPhaseNoise = plt.figure()
    gnssSysNum = len(PhaseNoiseData)
    nowAxNum = 1
    prnIndex = 0
    
    matplotlib.rcParams['font.family'] = 'Arial'  # 使用 Arial 无衬线字体
    matplotlib.rcParams['font.size'] = 10         # 设置字体大小为 10pt

    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        self.status.showMessage('Plot PhaseNoise...')
        QApplication.processEvents()
    for gnssSys in PhaseNoiseData:
        axPhaseNoise=figPhaseNoise.add_subplot(gnssSysNum,1,nowAxNum)
        if nowAxNum == 1:
            axPhaseNoise.set_title('Phase Noise', fontdict={'size': 10}, pad=1)
        axPhaseNoise.set_ylabel(gnssSys + ' [cm]', fontdict={'size': 10})  
        axPhaseNoise.yaxis.labelpad = 0  # 单位为像素
        axPhaseNoise.grid(zorder=0) 
        axPhaseNoise.tick_params(axis='y', labelsize=10)
        axPhaseNoise.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
        bandData = {}
        for prn in PhaseNoiseData[gnssSys]:
            for band in PhaseNoiseData[gnssSys][prn]:
                epochList = PhaseNoiseData[gnssSys][prn][band]['epoch']
                PhaseNoiseList = PhaseNoiseData[gnssSys][prn][band]['phaseNoise']
                PhaseNoiseList = [x * 100.0 for x in PhaseNoiseList]
                axPhaseNoise.scatter(epochList, PhaseNoiseList, marker='+', s=1, zorder=10, alpha=0.8)
                if band not in bandData:
                    bandData[band] = []
                bandData[band] += PhaseNoiseList
            prnIndex += 1
        rmsLine = 'RMS:'
        bandIndex = 0
        for band in bandData:
            if len(bandData[band]) == 0:continue
            if bandIndex == 3:rmsLine += '\n         '
            rmsLine += 'L' + band[1:] + ' (' + '%.2f' % rms(bandData[band]) +  ') '
            bandIndex += 1
        axPhaseNoise.text(0.02, 0.92, rmsLine,
                transform=axPhaseNoise.transAxes, verticalalignment='top',
                horizontalalignment='left', color='black',
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4'),
                zorder=30, fontsize=10)
        y_min, y_max = axPhaseNoise.get_ylim()
        y_min_rounded = (y_min // 2) * 2  # 向下取整到最近的 5 的倍数
        y_max_rounded = ((y_max + 1) // 2) * 2  # 向上取整到最近的 5 的倍数
        y_max = max(abs(y_max_rounded), abs(y_min_rounded))
        axPhaseNoise.set_ylim(-y_max, y_max)

        if nowAxNum != gnssSysNum:
            axPhaseNoise.set_xticklabels([])
        else:
            xfmt = mdate.DateFormatter('%dD-%HH')
            axPhaseNoise.xaxis.set_major_formatter(xfmt)
            axPhaseNoise.tick_params(axis='x', labelsize=10)
        nowAxNum += 1
        axPhaseNoise.xaxis.set_major_locator(mdate.HourLocator(interval=6))


    figPhaseNoise.subplots_adjust(left=0.18, right=0.99, bottom=0.04, top=0.93,hspace=0.1)

    if self is not None:
        # figPhaseNoise.savefig('D:\Code\FAST\manual\RUN_image\phase.png')
        figPhaseNoise.canvas.draw()
        self.status.showMessage('Plot PhaseNoise completed.')
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()
