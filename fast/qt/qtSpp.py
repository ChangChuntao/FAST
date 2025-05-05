# -*- coding: utf-8 -*-
# qtSpp             : pyqt5 for SPP module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02


from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, QTimer, QDateTime
import os
from functools import partial
from PyQt5.QtWidgets import QFileDialog, QApplication
from os.path import expanduser
from fast.com.gnssParameter import getCode
from fast.com.readObs import is_obs
from PyQt5.QtWidgets import QMessageBox
from fast.com.readObs import readObs, readObs3, readObsHead, is_obs
from fast.com.readNav import readNav, is_nav
import sys
from fast.spp.sppbybrdc import spp, writePosData
from PyQt5.QtCore import QObject, pyqtSignal

class runSppWorker(QObject):
    finished = pyqtSignal(object)
    def __init__(self, obsHead, obsData, navData, bandChoose, startDatetime, endDatetime, mainSelf):
        super().__init__()
        self.obsHead = obsHead
        self.obsData = obsData
        self.navData = navData
        self.bandChoose = bandChoose
        self.startDatetime = startDatetime
        self.endDatetime = endDatetime
        self.mainSelf = mainSelf
        self.isSppRunning = mainSelf.isSppRunning

    def do_work(self):
        if not self.isSppRunning:
            return
        posData, XMEAN, YMEAN, ZMEAN = spp(self.obsHead, self.obsData, self.navData, self.bandChoose, self.startDatetime, self.endDatetime, self=self.mainSelf)
        self.finished.emit(posData)

    def stop(mainSelf):
        mainSelf.isSppRunning = False

def sppChooseObs(self):
    obsHead = None
    obsData = None
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
        return obsHead, obsData
    else:
        self.status.showMessage('Selected obs file -> ' + filename)
        QApplication.processEvents()
        out_dir = str(filename).split(os.path.basename(filename))[0][:-1]
        open_path_file_open = open(open_path_file, 'w+')
        open_path_file_open.write(out_dir)
        open_path_file_open.close()

    if not is_obs(filename):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("This file format is not supported.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return obsHead, obsData
    
    self.sppObsFileChoose.setText(filename)
    obsFile = self.sppObsFileChoose.text()
    self.posData = None
    obsHead = readObsHead(obsFile, needSatList=True)
    obsData = readObs(obsFile, obsHead, bar=self)
    return obsHead, obsData

def sppChooseObsProcess(self):
    obsHead, obsData = sppChooseObs(self)
    
    if obsHead is None or obsData is None:
        return None
    
    self.sppChooseObsHead = obsHead
    self.sppChooseObsData = obsData

    stDatetime = list(obsData)[0]
    edDatetime = list(obsData)[-1]

    self.sppStartDateTimeEdit.setDateTime(QDateTime(stDatetime.year, stDatetime.month, stDatetime.day, stDatetime.hour,
                                            stDatetime.minute, stDatetime.second))

    self.sppEndDateTimeEdit.setDateTime(QDateTime(edDatetime.year, edDatetime.month, edDatetime.day, edDatetime.hour,
                                            edDatetime.minute, edDatetime.second))


def sppChooseNav(self):
    navData = None

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
    filename, filetype = QFileDialog.getOpenFileName(self, "Select nav file", expanduser(open_path), "")
    if len(filename) == 0:
        self.status.showMessage('No file selected')
        return navData
    else:
        self.status.showMessage('Selected nav file -> ' + filename)
        QApplication.processEvents()

        out_dir = str(filename).split(os.path.basename(filename))[0][:-1]
        open_path_file_open = open(open_path_file, 'w+')
        open_path_file_open.write(out_dir)
        open_path_file_open.close()

    try:
        self.status.showMessage('Reading nav ...')
        QApplication.processEvents()
        navData = readNav(filename)
    except:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("This file format is not supported.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return navData

    self.sppNavFileChoose.setText(filename)

    self.status.showMessage('Reading nav completed.')
    QApplication.processEvents()

    self.sppChooseNavData = navData

    return navData

def resetSppRunningFlag(self, posData):
    self.posData = posData
    self.isSppRunning = False
    print('self.isSppRunning')



def runSpp(self):
    if self.isSppRunning:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Runing, do not click again!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    if self.sppChooseObsHead is None or self.sppChooseObsData is None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("NO OBS!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    
    if self.sppChooseNavData is None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("NO NAV!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    
    bandChooseInf = {'G': ['1', '2'], 'C': ['2', '6'], 'E': ['1', '5']}
    
    freqChoose = {}
    for gnssSys in self.sppChooseSysCombBox.currentText().split(','):
        if gnssSys == '':
            continue
        if gnssSys == 'GPS':
            freqChoose['G'] = bandChooseInf['G']
        if gnssSys == 'BDS':
            freqChoose['C'] = bandChooseInf['C']
        if gnssSys == 'GAL':
            freqChoose['E'] = bandChooseInf['E']
    startdatetime = self.sppStartDateTimeEdit.dateTime().toPyDateTime()
    enddatetime = self.sppEndDateTimeEdit.dateTime().toPyDateTime()

    bandChoose = getCode(self.sppChooseObsHead, freqChoose)
    print(bandChoose)
    if len(list(bandChoose)) == 0:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("NO available FREQ!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None

    self.isSppRunning = True
    self.thread = QThread()
    self.sppWorker = runSppWorker(self.sppChooseObsHead, self.sppChooseObsData, self.sppChooseNavData, bandChoose, startdatetime, enddatetime, self)
    self.sppWorker.moveToThread(self.thread)
    self.thread.started.connect(self.sppWorker.do_work)
    self.sppWorker.finished.connect(self.thread.quit)
    self.sppWorker.finished.connect(self.sppWorker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.sppWorker.finished.connect(partial(resetSppRunningFlag, self))
    self.thread.start()

def resetSppSaveFlag(self):
    self.isSppSaving = False


class runSppSave(QObject):
    finished = pyqtSignal(object)
    def __init__(self, savePath, mainSelf):
        super().__init__()
        self.savePath = savePath
        self.mainSelf = mainSelf

    def do_work(self):
        if not self.mainSelf.isSppSaving:
            return
        
        self.mainSelf.status.showMessage("Saving " + self.savePath)
        QApplication.processEvents()
        writePosData(self.mainSelf.posData, self.savePath)
        pngFile = self.savePath + '.png'
        self.mainSelf.status.showMessage("Saving " + pngFile)
        QApplication.processEvents()
        self.mainSelf.figSPP.savefig(pngFile, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)

    def stop(mainSelf):
        mainSelf.isSppRunning = False

def saveSppPos(self):
    if self.posData is None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("No SPP conducted!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog   # 可选,禁用本地对话框
    savePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)

    self.isSppSaving = True
    self.thread = QThread()
    self.sppSaver = runSppSave(savePath, self)
    self.sppSaver.moveToThread(self.thread)
    self.thread.started.connect(self.sppSaver.do_work)
    self.sppSaver.finished.connect(self.thread.quit)
    self.sppSaver.finished.connect(self.sppSaver.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.sppSaver.finished.connect(partial(resetSppSaveFlag, self))
    self.thread.start()
    