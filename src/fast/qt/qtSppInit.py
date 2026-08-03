# -*- coding: utf-8 -*-
# FAST           : SPP UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : AIR, Chinese Academy of Sciences
# Creation       : 2026.03.18
# Latest Version : 3.01.01 - 2026.08.03

# 2026.08.03 : 控件补tooltip/placeholder, 修正Lable拼写, 统一按钮文案
#              by ChangChuntao -> Version : 3.01.01

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
    main_win.sppObsFileChoose.setReadOnly(True)
    main_win.sppObsFileChoose.setPlaceholderText('请选择观测文件' if chinese else 'Select obs file')
    main_win.sppObsFileChoose.setToolTip('观测文件(OBS)' if chinese else 'Observation file (OBS)')
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
    main_win.sppNavFileChoose.setReadOnly(True)
    main_win.sppNavFileChoose.setPlaceholderText('请选择广播星历文件' if chinese else 'Select nav file')
    main_win.sppNavFileChoose.setToolTip('广播星历文件(NAV)' if chinese else 'Broadcast ephemeris file (NAV)')
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
    main_win.sppStartDateTimeEdit.setToolTip('定位起始时间(UTC)' if chinese else 'Start time (UTC)')
    sppMenu.addWidget(main_win.sppStartDateTimeEdit, 3, 0, 1, 1, alignment=Qt.AlignRight)

    if chinese:
        sppStartDateTimeLabel = QLabel('开始时间')
    else:
        sppStartDateTimeLabel = QLabel('Time Start')
    sppStartDateTimeLabel.setFont(font)
    sppStartDateTimeLabel.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(sppStartDateTimeLabel, 3, 1, 1, 1)

    # 结束时间
    main_win.sppEndDateTimeEdit = QDateTimeEdit()
    main_win.sppEndDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
    main_win.sppEndDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
    main_win.sppEndDateTimeEdit.setFont(font)
    main_win.sppEndDateTimeEdit.setToolTip('定位结束时间(UTC)' if chinese else 'End time (UTC)')
    sppMenu.addWidget(main_win.sppEndDateTimeEdit, 4, 0, 1, 1, alignment=Qt.AlignRight)

    if chinese:
        sppEndDateTimeLabel = QLabel('结束时间')
    else:
        sppEndDateTimeLabel = QLabel('Time End')
    sppEndDateTimeLabel.setFont(font)
    sppEndDateTimeLabel.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(sppEndDateTimeLabel, 4, 1, 1, 1)

    # 系统选择
    main_win.sppChooseSysCombBox = ComboCheckBox(['GPS', 'GAL', 'BDS'], None)
    main_win.sppChooseSysCombBox.setToolTip('选择参与定位的系统(GPS/BDS/GAL)' if chinese else 'Select systems (GPS/BDS/GAL)')
    sppMenu.addWidget(main_win.sppChooseSysCombBox, 5, 0, 1, 1)
    sppSYSLabel = QLabel('System')
    sppSYSLabel.setFont(font)
    sppSYSLabel.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(sppSYSLabel, 5, 1, 1, 1)

    # Cutoff
    main_win.cutoffChoose = QLineEdit(main_win)
    main_win.cutoffChoose.setFont(font)
    main_win.cutoffChoose.setText("7")
    main_win.cutoffChoose.setToolTip('卫星截止高度角(度), 低于此角度的卫星不参与解算' if chinese else 'Elevation cutoff (deg)')
    sppMenu.addWidget(main_win.cutoffChoose, 6, 0, 1, 1)

    catoffLabel = QLabel('Cutoff')
    catoffLabel.setFont(font)
    catoffLabel.setAlignment(Qt.AlignRight)
    sppMenu.addWidget(catoffLabel, 6, 1, 1, 1)

    none_label = QLabel('')
    sppMenu.addWidget(none_label, 11, 0)

    # 按钮样式
    spp_run_style = get_run_btn_style()
    spp_save_style = get_save_btn_style()
    main_win.sppChooseObsBtn.setStyleSheet(get_small_btn_style())
    main_win.sppChooseNavBtn.setStyleSheet(get_small_btn_style())

    # 运行按钮
    if chinese:
        runSppBtn = QPushButton('运行', main_win)
    else:
        runSppBtn = QPushButton('RUN', main_win)
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
