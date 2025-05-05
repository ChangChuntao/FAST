# -*- coding: utf-8 -*-
# plotSatNum        : plot SatNum
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2024.07.01 - Version 3.00.02

def plotSatNum(obsData, self = None, pngFile=None, gnssSystem=['G', 'C', 'R', 'E', 'L', 'S', 'J', '0', 'W', 'ALL']):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    # from gnssbox.lib.pub import printPanda
    # printPanda('plot sat num -> ' + pngFile)
    if pngFile is not None:
        plt.switch_backend('agg')
    if self is not None:
        from PyQt5.QtWidgets import QApplication
        startdatetime = self.qcStartDateTimeEdit.dateTime().toPyDateTime()
        enddatetime = self.qcEndDateTimeEdit.dateTime().toPyDateTime()
        QApplication.processEvents()
        nowSys = self.qcChooseSysBox.currentText()
        gnssSystem = []
        for gnssSys in nowSys.split(','):
            if '' != gnssSys:
                gnssSystem.append(gnssSys)
        gnssSystem.append('ALL')
        self.status.showMessage('Plot SatNum...')
        QApplication.processEvents()
    epochList = []
    gnum = []
    cnum = []
    rnum = []
    enum = []
    lnum = []
    snum = []
    jnum = []
    wnum = []
    allnum = []
    addgprnNum = 0
    addcprnNum = 0
    addrprnNum = 0
    addeprnNum = 0
    addlprnNum = 0
    addsprnNum = 0
    addjprnNum = 0
    addwprnNum = 0
    addallprnNum = 0
    outSatNum = []
    satNumData = {}
    satNumData['stat'] = {}
    for gSys in gnssSystem:
        satNumData['stat'][gSys] = {}
        satNumData['stat'][gSys]['AVE'] = 0
        satNumData['stat'][gSys]['MIN'] = 0
        satNumData['stat'][gSys]['MAX'] = 0
    satNumData['data'] = {}
    interval = (list(obsData)[1] - list(obsData)[0]).total_seconds()
    backEp = list(obsData)[0]
    for epIndex in range(len(obsData)):
        ep = list(obsData)[epIndex]
        
        if ep < startdatetime or ep > enddatetime:
            continue
        satNumData['data'][ep] = {}
        for gSys in gnssSystem:
            satNumData['data'][ep][gSys] = 0
        gprnNum = 0
        cprnNum = 0
        rprnNum = 0
        eprnNum = 0
        lprnNum = 0
        sprnNum = 0
        jprnNum = 0
        wprnNum = 0
        allprnNum = 0
        for satPrn in obsData[ep]:
            if 'ALL' in gnssSystem:
                allprnNum += 1
                addallprnNum += 1
                satNumData['data'][ep]['ALL'] += 1
            if 'C' in satPrn and 'C' in gnssSystem:
                cprnNum += 1
                addcprnNum += 1
                satNumData['data'][ep]['C'] += 1
            if 'G' in satPrn and 'G' in gnssSystem:
                gprnNum += 1
                addgprnNum += 1
                satNumData['data'][ep]['G'] += 1
            if 'R' in satPrn and 'R' in gnssSystem:
                rprnNum += 1
                addrprnNum += 1
                satNumData['data'][ep]['R'] += 1
            if 'E' in satPrn and 'E' in gnssSystem:
                eprnNum += 1
                addeprnNum += 1
                satNumData['data'][ep]['E'] += 1
            if 'L' in satPrn and 'L' in gnssSystem:
                lprnNum += 1
                addlprnNum += 1
                satNumData['data'][ep]['L'] += 1
            if 'W' in satPrn and 'W' in gnssSystem:
                wprnNum += 1
                addwprnNum += 1
                satNumData['data'][ep]['W'] += 1
            if 'S' in satPrn and 'S' in gnssSystem:
                sprnNum += 1
                addsprnNum += 1
                satNumData['data'][ep]['S'] += 1
            if 'J' in satPrn and 'J' in gnssSystem:
                jprnNum += 1
                addjprnNum += 1
                satNumData['data'][ep]['J'] += 1
        if (ep - backEp).total_seconds() <= interval * 2:
            epochList.append(ep)
            cnum.append(cprnNum)
            gnum.append(gprnNum)
            rnum.append(rprnNum)
            enum.append(eprnNum)
            lnum.append(lprnNum)
            snum.append(sprnNum)
            jnum.append(jprnNum)
            wnum.append(wprnNum)
            allnum.append(allprnNum)
            outSatNum.append(allprnNum)
        else:
            epochList.append(backEp)
            cnum.append(0)
            gnum.append(0)
            rnum.append(0)
            enum.append(0)
            lnum.append(0)
            snum.append(0)
            jnum.append(0)
            wnum.append(0)
            allnum.append(0)
            epochList.append(ep)
            cnum.append(0)
            gnum.append(0)
            rnum.append(0)
            enum.append(0)
            lnum.append(0)
            snum.append(0)
            jnum.append(0)
            wnum.append(0)
            allnum.append(0)
            epochList.append(ep)
            cnum.append(cprnNum)
            gnum.append(gprnNum)
            rnum.append(rprnNum)
            enum.append(eprnNum)
            lnum.append(lprnNum)
            snum.append(sprnNum)
            jnum.append(jprnNum)
            wnum.append(wprnNum)
            allnum.append(allprnNum)
        backEp = ep
    if self is not None:
        self.figsatnum.clf()
        self.axsatnum = self.figsatnum.add_subplot(111)
        figsatnum = self.figsatnum
        axsatnum = self.axsatnum
    else:
        figsatnum, axsatnum = plt.subplots(figsize=(12, 5))
    if 'ALL' in gnssSystem and addallprnNum != 0:

        axsatnum.plot(epochList, allnum, linewidth=1.5, label="AVE: " + '%.1f' % (sum(allnum) / len(allnum)) + ' MIN: ' + str(min(allnum)) + ' MAX: ' + str(max(allnum)), zorder=20)
        satNumData['stat']['ALL'] = {}
        satNumData['stat']['ALL']['AVE'] = sum(allnum) / len(allnum)
        satNumData['stat']['ALL']['MIN'] = min(allnum)
        satNumData['stat']['ALL']['MAX'] = max(allnum)

    if 'C' in gnssSystem and addcprnNum != 0:
        axsatnum.plot(epochList, cnum, linewidth=1.5, label="C AVE: " + '%.1f' % (sum(cnum) / len(cnum)) + ' MIN: ' + str(min(cnum)) + ' MAX: ' + str(max(cnum)), zorder=20)
        satNumData['stat']['C'] = {}
        satNumData['stat']['C']['AVE'] = sum(cnum) / len(cnum)
        satNumData['stat']['C']['MIN'] = min(cnum)
        satNumData['stat']['C']['MAX'] = max(cnum)
        
    if 'G' in gnssSystem and addgprnNum != 0:
        axsatnum.plot(epochList, gnum, linewidth=1.5, label="G AVE: " + '%.1f' % (sum(gnum) / len(gnum)) + ' MIN: ' + str(min(gnum)) + ' MAX: ' + str(max(gnum)), zorder=20)
        satNumData['stat']['G'] = {}
        satNumData['stat']['G']['AVE'] = sum(gnum) / len(gnum)
        satNumData['stat']['G']['MIN'] = min(gnum)
        satNumData['stat']['G']['MAX'] = max(gnum)

    if 'R' in gnssSystem and addrprnNum != 0:
        axsatnum.plot(epochList, rnum, linewidth=1.5, label="R AVE: " + '%.1f' % (sum(rnum) / len(rnum)) + ' MIN: ' + str(min(rnum)) + ' MAX: ' + str(max(rnum)), zorder=20)
        satNumData['stat']['R'] = {}
        satNumData['stat']['R']['AVE'] = sum(rnum) / len(rnum)
        satNumData['stat']['R']['MIN'] = min(rnum)
        satNumData['stat']['R']['MAX'] = max(rnum)

    if 'E' in gnssSystem and addeprnNum != 0:
        axsatnum.plot(epochList, enum, linewidth=1.5, label="E AVE: " + '%.1f' % (sum(enum) / len(enum)) + ' MIN: ' + str(min(enum)) + ' MAX: ' + str(max(enum)), zorder=20)
        satNumData['stat']['E'] = {}
        satNumData['stat']['E']['AVE'] = sum(enum) / len(enum)
        satNumData['stat']['E']['MIN'] = min(enum)
        satNumData['stat']['E']['MAX'] = max(enum)

    if 'L' in gnssSystem and addlprnNum != 0:
        axsatnum.plot(epochList, lnum, linewidth=1.5, label="L AVE: " + '%.1f' % (sum(lnum) / len(lnum)) + ' MIN: ' + str(min(lnum)) + ' MAX: ' + str(max(lnum)), zorder=20)
        satNumData['stat']['L'] = {}
        satNumData['stat']['L']['AVE'] = sum(lnum) / len(lnum)
        satNumData['stat']['L']['MIN'] = min(lnum)
        satNumData['stat']['L']['MAX'] = max(lnum)

    if 'S' in gnssSystem and addsprnNum != 0:
        axsatnum.plot(epochList, snum, linewidth=1.5, label="S AVE: " + '%.1f' % (sum(snum) / len(snum)) + ' MIN: ' + str(min(snum)) + ' MAX: ' + str(max(snum)), zorder=20)
        satNumData['stat']['S'] = {}
        satNumData['stat']['S']['AVE'] = sum(snum) / len(snum)
        satNumData['stat']['S']['MIN'] = min(snum)
        satNumData['stat']['S']['MAX'] = max(snum)

    if 'J' in gnssSystem and addjprnNum != 0:
        axsatnum.plot(epochList, jnum, linewidth=1.5, label="J AVE: " + '%.1f' % (sum(jnum) / len(jnum)) + ' MIN: ' + str(min(jnum)) + ' MAX: ' + str(max(jnum)), zorder=20)
        satNumData['stat']['J'] = {}
        satNumData['stat']['J']['AVE'] = sum(jnum) / len(jnum)
        satNumData['stat']['J']['MIN'] = min(jnum)
        satNumData['stat']['J']['MAX'] = max(jnum)

    if 'W' in gnssSystem and addwprnNum != 0:
        axsatnum.plot(epochList, wnum, linewidth=1.5, label="W AVE: " + '%.1f' % (sum(wnum) / len(wnum)) + ' MIN: ' + str(min(wnum)) + ' MAX: ' + str(max(wnum)), zorder=20)
        satNumData['stat']['W'] = {}
        satNumData['stat']['W']['AVE'] = sum(wnum) / len(wnum)
        satNumData['stat']['W']['MIN'] = min(wnum)
        satNumData['stat']['W']['MAX'] = max(wnum)


    # axsatnum.set_xlabel('Time', fontsize=13)
    axsatnum.set_ylabel('Number Of Sat', fontsize='medium')
    axsatnum.legend(loc="best")
    
    xfmt = mdate.DateFormatter('%dD-%H:%M')
    # xfmt = mdate.DateFormatter('%dD-%HH')
    axsatnum.xaxis.set_major_formatter(xfmt)
    axsatnum.tick_params(axis='x', labelsize='small')
    axsatnum.tick_params(axis='y', labelsize='medium')
    axsatnum.grid(zorder=10)

    figsatnum.subplots_adjust(left=0.08, right=0.99, bottom=0.03, top=0.99)
    if self is not None:
        figsatnum.canvas.draw()
        self.status.showMessage('Plot SatNum completed.')
        QApplication.processEvents()
    if pngFile is not None:
        figsatnum.savefig(pngFile)
    return satNumData


if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) == 3:
        rnxFile = args[1]
        pngFile = args[2]
        plotSatNum(rnxFile, pngFile)