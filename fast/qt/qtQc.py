# -*- coding: utf-8 -*-
# qtQc              : pyqt5 for QC module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02


from PyQt5.QtCore import QThread, QTimer
import os
from PyQt5.QtWidgets import QFileDialog, QApplication
from os.path import expanduser
from PyQt5.QtWidgets import QMessageBox
from fast.com.readObs import readObs, readObsHead, is_obs
from functools import partial
from PyQt5.QtCore import QObject, pyqtSignal, QDateTime
from fast.plot.plotFreq import plotFreq
from fast.plot.plotLnoise import plotPhaseNoise
from fast.plot.plotSatNum import plotSatNum
from fast.plot.plotCnr import plotCnr
from fast.qc.highOrderDiff import getObsHighOrderDiff, writeHod
from fast.plot.plotHighOrderDiff import plotHighOrderDiff
from fast.plot.plotHighOrderDiff import plotHighOrderDiff
from fast.qc.multipath import multipath, writeMp
from fast.plot.plotMultipath import plotMultipath
from fast.qc.cycleSlip import turboedit, writeSlip
from fast.plot.plotCycleSlip import plotCycleSlip
from fast.qc.CMC import CMC, writeCmc
from fast.plot.plotCMC import plotCMC
from fast.qc.IOD import IOD, writeIon
from fast.plot.plotIOD import plotIOD
from fast.qc.noise import phaseNoise, writePhaseNoise
from fast.qc.obsFreq import writeFreqData
from fast.qc.satNum import writeSatNum
from fast.qc.CNR import writeCnr

QApplication.processEvents()

class runPlotWorker(QObject):
    finished = pyqtSignal(object, object)

    def __init__(self, obsHead, obsData, mainSelf):
        super().__init__()
        self.obsHead = obsHead
        self.obsData = obsData
        self.mainSelf = mainSelf
        self.is_running = mainSelf.is_running

    def do_work(self):
        if not self.is_running:
            return
        print(self.obsHead)
        modeChoose = self.mainSelf.qcCombBox.currentText()
        qcData = None
        if modeChoose == '频点序列' or modeChoose == 'Sat Vis':
            qcData = plotFreq(self.obsHead, self.obsData, self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(0)
        elif modeChoose == '卫星数量' or modeChoose == 'Sat Num':
            qcData = plotSatNum(self.obsData, self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(1)
        elif modeChoose == 'CNR':
            qcData = plotCnr(self.obsHead, self.obsData, self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(2)
        elif modeChoose == '周跳比' or modeChoose == 'CSR':
            qcData = turboedit(self.obsHead, self.obsData, self=self.mainSelf)
            plotCycleSlip(qcData, self=self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(3)
        elif modeChoose == '相位噪声' or modeChoose == 'L_NOISE':
            qcData = phaseNoise(self.obsHead, self.obsData, self=self.mainSelf)
            plotPhaseNoise(qcData, self=self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(4)
        elif modeChoose == '多路径' or modeChoose == 'MP':
            qcData = multipath(self.obsHead, self.obsData, self=self.mainSelf)
            plotMultipath(qcData, self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(5)
        elif modeChoose == 'CMC':
            qcData = CMC(self.obsHead, self.obsData, self=self.mainSelf)
            plotCMC(qcData, self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(6)
        elif modeChoose == 'IOD':
            qcData = IOD(self.obsHead, self.obsData, self=self.mainSelf)
            plotIOD(qcData, self.mainSelf)
            self.mainSelf.qc_plot.setCurrentIndex(7)
        else:
            print()
        self.finished.emit(modeChoose, qcData)


class batchRunPlotWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, obsHead, obsData, savePath, mainSelf):
        super().__init__()
        self.obsHead = obsHead
        self.obsData = obsData
        self.mainSelf = mainSelf
        self.savePath = savePath
        self.is_running = mainSelf.is_running

    def do_work(self):
        if not self.is_running:
            return
        self.mainSelf.qcFreqData = plotFreq(self.obsHead, self.obsData, self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(0)

        self.mainSelf.qcSatNumData = plotSatNum(self.obsData, self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(1)

        self.mainSelf.qcCnrData = plotCnr(self.obsHead, self.obsData, self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(2)

        mwgfData = turboedit(self.obsHead, self.obsData, self=self.mainSelf)
        self.mainSelf.qcSlipData = mwgfData
        plotCycleSlip(mwgfData, self=self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(3)

        # highOrderDiffData = getObsHighOrderDiff(self.obsHead, self.obsData, self=self.mainSelf)
        # self.mainSelf.qcHighData = highOrderDiffData
        # plotHighOrderDiff(highOrderDiffData, self=self.mainSelf)
        # self.mainSelf.qc_plot.setCurrentIndex(4)

        phaseNoiseData = phaseNoise(self.obsHead, self.obsData, self=self.mainSelf)
        self.mainSelf.phaseNoiseData = phaseNoiseData
        plotPhaseNoise(phaseNoiseData, self=self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(4)
        
        mpData = multipath(self.obsHead, self.obsData, self=self.mainSelf)
        self.mainSelf.qcMpData = mpData
        plotMultipath(mpData, self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(5)

        cmcData = CMC(self.obsHead, self.obsData, self=self.mainSelf)
        self.mainSelf.qcCmcData = cmcData
        plotCMC(cmcData, self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(6)

        iodData = IOD(self.obsHead, self.obsData, self=self.mainSelf)
        self.mainSelf.qcIodData = iodData
        plotIOD(iodData, self.mainSelf)
        self.mainSelf.qc_plot.setCurrentIndex(7)
        
        savePngPath = self.savePath + '_Freq.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figFreq.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_Freq.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcFreqData is not None:
            writeFreqData(self.mainSelf.qcFreqData, saveTxtPath)

        savePngPath = self.savePath + '_SatNum.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figsatnum.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_SatNum.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcSatNumData is not None:
            writeSatNum(self.mainSelf.qcSatNumData, saveTxtPath)


        savePngPath = self.savePath + '_CNR.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figcnr.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_CNR.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcCnrData is not None:
            writeCnr(self.mainSelf.qcCnrData, saveTxtPath)


        savePngPath = self.savePath + '_Slip.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figCycleSlip.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_Slip.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcSlipData is not None:
            writeSlip(self.mainSelf.qcSlipData, saveTxtPath)

        # savePngPath = self.savePath + '_HOD.png'
        # self.mainSelf.status.showMessage("Saving " + savePngPath)
        # QApplication.processEvents()
        # self.mainSelf.fighighorder.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        # saveTxtPath = self.savePath + '_HOD.txt'
        # self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        # QApplication.processEvents()
        # if self.mainSelf.qcHighData is not None:
        #     writeHod(self.mainSelf.qcHighData, saveTxtPath)

        savePngPath = self.savePath + '_phaseNoise.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figPhaseNoise.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_phaseNoise.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.phaseNoiseData is not None:
            writePhaseNoise(self.mainSelf.phaseNoiseData, saveTxtPath)

        savePngPath = self.savePath + '_MP.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figMP.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_MP.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcMpData is not None:
            writeMp(self.mainSelf.qcMpData, saveTxtPath)

        savePngPath = self.savePath + '_CMC.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figCMC.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_CMC.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcCmcData is not None:
            writeCmc(self.mainSelf.qcCmcData, saveTxtPath)

        savePngPath = self.savePath + '_IOD.png'
        self.mainSelf.status.showMessage("Saving " + savePngPath)
        QApplication.processEvents()
        self.mainSelf.figIOD.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
        saveTxtPath = self.savePath + '_IOD.txt'
        self.mainSelf.status.showMessage("Saving " + saveTxtPath)
        QApplication.processEvents()
        if self.mainSelf.qcIodData is not None:
            writeIon(self.mainSelf.qcIodData, saveTxtPath)

        self.mainSelf.status.showMessage("Saving completed.")
        QApplication.processEvents()
        self.finished.emit()

def choose_obs_file(self):
    import sys
    obsHead = None
    obsData = None


    open_path_file = os.path.join(self.exeDirName, 'win_bin', 'open.path')
    if os.path.isfile(open_path_file):
        open_path_file_open = open(open_path_file, 'r+')
        open_path = open_path_file_open.readline()
        open_path_file_open.close()
    else:
        open_path = '~'
    filename, filetype = QFileDialog.getOpenFileName(self, "Select Obs file", expanduser(open_path), "")
    if len(filename) == 0:
        self.status.showMessage('No file is selected')
        return obsHead, obsData
    else:
        self.status.showMessage('Select the Obs file -> ' + filename)
        QApplication.processEvents()

        out_dir = str(filename).split(os.path.basename(filename))[0][:-1]
        open_path_file_open = open(open_path_file, 'w+')
        open_path_file_open.write(out_dir)
        open_path_file_open.close()

    
    if not is_obs(filename):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("File format error!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return obsHead, obsData
    self.qcObsFileChoose.setText(filename)
    obsFile = self.qcObsFileChoose.text()
    self.qcObsFile = obsFile
    self.qcFreqData = None
    self.qcSatNumData = None  
    self.qcCnrData = None  
    self.qcSlipData = None  
    self.qcHighData = None  
    self.qcMpData = None  
    self.qcCmcData = None  
    self.qcIodData = None  
    obsHead = readObsHead(obsFile, needSatList=True, bar=self)
    obsData = readObs(obsFile, obsHead, bar=self)
    return obsHead, obsData


def choose_obs_and_process(self):
    obsHead = None
    obsData = None
    try:
        obsHead, obsData = choose_obs_file(self)
    except:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("FORMAT ERROR, CHECK FILE!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    
    if obsHead is None or obsData is None:
        return None
    
    stDatetime = list(obsData)[0]
    edDatetime = list(obsData)[-1]

    self.qcStartDateTimeEdit.setDateTime(QDateTime(stDatetime.year, stDatetime.month, stDatetime.day, stDatetime.hour,
                                            stDatetime.minute, stDatetime.second))

    self.qcEndDateTimeEdit.setDateTime(QDateTime(edDatetime.year, edDatetime.month, edDatetime.day, edDatetime.hour,
                                            edDatetime.minute, edDatetime.second))
    self.qcChooseObsHead = obsHead
    self.qcChooseObsData = obsData

    self.qcChooseSysBox.clear()
    self.qcChooseBandBox.clear()
    self.qcChoosePrnBox.clear()

    self.figFreq.clf()
    self.axFreq = self.figFreq.add_subplot()
    self.figFreq.canvas.draw()

    self.figsatnum.clf()
    self.axsatnum = self.figsatnum.add_subplot()
    self.figsatnum.canvas.draw()

    self.figcnr.clf()
    self.axcnr = self.figcnr.add_subplot()
    self.figcnr.canvas.draw()

    self.figCycleSlip.clf()
    self.axCycleSlip = self.figCycleSlip.add_subplot()
    self.figCycleSlip.canvas.draw()

    # self.fighighorder.clf()
    # self.axhighorder = self.fighighorder.add_subplot()
    # self.fighighorder.canvas.draw()

    self.figPhaseNoise.clf()
    self.axPhaseNoise = self.figPhaseNoise.add_subplot()
    self.figPhaseNoise.canvas.draw()

    self.figMP.clf()
    self.axMP = self.figMP.add_subplot()
    self.figMP.canvas.draw()

    self.figCMC.clf()
    self.axCMC = self.figCMC.add_subplot()
    self.figCMC.canvas.draw()

    self.figIOD.clf()
    self.axIOD = self.figIOD.add_subplot()
    self.figIOD.canvas.draw()

    
    self.qcSysBand = []
    for gnssSys in obsHead['OBS TYPES']:
        self.qcChooseSysBox.addItem(gnssSys)
        for band in obsHead['OBS TYPES'][gnssSys]:
            nowBand = gnssSys + '_' + band[1:]
            if nowBand not in self.qcSysBand:
                self.qcSysBand.append(nowBand)
                self.qcChooseBandBox.addItem(nowBand)


    for i in range(self.qcChooseSysBox.row_num):
        self.qcChooseSysBox.qCheckBox[i].setChecked(True)

    for i in range(self.qcChoosePrnBox.row_num):
        self.qcChoosePrnBox.qCheckBox[i].setChecked(True)

    for i in range(self.qcChooseBandBox.row_num):
        self.qcChooseBandBox.qCheckBox[i].setChecked(True)

def qcWorkFinished(self, modeChoose, qcData):
    if modeChoose == '频点序列' or modeChoose == 'Sat Vis':
        self.qcFreqData = qcData
    elif modeChoose == '卫星数量' or modeChoose == 'Sat Num':
        self.qcSatNumData = qcData
    elif modeChoose == 'CNR':
        self.qcCnrData = qcData
    elif modeChoose == '周跳比' or modeChoose == 'CSR':
        self.qcSlipData = qcData
    elif modeChoose == '高次差' or modeChoose == 'HOD':
        self.qcHighData = qcData
    elif modeChoose == '多路径' or modeChoose == 'MP':
        self.qcMpData = qcData
    elif modeChoose == '相位噪声' or modeChoose == 'L_NOISE':
        self.phaseNoiseData = qcData
    elif modeChoose == 'CMC':
        self.qcCmcData = qcData
    elif modeChoose == 'IOD':
        self.qcIodData = qcData
    else:
        ...
    self.is_running = False

def analyze_plot(self):
    if self.is_running:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Runing, do not click again!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    if self.qcChooseObsHead is None or self.qcChooseObsData is None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Please select Obs file!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    self.is_running = True

    self.thread = QThread()
    self.plotWorker = runPlotWorker(self.qcChooseObsHead, self.qcChooseObsData, self)
    self.plotWorker.moveToThread(self.thread)
    self.thread.started.connect(self.plotWorker.do_work)
    self.plotWorker.finished.connect(partial(qcWorkFinished, self))
    self.plotWorker.finished.connect(self.thread.quit)
    self.plotWorker.finished.connect(self.plotWorker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.start()

def batchQcWorkFinished(self):
    self.is_running = False

def batch_analyze_plot(self):
    if self.is_running:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Runing, do not click again!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    if self.qcChooseObsHead is None or self.qcChooseObsData is None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Please select Obs file!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog   # 可选,禁用本地对话框

    savePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)

    if len(savePath) == 0:
        return None
    
    self.is_running = True
    self.thread = QThread()
    self.plotWorker = batchRunPlotWorker(self.qcChooseObsHead, self.qcChooseObsData, savePath, self)
    self.plotWorker.moveToThread(self.thread)
    self.thread.started.connect(self.plotWorker.do_work)
    self.plotWorker.finished.connect(self.thread.quit)
    self.plotWorker.finished.connect(self.plotWorker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.plotWorker.finished.connect(lambda: batchQcWorkFinished(self))
    self.thread.start()

def qcSysChange(self):
    if self.qcChooseObsHead is None or self.qcChooseObsData is None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Please select Obs file!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None
    self.qcChooseBandBox.clear()
    self.qcChoosePrnBox.clear()
    
    nowSys = self.qcChooseSysBox.currentText()
    nowGnssSys = []
    
    self.qcChooseBandBox.clear()
    for gnssSys in nowSys.split(','):
        if '' != gnssSys:
            nowGnssSys.append(gnssSys)

    qcSysBand = []
    for gnssSys in self.qcChooseObsHead['OBS TYPES']:
        if gnssSys in nowGnssSys:
            for band in self.qcChooseObsHead['OBS TYPES'][gnssSys]:
                nowBand = gnssSys + '_' + band[1:]
                if nowBand not in qcSysBand:
                    qcSysBand.append(nowBand)
                    self.qcChooseBandBox.addItem(nowBand)
    
    self.qcChooseObsHead['prn'].sort(reverse=False)

    for prn in self.qcChooseObsHead['prn']:
        if prn[0] in nowGnssSys:
            self.qcChoosePrnBox.addItem(prn)

    for i in range(self.qcChoosePrnBox.row_num):
        self.qcChoosePrnBox.qCheckBox[i].setChecked(True)

    for i in range(self.qcChooseBandBox.row_num):
        self.qcChooseBandBox.qCheckBox[i].setChecked(True)

class runSaveQcWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, savePath, mainSelf):
        super().__init__()
        self.savePath = savePath
        self.mainSelf = mainSelf
        self.is_save_running = mainSelf.is_save_running

    def do_work(self):
        if not self.is_save_running:
            return
        modeChoose = self.mainSelf.qcCombBox.currentText()
        if modeChoose == '频点序列' or modeChoose == 'Sat Vis':
            savePngPath = self.savePath + '_Freq.png'
            saveTxtPath = self.savePath + '_Freq.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figFreq.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcFreqData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeFreqData(self.mainSelf.qcFreqData, saveTxtPath)
        elif modeChoose == '卫星数量' or modeChoose == 'Sat Num':
            savePngPath = self.savePath + '_SatNum.png'
            saveTxtPath = self.savePath + '_SatNum.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figsatnum.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcSatNumData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeSatNum(self.mainSelf.qcSatNumData, saveTxtPath)
        elif modeChoose == 'CNR':
            savePngPath = self.savePath + '_CNR.png'
            saveTxtPath = self.savePath + '_CNR.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figcnr.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcCnrData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeCnr(self.mainSelf.qcCnrData, saveTxtPath)
        elif modeChoose == '周跳比' or modeChoose == 'CSR':
            savePngPath = self.savePath + '_Slip.png'
            saveTxtPath = self.savePath + '_Slip.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figCycleSlip.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcSlipData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeSlip(self.mainSelf.qcSlipData, saveTxtPath)
        elif modeChoose == '高次差' or modeChoose == 'HOD':
            savePngPath = self.savePath + '_HOD.png'
            saveTxtPath = self.savePath + '_HOD.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.fighighorder.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcHighData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeHod(self.mainSelf.qcHighData, saveTxtPath)

        elif modeChoose == '相位噪声' or modeChoose == 'L_NOISE':
            savePngPath = self.savePath + '_PhaseNoise.png'
            saveTxtPath = self.savePath + '_PhaseNoise.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figPhaseNoise.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.phaseNoiseData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writePhaseNoise(self.mainSelf.phaseNoiseData, saveTxtPath)

        elif modeChoose == '多路径' or modeChoose == 'MP':
            savePngPath = self.savePath + '_MP.png'
            saveTxtPath = self.savePath + '_MP.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figMP.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcMpData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeMp(self.mainSelf.qcMpData, saveTxtPath)

        elif modeChoose == 'CMC':
            savePngPath = self.savePath + '_CMC.png'
            saveTxtPath = self.savePath + '_CMC.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figCMC.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcCmcData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeCmc(self.mainSelf.qcCmcData, saveTxtPath)

        elif modeChoose == 'IOD':
            savePngPath = self.savePath + '_IOD.png'
            saveTxtPath = self.savePath + '_IOD.txt'
            self.mainSelf.status.showMessage("Saving " + savePngPath)
            QApplication.processEvents()
            self.mainSelf.figIOD.savefig(savePngPath, bbox_inches='tight', dpi=self.mainSelf.savePngDPI)
            if self.mainSelf.qcIodData is not None:
                self.mainSelf.status.showMessage("Saving " + saveTxtPath)
                QApplication.processEvents()
                writeIon(self.mainSelf.qcIodData, saveTxtPath)
        else:
            print()
        self.mainSelf.status.showMessage("Saving completed.")
        QApplication.processEvents()
        self.finished.emit()
    

def qcSaveFinished(self):
    self.is_save_running = False


def saveQcFile(self):
    if self.is_save_running:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Poltting!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        return None

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog   # 可选,禁用本地对话框

    savePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)
    
    if len(savePath) == 0:
        return None
    
    self.is_save_running = True

    self.qcSaveThread = QThread()
    self.savePngWorker = runSaveQcWorker(savePath, self)
    self.savePngWorker.moveToThread(self.qcSaveThread)
    self.qcSaveThread.started.connect(self.savePngWorker.do_work)
    self.savePngWorker.finished.connect(partial(qcSaveFinished, self))
    self.savePngWorker.finished.connect(self.qcSaveThread.quit)
    self.savePngWorker.finished.connect(self.savePngWorker.deleteLater)
    self.qcSaveThread.finished.connect(self.qcSaveThread.deleteLater)
    self.qcSaveThread.start()
