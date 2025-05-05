# -*- coding: utf-8 -*-
# qtSite            : pyqt5 for Station selection module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02

from PyQt5.QtCore import QThread, QTimer
import os
from functools import partial
from PyQt5.QtWidgets import QFileDialog, QApplication
from os.path import expanduser
from PyQt5.QtWidgets import QMessageBox
from fast.com.writeSiteInf import writeSiteInf, writeSiteList
from PyQt5.QtCore import QObject, pyqtSignal
from fast.plot.plotSite import plotSite
from fast.com.readSiteinfo import readSiteInf, readIgsSiteList
from fast.site.thinning import thinning
from fast.com.mgexSite import readMegxSiteInf
from fast.com.pub import is_number
from fast.com.writeSiteInf import writeSiteInf


class runSiteWorker(QObject):
    finished = pyqtSignal(object)
    def __init__(self, mainSelf):
        super().__init__()
        self.mainSelf = mainSelf
        self.isSiteRunning = mainSelf.isSiteRunning

    def do_work(self):
        import sys
        import os
        if not self.isSiteRunning:
            return
        
        if os.path.isdir(os.path.join(self.mainSelf.exeDirName, 'win_bin', 'bin')):
            binDir = os.path.join(self.mainSelf.exeDirName, 'win_bin', 'bin')
        else:
            binDir = os.path.join(self.mainSelf.exeDirName, 'mac_bin', 'bin')

        igsFileCsv = os.path.join(binDir, 'IGSNetwork.csv')
        megxSiteList = readMegxSiteInf(igsFileCsv)
        siteFile = self.mainSelf.siteFileChoose.text()
        
        if self.mainSelf.siteCombBox.currentText() == 'ALL IGS  SITE' or self.mainSelf.siteCombBox.currentText() == 'IGS LIST FILE - e.g(bjfs irkj urum)':
            if self.mainSelf.siteCombBox.currentText() == 'ALL IGS  SITE':
                allSite = megxSiteList
            else:
                allSite = readIgsSiteList(siteFile, megxSiteList)
            
            gnssSysList = []
            for gnssSys in self.mainSelf.igsSiteSys.currentText().split(','):
                if gnssSys == '':
                    continue
                gnssSysList.append(gnssSys)
                
            antList = []
            for ant in self.mainSelf.igsAntListComboCheck.currentText().split(','):
                if ant == '':
                    continue
                antList.append(ant)

            allSiteHaveSys = {}
            for s in allSite:
                if all(item in allSite[s]['System'] for item in gnssSysList):
                    allSiteHaveSys[s] = allSite[s]
            allSiteHaveAnt = {}
            for s in allSiteHaveSys:
                if allSite[s]['Ant'] in antList:
                    allSiteHaveAnt[s] = allSiteHaveSys[s]
                    
            self.chooseSite = allSiteHaveAnt
        else:
            self.chooseSite = readSiteInf(siteFile)
        
        lmin = self.mainSelf.LminLine.text()
        lmax = self.mainSelf.LmaxLine.text()
        bmin = self.mainSelf.BminLine.text()
        bmax = self.mainSelf.BmaxLine.text()
        
        if is_number(lmin) and is_number(lmax) and is_number(bmin) and is_number(bmax):
            lmin = float(lmin)
            lmax = float(lmax)
            bmin = float(bmin)
            bmax = float(bmax)
            if -180 <= lmin <= 180 and -180 <= lmax <= 180  and -90 <= bmin <= 90  and -90 <= bmax <= 90 and lmin < lmax and bmin < bmax:
                pass
            else:
                lmin = -180
                lmax = 180
                bmin = -90
                bmax = 90
        else:
            lmin = -180
            lmax = 180
            bmin = -90
            bmax = 90

        thinningLine = self.mainSelf.thinningLine.text()
        if thinningLine == '':
            thinningNum = None
        elif is_number(thinningLine):
            thinningNum = float(thinningLine)
            if 90 > thinningNum > 0:
                ...
            else:
                thinningNum = None
        else:
            thinningNum = None

        if thinningNum is not None:
            self.chooseSite = thinning(self.chooseSite, thinningNum, lmin, lmax, bmin, bmax)
        else:
            checkBL = {}
            for s in self.chooseSite:
                sL = self.chooseSite[s]['L']
                sB = self.chooseSite[s]['B']

                if lmin <= sL <= lmax and bmin <= sB <= bmax:
                    checkBL[s] = self.chooseSite[s]
            self.chooseSite = checkBL
        autoLB = not self.mainSelf.globalCheckBox.isChecked()
        plotSite(site=self.chooseSite, self=self.mainSelf, siteName=self.mainSelf.siteNameCheckBox.isChecked(), autoLB = autoLB)

        self.finished.emit(self.chooseSite)

    def stop(mainSelf):
        mainSelf.isSiteRunning = False

def siteCombBoxChanged(self):
    if self.siteCombBox.currentText() == 'ALL IGS  SITE':
        self.siteFileChoose.setEnabled(False)
        self.siteChooseFileBtn.setEnabled(False)
    else:
        self.siteFileChoose.setEnabled(True)
        self.siteChooseFileBtn.setEnabled(True)



def siteChooseFileProcess(self):
    
    if os.path.isdir(os.path.join(self.exeDirName, 'win_bin')):
        binDir = os.path.join(self.exeDirName, 'win_bin')
    else:
        binDir = os.path.join(self.exeDirName, 'mac_bin')
    open_path_file = os.path.join(binDir, 'open.path')
    if os.path.isfile(open_path_file):
        open_path_file_open = open(open_path_file, 'r+')
        open_path = open_path_file_open.readline()
        open_path_file_open.close()
    else:
        open_path = '~'
    filename, filetype = QFileDialog.getOpenFileName(self, "Select OBS file", expanduser(open_path), "")
    if len(filename) == 0:
        self.status.showMessage('No file selected')
    else:
        self.status.showMessage('Selected obs file -> ' + filename)
        QApplication.processEvents()

        out_dir = str(filename).split(os.path.basename(filename))[0][:-1]
        open_path_file_open = open(open_path_file, 'w+')
        open_path_file_open.write(out_dir)
        open_path_file_open.close()
    self.siteFileChoose.setText(filename)

def siteWorkFinished(self, chooseSite):
    self.chooseSite = chooseSite
    self.isSiteRunning = False

    
def sitePlotProcess(self):
    if self.isSiteRunning:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Plotting, do not click again!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    self.isSiteRunning = True
    self.thread = QThread()
    self.siteWork = runSiteWorker(self)
    self.siteWork.moveToThread(self.thread)
    self.thread.started.connect(self.siteWork.do_work)
    self.siteWork.finished.connect(partial(siteWorkFinished, self))
    self.siteWork.finished.connect(self.thread.quit)
    self.siteWork.finished.connect(self.siteWork.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.start()

def saveSite(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog   # 可选,禁用本地对话框

    savePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)
    savePngPath = savePath + '.png'
    saveSiteFile = savePath + '_sitInf.txt'
    self.figsite.savefig(savePngPath, bbox_inches='tight', dpi=800)
    writeSiteInf(self.chooseSite, saveSiteFile)

    saveSiteFile = savePath + '_sitList.txt'
    writeSiteList(self.chooseSite, saveSiteFile)