
def plotCnrAll(obsHead, obsData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    cnrData = {}
    satList = obsHead['prn']
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        satList = [item for item in self.qcChoosePrnBox.currentText().split(',') if item != '']
        nowSys = self.qcChooseSysBox.currentText()
        gnssSystem = []
        for gnssSys in nowSys.split(','):
            if '' != gnssSys:
                gnssSystem.append(gnssSys)
        bandChoose = {}
        for sys_band in self.qcChooseBandBox.currentText().split(','):
            if sys_band == '':
                continue
            nowSys = sys_band[0]
            if nowSys not in bandChoose:
                bandChoose[nowSys] = []
            bandChoose[nowSys].append('S'+sys_band[2:])

    for epoch in obsData:
        if epoch < startdatetime or epoch > enddatetime:
            continue
        for prn in obsData[epoch]:
            gnssSys = prn[0]
            if self is not None:
                if gnssSys not in gnssSystem:
                    continue

            if gnssSys not in cnrData:
                cnrData[gnssSys] = {}

            if prn not in cnrData[gnssSys]:
                cnrData[gnssSys][prn] = {}
            for band in obsData[epoch][prn]:
                if 'S' != band[0]:
                    continue
                if obsData[epoch][prn][band] == None:
                    continue
                if band not in cnrData[gnssSys][prn]:
                    cnrData[gnssSys][prn][band] = {}
                cnrData[gnssSys][prn][band][epoch] = obsData[epoch][prn][band]
    
    gnssSysNum = len(cnrData)
    
    if self is not None:
        self.figcnr.clf()
        figcnr = self.figcnr
    else:
        figcnr = plt.figure()

    nowAxNum = 1
    prnIndex = 0
    for gnssSys in cnrData:
        axcnr=figcnr.add_subplot(gnssSysNum,1,nowAxNum)
        axcnr.set_ylabel(gnssSys + ' [dBHz]', fontsize=16)
        axcnr.grid(zorder=0)
        axcnr.tick_params(axis='y', labelsize=13)

        for prn in cnrData[gnssSys]:

            if self is not None:
                if prn not in satList:
                    continue
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage("Plot cnr of " + prn +  "  [" + barPercent + '] ' + percentage)
                QApplication.processEvents()
            for band in cnrData[gnssSys][prn]:
                if self is not None:
                    if gnssSys not in bandChoose:
                        continue
                    if band not in bandChoose[gnssSys]:
                        continue
                epoch_list = list(cnrData[gnssSys][prn][band])
                cnrList = []
                for epoch in cnrData[gnssSys][prn][band]:cnrList.append(cnrData[gnssSys][prn][band][epoch])
                axcnr.scatter(epoch_list, cnrList, marker='+', s=1, zorder=10, alpha=0.3)
            prnIndex += 1
        if nowAxNum != gnssSysNum:
            axcnr.set_xticklabels([])
        else:
            # xfmt = mdate.DateFormatter('%dD-%H:%M')
            xfmt = mdate.DateFormatter('%dD-%HH')
            
            axcnr.xaxis.set_major_formatter(xfmt)
            axcnr.tick_params(axis='x', labelsize=13)
            # axcnr.tick_params(axis='x', labelsize=8)
        nowAxNum += 1
    
    figcnr.subplots_adjust(left=0.08, right=0.99, bottom=0.03, top=0.99)

    if self is not None:
        figcnr.canvas.draw()
        self.status.showMessage("Plot cnr Completed [" + 20*'=' + '] ' + "100% ")
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile)
        else:
            plt.show()
    return cnrData

def plotCnrBack(obsHead, obsData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    import numpy as np
    import seaborn as sns
    cnrData = {}
    satList = obsHead['prn']
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        satList = [item for item in self.qcChoosePrnBox.currentText().split(',') if item != '']
        nowSys = self.qcChooseSysBox.currentText()
        gnssSystem = []
        for gnssSys in nowSys.split(','):
            if '' != gnssSys:
                gnssSystem.append(gnssSys)
        bandChoose = {}
        for sys_band in self.qcChooseBandBox.currentText().split(','):
            if sys_band == '':
                continue
            nowSys = sys_band[0]
            if nowSys not in bandChoose:
                bandChoose[nowSys] = []
            bandChoose[nowSys].append('S'+sys_band[2:])
    # sns.set_theme(style="whitegrid", palette="pastel")
    for epoch in obsData:
        if epoch < startdatetime or epoch > enddatetime:
            continue
        for prn in obsData[epoch]:
            gnssSys = prn[0]
            if self is not None:
                if gnssSys not in gnssSystem:
                    continue

            if gnssSys not in cnrData:
                cnrData[gnssSys] = {}

            if prn not in cnrData[gnssSys]:
                cnrData[gnssSys][prn] = {}
            for band in obsData[epoch][prn]:
                if 'S' != band[0]:
                    continue
                if obsData[epoch][prn][band] == None:
                    continue
                if band not in cnrData[gnssSys][prn]:
                    cnrData[gnssSys][prn][band] = {}
                cnrData[gnssSys][prn][band][epoch] = obsData[epoch][prn][band]
    
    gnssSysNum = len(cnrData)
    
    if self is not None:
        self.figcnr.clf()
        figcnr = self.figcnr
    else:
        figcnr = plt.figure()

    nowAxNum = 1
    prnIndex = 0
    for gnssSys in cnrData:
        axcnr = figcnr.add_subplot(gnssSysNum, 1, nowAxNum)
        axcnr.set_ylabel(f'{gnssSys} [dBHz]', fontsize=16)
        axcnr.grid(zorder=0)
        axcnr.tick_params(axis='y', labelsize=13)

        if nowAxNum == 1:
            axcnr.set_title('CNR', fontdict={'size': 16})
        allCnrDict = {}
        for prn in cnrData[gnssSys]:
            if self is not None:
                if prn not in satList:
                    continue
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage(f"Plot cnr of {prn}  [{barPercent}] {percentage}")
                QApplication.processEvents()

            for band in cnrData[gnssSys][prn]:
                if self is not None:
                    if gnssSys not in bandChoose:
                        continue
                    if band not in bandChoose[gnssSys]:
                        continue
                cnrList = []
                for epoch in cnrData[gnssSys][prn][band]:
                    cnrList.append(cnrData[gnssSys][prn][band][epoch])
                if band not in allCnrDict:
                    allCnrDict[band] = []
                allCnrDict[band] += cnrList
            prnIndex += 1

        # 提取数据
        values = list(allCnrDict.values())
        labels = list(allCnrDict.keys())
        for band in allCnrDict:
            print(band, np.mean(allCnrDict[band]))

        # 绘制箱线图
        bp = axcnr.boxplot(values, positions=range(1, len(values) + 1))
        for i, flier in enumerate(bp['fliers']):
            flier.set(marker='o', color='blue', alpha=0.2)
        # 设置 x 轴刻度标签
        axcnr.set_xticks(range(1, len(labels) + 1))
        axcnr.set_xticklabels(labels, fontsize=12)

        # 添加图例（只显示一次均值标签）
        handles, labels = axcnr.get_legend_handles_labels()
        if handles:
            axcnr.legend(handles, labels, loc='upper right', fontsize=12)

        # 调整纵轴范围为10的倍数
        current_min, current_max = axcnr.get_ylim()
        lower_bound = np.floor(current_min / 10) * 10
        upper_bound = np.ceil(current_max / 10) * 10
        axcnr.set_ylim(lower_bound, upper_bound)

        nowAxNum += 1

    # 调整子图间距
    figcnr.subplots_adjust(left=0.08, right=0.99, bottom=0.03, top=0.99, hspace=0.3)

    if self is not None:
        figcnr.canvas.draw()
        self.status.showMessage("Plot cnr Completed [" + 20 * '=' + '] ' + "100% ")
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    return cnrData




def plotCnr(obsHead, obsData, self = None, pngFile = None):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    import numpy as np
    import seaborn as sns
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    cnrData = {}
    satList = obsHead['prn']
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        satList = [item for item in self.qcChoosePrnBox.currentText().split(',') if item != '']
        nowSys = self.qcChooseSysBox.currentText()
        gnssSystem = []
        for gnssSys in nowSys.split(','):
            if '' != gnssSys:
                gnssSystem.append(gnssSys)
        bandChoose = {}
        for sys_band in self.qcChooseBandBox.currentText().split(','):
            if sys_band == '':
                continue
            nowSys = sys_band[0]
            if nowSys not in bandChoose:
                bandChoose[nowSys] = []
            bandChoose[nowSys].append('S'+sys_band[2:])
    # sns.set_theme(style="whitegrid", palette="pastel")
    for epoch in obsData:
        if epoch < startdatetime or epoch > enddatetime:
            continue
        for prn in obsData[epoch]:
            gnssSys = prn[0]
            if self is not None:
                if gnssSys not in gnssSystem:
                    continue

            if gnssSys not in cnrData:
                cnrData[gnssSys] = {}

            if prn not in cnrData[gnssSys]:
                cnrData[gnssSys][prn] = {}
            for band in obsData[epoch][prn]:
                if 'S' != band[0]:
                    continue
                if obsData[epoch][prn][band] == None:
                    continue
                if band not in cnrData[gnssSys][prn]:
                    cnrData[gnssSys][prn][band] = {}
                cnrData[gnssSys][prn][band][epoch] = obsData[epoch][prn][band]
    
    gnssSysNum = len(cnrData)
    
    if self is not None:
        self.figcnr.clf()
        figcnr = self.figcnr
        # self.figcnr = plt.figure(figsize=(84 / 25.4, 84 / 25.4 * 1.5), dpi=300)  # 设置新的尺寸和分辨率
        # self.canvas = FigureCanvas(self.figcnr)  # 如果需要，重新创建画布
    else:
        figcnr = plt.figure()

    matplotlib.rcParams['font.family'] = 'Arial'  # 使用 Arial 无衬线字体
    matplotlib.rcParams['font.size'] = 10         # 设置字体大小为 10pt
    nowAxNum = 1
    prnIndex = 0
    for gnssSys in cnrData:
        axcnr = figcnr.add_subplot(gnssSysNum, 1, nowAxNum)
        axcnr.set_ylabel(f'{gnssSys} [dBHz]', fontsize=10)
        axcnr.yaxis.labelpad = 0  # 单位为像素
        axcnr.grid(zorder=0)
        axcnr.tick_params(axis='y', labelsize=10)


        if nowAxNum == 1:
            axcnr.set_title('CNR', fontdict={'size': 10}, pad=1)
        allCnrDict = {}
        for prn in cnrData[gnssSys]:
            if self is not None:
                if prn not in satList:
                    continue
            if prnIndex / len(satList) * 100 - int(prnIndex / len(satList) * 100) < 1:
                completed = int(20 * prnIndex / len(satList)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(prnIndex / len(satList)) * 100:.2f}%'
                self.status.showMessage(f"Plot cnr of {prn}  [{barPercent}] {percentage}")
                QApplication.processEvents()

            for band in cnrData[gnssSys][prn]:
                if self is not None:
                    if gnssSys not in bandChoose:
                        continue
                    if band not in bandChoose[gnssSys]:
                        continue
                cnrList = []
                for epoch in cnrData[gnssSys][prn][band]:
                    cnrList.append(cnrData[gnssSys][prn][band][epoch])
                if band not in allCnrDict:
                    allCnrDict[band] = []
                allCnrDict[band] += cnrList
            prnIndex += 1

        # 提取数据
        values = list(allCnrDict.values())
        labels = list(allCnrDict.keys())
        for band in allCnrDict:
            print(band, np.mean(allCnrDict[band]))

        # 绘制箱线图
        bp = axcnr.boxplot(values, positions=range(1, len(values) + 1))
        for i, flier in enumerate(bp['fliers']):
            flier.set(marker='o', 
                        # markerfacecolor='red',  # 填充颜色
                        markeredgecolor='red',  # 边缘颜色
                      alpha=0.3,
                      markersize=4)
        # 设置 x 轴刻度标签
        axcnr.set_xticks(range(1, len(labels) + 1))
        axcnr.set_xticklabels(labels, fontsize=10)

        # 添加图例（只显示一次均值标签）
        handles, labels = axcnr.get_legend_handles_labels()
        if handles:
            axcnr.legend(handles, labels, loc='upper right', fontsize=10)

        # 调整纵轴范围为10的倍数
        current_min, current_max = axcnr.get_ylim()
        lower_bound = np.floor(current_min / 10) * 10
        upper_bound = np.ceil(current_max / 10) * 10
        axcnr.set_ylim(lower_bound, upper_bound)

        nowAxNum += 1

        axcnr.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
        y_min, y_max = axcnr.get_ylim()
        y_max_rounded = ((y_max + 0) // 10) * 10  # 向上取整到最近的 5 的倍数
        axcnr.set_ylim(0, 60)
    # 调整子图间距
    figcnr.subplots_adjust(left=0.15, right=0.99, bottom=0.04, top=0.95)

    if self is not None:
        # figcnr.savefig('D:\Code\FAST\manual\RUN_image\snr.png')
        figcnr.canvas.draw()
        self.status.showMessage("Plot cnr Completed [" + 20 * '=' + '] ' + "100% ")
        QApplication.processEvents()
    else:
        if pngFile is not None:
            plt.savefig(pngFile, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    return cnrData
# from fast.com.readObs import readObs3
# plotcnr(readObs3(r'D:\Code\gnssbox\gnssbox\test\posTest\test\abpo1280_02.23o'))
# from fast.com.readObs import readObs3
# plotcnr(readObs3(r'D:\Code\gnssbox\gnssbox\test\posTest\test\abpo1280_02.23o'))