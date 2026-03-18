# -*- coding: utf-8 -*-
# FAST           : SPP UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.18

from PyQt5.QtWidgets import QGridLayout, QFrame, QWidget, QSplitter, QLabel, \
    QPushButton, QLineEdit, QHBoxLayout, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime, QSize
from fast.qt.qtFrame import ComboCheckBox
from fast.qt.qtStyle import get_small_btn_style, get_run_btn_style, get_save_btn_style
from fast.qt.qtSpp import sppChooseObsProcess, runSpp, saveSppPos, sppChooseNav

import matplotlib.pyplot as plt


def init_spp_ui(main_win, font, chinese, choose_h):
    """初始化SPP模块UI"""
    sppMenu = QGridLayout()
    sppMenu.setSpacing(20)
    main_win.isSppRunning = False
    main_win.isSppSaving = False
    main_win.posData = None

    # 观测文件
    main_win.sppObsFileChoose = QLineEdit(main_win)
    main_win.sppObsFileChoose.setFont(font)
    sppMenu.addWidget(main_win.sppObsFileChoose, 0, 0, 1, 1)

    main_win.sppChooseObsHead = None
    main_win.sppChooseObsData = None
    main_win.sppSysBand = []
    if chinese:
        main_win.sppChooseObsBtn = QPushButton('观测文件', main_win)
    else:
        main_win.sppChooseObsBtn = QPushButton('OBS', main_win)
    main_win.sppChooseObsBtn.setFont(font)
    main_win.sppChooseObsBtn.setMinimumSize(QSize(80, choose_h + 15))
    sppMenu.addWidget(main_win.sppChooseObsBtn, 0, 1, 1, 1, alignment=Qt.AlignRight)
    main_win.sppChooseObsBtn.clicked.connect(lambda: sppChooseObsProcess(main_win))

    # 广播星历
    main_win.sppNavFileChoose = QLineEdit(main_win)
    main_win.sppNavFileChoose.setFont(font)
    sppMenu.addWidget(main_win.sppNavFileChoose, 1, 0, 1, 1)

    main_win.sppChooseNavData = None
    if chinese:
        main_win.sppChooseNavBtn = QPushButton('广播星历', main_win)
    else:
        main_win.sppChooseNavBtn = QPushButton('NAV', main_win)
    main_win.sppChooseNavBtn.setFont(font)
    main_win.sppChooseNavBtn.setMinimumSize(QSize(80, choose_h + 15))
    sppMenu.addWidget(main_win.sppChooseNavBtn, 1, 1, 1, 1, alignment=Qt.AlignRight)
    main_win.sppChooseNavBtn.clicked.connect(lambda: sppChooseNav(main_win))

    # 开始时间
    main_win.sppStartDateTimeEdit = QDateTimeEdit()
    main_win.sppStartDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
    main_win.sppStartDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
    main_win.sppStartDateTimeEdit.setFont(font)
    sppMenu.addWidget(main_win.sppStartDateTimeEdit, 3, 0, 1, 1, alignment=Qt.AlignRight)

    if chinese:
        sppStartDateTimeLable = QLabel('开始时间')
    else:
        sppStartDateTimeLable = QLabel('Time Start')
    sppStartDateTimeLable.setFont(font)
    sppStartDateTimeLable.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(sppStartDateTimeLable, 3, 1, 1, 1)

    # 结束时间
    main_win.sppEndDateTimeEdit = QDateTimeEdit()
    main_win.sppEndDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
    main_win.sppEndDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
    main_win.sppEndDateTimeEdit.setFont(font)
    sppMenu.addWidget(main_win.sppEndDateTimeEdit, 4, 0, 1, 1, alignment=Qt.AlignRight)

    if chinese:
        sppEndDateTimeLable = QLabel('结束时间')
    else:
        sppEndDateTimeLable = QLabel('Time End')
    sppEndDateTimeLable.setFont(font)
    sppEndDateTimeLable.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(sppEndDateTimeLable, 4, 1, 1, 1)

    # 系统选择
    main_win.sppChooseSysCombBox = ComboCheckBox(['GPS', 'GAL', 'BDS'], None)
    sppMenu.addWidget(main_win.sppChooseSysCombBox, 5, 0, 1, 1)
    sppSYSLable = QLabel('System')
    sppSYSLable.setFont(font)
    sppSYSLable.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(sppSYSLable, 5, 1, 1, 1)

    # Cutoff
    main_win.cutoffChoose = QLineEdit(main_win)
    main_win.cutoffChoose.setFont(font)
    main_win.cutoffChoose.setText("7")
    sppMenu.addWidget(main_win.cutoffChoose, 6, 0, 1, 1)

    catoffLable = QLabel('Cutoff')
    catoffLable.setFont(font)
    catoffLable.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(catoffLable, 6, 1, 1, 1)

    none_lable = QLabel('')
    sppMenu.addWidget(none_lable, 11, 0)

    # 按钮样式
    spp_run_style = get_run_btn_style()
    spp_save_style = get_save_btn_style()
    main_win.sppChooseObsBtn.setStyleSheet(get_small_btn_style())
    main_win.sppChooseNavBtn.setStyleSheet(get_small_btn_style())

    # 运行按钮
    if chinese:
        runSppBtn = QPushButton('运行', main_win)
    else:
        runSppBtn = QPushButton('Run', main_win)
    runSppBtn.setFont(font)
    runSppBtn.setMinimumSize(QSize(150, choose_h + 15))
    runSppBtn.setStyleSheet(spp_run_style)
    total_columns = sppMenu.columnCount()
    sppMenu.addWidget(runSppBtn, 12, 0, 1, total_columns)
    runSppBtn.clicked.connect(lambda: runSpp(main_win))

    # 保存按钮
    if chinese:
        saveSppBtn = QPushButton('保存', main_win)
    else:
        saveSppBtn = QPushButton('SAVE', main_win)
    saveSppBtn.setFont(font)
    saveSppBtn.setMinimumSize(QSize(150, choose_h + 15))
    saveSppBtn.setStyleSheet(spp_save_style)
    sppMenu.addWidget(saveSppBtn, 13, 0, 1, total_columns)
    saveSppBtn.clicked.connect(lambda: saveSppPos(main_win))

    sppLeft_in = QFrame()
    sppLeft_in.setFrameShape(QFrame.StyledPanel)
    sppMenu.setColumnStretch(1, 1)
    sppLeft_in.setLayout(sppMenu)

    sppRight_in = QFrame()
    sppRight_in.setFrameShape(QFrame.StyledPanel)

    main_win.figSPP, main_win.axSPP = plt.subplots()
    main_win.canvasSPP = main_win.figSPP.canvas

    sppRight_in.setLayout(QHBoxLayout())
    sppRight_in.layout().addWidget(main_win.canvasSPP)

    sppLeft = QSplitter(Qt.Vertical)
    sppLeft.addWidget(sppLeft_in)

    sppRight = QSplitter(Qt.Vertical)
    sppRight.addWidget(sppRight_in)

    sppAllLayout = QSplitter(Qt.Horizontal)
    sppAllLayout.addWidget(sppLeft)
    sppAllLayout.addWidget(sppRight)
    sppAllLayout.setStretchFactor(1, 3)

    sppLayout = QHBoxLayout(main_win)
    sppLayout.addWidget(sppAllLayout)
    
    return sppLayout
