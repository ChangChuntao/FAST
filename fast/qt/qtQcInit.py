# -*- coding: utf-8 -*-
# FAST           : QC UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.18

from PyQt5.QtWidgets import QGridLayout, QComboBox, QTabWidget, QFrame, \
    QWidget, QSplitter, QLabel, QPushButton, QLineEdit, QVBoxLayout, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime, QSize
from fast.qt.qtFrame import ComboCheckBox
from fast.qt.qtStyle import (
    get_small_btn_style, get_primary_btn_style, 
    get_save_btn_style, get_qc_plot_tab_style
)
from fast.qt.qtQc import analyze_plot, qcSysChange, choose_obs_and_process, batch_analyze_plot, saveQcFile

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def init_qc_ui(main_win, font, chinese, choose_h, screenWidth, screenHeight):
    """初始化QC模块UI"""
    qcMenu = QGridLayout()
    qcMenu.setSpacing(20)
    main_win.qcObsFile = None
    main_win.is_running = False
    main_win.is_save_running = False
    main_win.qcFreqData = None
    main_win.qcSatNumData = None
    main_win.qcCnrData = None
    main_win.qcSlipData = None
    main_win.qcHighData = None
    main_win.qcMpData = None
    main_win.qcCmcData = None
    main_win.qcIodData = None

    # 观测文件选择
    main_win.qcObsFileChoose = QLineEdit(main_win)
    main_win.qcObsFileChoose.setFont(font)
    qcMenu.addWidget(main_win.qcObsFileChoose, 0, 0, 1, 1)

    main_win.qcChooseObsHead = None
    main_win.qcChooseObsData = None
    if chinese:
        main_win.qcChooseObsBtn = QPushButton('观测文件', main_win)
    else:
        main_win.qcChooseObsBtn = QPushButton('OBS', main_win)
    main_win.qcChooseObsBtn.setFont(font)
    main_win.qcChooseObsBtn.setMinimumSize(QSize(80, choose_h + 15))
    qcMenu.addWidget(main_win.qcChooseObsBtn, 0, 1, 1, 1, alignment=Qt.AlignRight)
    main_win.qcChooseObsBtn.clicked.connect(lambda: choose_obs_and_process(main_win))

    # 分析选择下拉框
    main_win.qcCombBox = QComboBox(main_win)
    if chinese:
        main_win.qcCombBox.addItem("频点序列")
        main_win.qcCombBox.addItem("卫星数量")
        main_win.qcCombBox.addItem("CNR")
        main_win.qcCombBox.addItem("周跳比")
        main_win.qcCombBox.addItem("相位噪声")
        main_win.qcCombBox.addItem("多路径")
        main_win.qcCombBox.addItem("CMC")
        main_win.qcCombBox.addItem("IOD")
    else:
        main_win.qcCombBox.addItem("Sat Vis")
        main_win.qcCombBox.addItem("Sat Num")
        main_win.qcCombBox.addItem("CNR")
        main_win.qcCombBox.addItem("CSR")
        main_win.qcCombBox.addItem("L_NOISE")
        main_win.qcCombBox.addItem("MP")
        main_win.qcCombBox.addItem("CMC")
        main_win.qcCombBox.addItem("IOD")
    main_win.qcCombBox.setFont(font)
    qcMenu.addWidget(main_win.qcCombBox, 1, 0, 1, 1)

    if chinese:
        qcChooseLable = QLabel('分析选择')
    else:
        qcChooseLable = QLabel('Options')
    qcChooseLable.setFont(font)
    qcChooseLable.setAlignment(Qt.AlignRight)
    qcMenu.addWidget(qcChooseLable, 1, 1, 1, 1)

    # 系统选择
    main_win.qcChooseSysBox = ComboCheckBox([], None)
    main_win.qcChooseSysBox.setFont(font)
    qcMenu.addWidget(main_win.qcChooseSysBox, 2, 0, 1, 1)
    main_win.qcChooseSysBox.qLineEdit.textChanged.connect(lambda: qcSysChange(main_win))

    if chinese:
        qcChooseSysLable = QLabel('系统选择')
    else:
        qcChooseSysLable = QLabel('System')
    qcChooseSysLable.setFont(font)
    qcChooseSysLable.setAlignment(Qt.AlignRight)
    qcMenu.addWidget(qcChooseSysLable, 2, 1, 1, 1)

    # PRN选择
    main_win.qcChoosePrnBox = ComboCheckBox([], None)
    main_win.qcChoosePrnBox.setFont(font)
    qcMenu.addWidget(main_win.qcChoosePrnBox, 3, 0, 1, 1)

    if chinese:
        qcChoosePrnLable = QLabel('卫星选择')
    else:
        qcChoosePrnLable = QLabel('PRN')
    qcChoosePrnLable.setFont(font)
    qcChoosePrnLable.setAlignment(Qt.AlignRight)
    qcMenu.addWidget(qcChoosePrnLable, 3, 1, 1, 1)

    # 频点选择
    main_win.qcChooseBandBox = ComboCheckBox([], None)
    main_win.qcChooseBandBox.setFont(font)
    qcMenu.addWidget(main_win.qcChooseBandBox, 4, 0, 1, 1)

    if chinese:
        qcChooseBandLable = QLabel('频点选择')
    else:
        qcChooseBandLable = QLabel('Freq')
    qcChooseBandLable.setFont(font)
    qcChooseBandLable.setAlignment(Qt.AlignRight)
    qcMenu.addWidget(qcChooseBandLable, 4, 1, 1, 1)

    # 开始时间
    main_win.qcStartDateTimeEdit = QDateTimeEdit()
    main_win.qcStartDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
    main_win.qcStartDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
    main_win.qcStartDateTimeEdit.setFont(font)
    qcMenu.addWidget(main_win.qcStartDateTimeEdit, 5, 0, 1, 1, alignment=Qt.AlignRight)

    if chinese:
        qcStartDateTimeLable = QLabel('开始时间')
    else:
        qcStartDateTimeLable = QLabel('Time Start')
    qcStartDateTimeLable.setFont(font)
    qcStartDateTimeLable.setAlignment(Qt.AlignRight)
    qcMenu.addWidget(qcStartDateTimeLable, 5, 1, 1, 1)

    # 结束时间
    main_win.qcEndDateTimeEdit = QDateTimeEdit()
    main_win.qcEndDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
    main_win.qcEndDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
    main_win.qcEndDateTimeEdit.setFont(font)
    qcMenu.addWidget(main_win.qcEndDateTimeEdit, 6, 0, 1, 1, alignment=Qt.AlignRight)

    if chinese:
        qcEndDateTimeLable = QLabel('结束时间')
    else:
        qcEndDateTimeLable = QLabel('Time End')
    qcEndDateTimeLable.setFont(font)
    qcEndDateTimeLable.setAlignment(Qt.AlignRight)
    qcMenu.addWidget(qcEndDateTimeLable, 6, 1, 1, 1)

    none_lable = QLabel('')
    qcMenu.addWidget(none_lable, 7, 0)

    # 按钮样式
    qc_btn_style = get_primary_btn_style()
    qc_save_style = get_save_btn_style()
    main_win.qcChooseObsBtn.setStyleSheet(get_small_btn_style())

    # 分析按钮
    if chinese:
        analyze_plot_btn = QPushButton('分析', main_win)
    else:
        analyze_plot_btn = QPushButton('PLOT', main_win)
    analyze_plot_btn.setFont(font)
    analyze_plot_btn.setMinimumSize(QSize(150, choose_h + 15))
    analyze_plot_btn.setStyleSheet(qc_btn_style)
    total_columns = qcMenu.columnCount()
    qcMenu.addWidget(analyze_plot_btn, 8, 0, 1, total_columns)
    analyze_plot_btn.clicked.connect(lambda: analyze_plot(main_win))

    # 保存按钮
    if chinese:
        analyze_save_btn = QPushButton('保存', main_win)
    else:
        analyze_save_btn = QPushButton('SAVE', main_win)
    analyze_save_btn.setFont(font)
    analyze_save_btn.setMinimumSize(QSize(150, choose_h + 15))
    analyze_save_btn.setStyleSheet(qc_save_style)
    qcMenu.addWidget(analyze_save_btn, 9, 0, 1, total_columns)
    analyze_save_btn.clicked.connect(lambda: saveQcFile(main_win))

    # 批量分析按钮
    if chinese:
        analyze_batch_btn = QPushButton('批量分析保存', main_win)
    else:
        analyze_batch_btn = QPushButton('Batch Analyze and Save', main_win)
    analyze_batch_btn.setFont(font)
    analyze_batch_btn.setMinimumSize(QSize(150, choose_h + 15))
    analyze_batch_btn.setStyleSheet(qc_btn_style)
    qcMenu.addWidget(analyze_batch_btn, 10, 0, 1, total_columns)
    analyze_batch_btn.clicked.connect(lambda: batch_analyze_plot(main_win))

    qcMenu.setColumnStretch(1, 1)

    qcLeft_in = QFrame()
    qcLeft_in.setFrameShape(QFrame.StyledPanel)
    qcLeft_in.setLayout(qcMenu)

    # 右侧Plot Tab
    main_win.qc_plot = QTabWidget()
    main_win.qc_plot.setTabPosition(QTabWidget.South)
    tabBar = main_win.qc_plot.tabBar()
    tabBar.setStyleSheet("QTabBar::tab { min-width: " + str(int(screenWidth / 20)) + "%; min-height: " + str(int(screenHeight / 40)) + "%; }")

    # 频点序列图
    freqTab = QWidget()
    if chinese:
        main_win.qc_plot.addTab(freqTab, '频点序列')
    else:
        main_win.qc_plot.addTab(freqTab, 'Sat Vis')
    main_win.figFreq, main_win.axFreq = plt.subplots()
    main_win.canvasFreq = FigureCanvas(main_win.figFreq)
    freqTabLayout = QVBoxLayout(freqTab)
    freqTabLayout.addWidget(main_win.canvasFreq)

    # 卫星数量
    satnumTab = QWidget()
    if chinese:
        main_win.qc_plot.addTab(satnumTab, '卫星数量')
    else:
        main_win.qc_plot.addTab(satnumTab, 'Sat Num')
    main_win.figsatnum, main_win.axsatnum = plt.subplots()
    main_win.canvassatnum = main_win.figsatnum.canvas
    satnumTabLayout = QVBoxLayout(satnumTab)
    satnumTabLayout.addWidget(main_win.canvassatnum)

    # 载噪比
    cnrTab = QWidget()
    main_win.qc_plot.addTab(cnrTab, 'CNR')
    main_win.figcnr, main_win.axcnr = plt.subplots()
    main_win.canvascnr = main_win.figcnr.canvas
    cnrTabLayout = QVBoxLayout(cnrTab)
    cnrTabLayout.addWidget(main_win.canvascnr)

    # SLIP
    cycleSlipTab = QWidget()
    if chinese:
        main_win.qc_plot.addTab(cycleSlipTab, '周跳比')
    else:
        main_win.qc_plot.addTab(cycleSlipTab, 'CSR')
    main_win.figCycleSlip, main_win.axCycleSlip = plt.subplots(figsize=(6, 5))
    main_win.canvascycleSlip = main_win.figCycleSlip.canvas
    cycleSlipTabLayout = QVBoxLayout(cycleSlipTab)
    cycleSlipTabLayout.addWidget(main_win.canvascycleSlip)

    # 相位噪声
    phaseNoiseTab = QWidget()
    if chinese:
        main_win.qc_plot.addTab(phaseNoiseTab, '相位噪声')
    else:
        main_win.qc_plot.addTab(phaseNoiseTab, 'L_NOISE')
    main_win.figPhaseNoise, main_win.axPhaseNoise = plt.subplots()
    main_win.canvasPhaseNoise = main_win.figPhaseNoise.canvas
    phaseNoiseTabLayout = QVBoxLayout(phaseNoiseTab)
    phaseNoiseTabLayout.addWidget(main_win.canvasPhaseNoise)

    # 多路径
    MPTab = QWidget()
    if chinese:
        main_win.qc_plot.addTab(MPTab, '多路径')
    else:
        main_win.qc_plot.addTab(MPTab, 'MP')
    main_win.figMP, main_win.axMP = plt.subplots()
    main_win.canvasMP = main_win.figMP.canvas
    MPTabLayout = QVBoxLayout(MPTab)
    MPTabLayout.addWidget(main_win.canvasMP)

    # CMC
    CMCTab = QWidget()
    main_win.qc_plot.addTab(CMCTab, 'CMC')
    main_win.figCMC, main_win.axCMC = plt.subplots()
    main_win.canvasCMC = main_win.figCMC.canvas
    CMCTabLayout = QVBoxLayout(CMCTab)
    CMCTabLayout.addWidget(main_win.canvasCMC)

    # IOD
    iodTab = QWidget()
    main_win.qc_plot.addTab(iodTab, 'IOD')
    main_win.figIOD, main_win.axIOD = plt.subplots()
    main_win.canvasIOD = main_win.figIOD.canvas
    iodTabLayout = QVBoxLayout(iodTab)
    iodTabLayout.addWidget(main_win.canvasIOD)

    main_win.qc_plot.setStyleSheet(get_qc_plot_tab_style(screenWidth, screenHeight))

    qcRight_in = QFrame()
    qcRight_in.setFrameShape(QFrame.StyledPanel)
    qcRight_in.setLayout(QHBoxLayout())
    qcRight_in.layout().addWidget(main_win.qc_plot)

    qcLeft = QSplitter(Qt.Vertical)
    qcLeft.addWidget(qcLeft_in)

    qcRight = QSplitter(Qt.Vertical)
    qcRight.addWidget(qcRight_in)

    qcAllLayout = QSplitter(Qt.Horizontal)
    qcAllLayout.addWidget(qcLeft)
    qcAllLayout.addWidget(qcRight)
    qcAllLayout.setStretchFactor(1, 3)

    qcLayout = QHBoxLayout(main_win)
    qcLayout.addWidget(qcAllLayout)
    
    return qcLayout


# 需要导入 QHBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
