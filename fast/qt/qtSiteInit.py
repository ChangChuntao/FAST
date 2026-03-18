# -*- coding: utf-8 -*-
# FAST           : Site UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.18

from PyQt5.QtWidgets import QGridLayout, QComboBox, QFrame, QWidget, QSplitter, \
    QLabel, QPushButton, QLineEdit, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt, QSize
from fast.qt.qtFrame import ComboCheckBox
from fast.qt.qtSite import sitePlotProcess, siteChooseFileProcess, siteCombBoxChanged, saveSite

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt


def init_site_ui(main_win, font, chinese, lable_h, normalBtnH):
    """初始化Site模块UI"""
    siteMenu = QGridLayout()
    siteMenu.setSpacing(20)
    main_win.isSiteRunning = False
    main_win.chooseSite = {}

    # 上方地图
    siteTop_in = QFrame()
    siteTop_in.setFrameShape(QFrame.StyledPanel)

    # 绘图初始化
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rc('xtick', labelsize=15)
    mpl.rc('ytick', labelsize=15)
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    main_win.figsite = plt.figure()
    main_win.figsite.clf()
    main_win.axsite = main_win.figsite.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    main_win.axsite.set_global()
    main_win.axsite.add_feature(cfeature.LAND, facecolor='antiquewhite', zorder=20)
    main_win.axsite.add_feature(cfeature.OCEAN, facecolor='steelblue', zorder=0)
    main_win.gl = main_win.axsite.gridlines(color='white', alpha=0.2, draw_labels=True, dms=True, x_inline=False, y_inline=False, zorder=10)
    main_win.axsite.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
    main_win.figsite.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
    main_win.canvassite = main_win.figsite.canvas

    siteTop_in.setLayout(QHBoxLayout())
    siteTop_in.layout().addWidget(main_win.canvassite)

    # 下方选项
    siteDown_in = QFrame()
    siteDown_in.setFrameShape(QFrame.StyledPanel)
    siteDown_in.setLayout(siteMenu)

    main_win.siteCombBox = QComboBox(main_win)
    main_win.siteCombBox.addItem("ALL IGS  SITE")
    main_win.siteCombBox.addItem("IGS LIST FILE - e.g(bjfs irkj urum)")
    main_win.siteCombBox.addItem("SITE FILE     - e.g(L, B, siteName)")
    main_win.siteCombBox.setMinimumSize(QSize(70, lable_h))
    main_win.siteCombBox.currentIndexChanged.connect(lambda: siteCombBoxChanged(main_win))
    siteMenu.addWidget(main_win.siteCombBox, 0, 0, 1, 2)

    # 站点文件
    main_win.siteFileChoose = QLineEdit(main_win)
    main_win.siteFileChoose.setFont(font)
    siteMenu.addWidget(main_win.siteFileChoose, 1, 0, 1, 1)
    main_win.siteFileChoose.setEnabled(False)

    main_win.siteFileData = None
    main_win.siteChooseFileBtn = QPushButton('Select File', main_win)
    main_win.siteChooseFileBtn.setFont(font)
    siteMenu.addWidget(main_win.siteChooseFileBtn, 1, 1, 1, 1, alignment=Qt.AlignRight)
    main_win.siteChooseFileBtn.clicked.connect(lambda: siteChooseFileProcess(main_win))
    main_win.siteChooseFileBtn.setEnabled(False)

    # GNSS系统
    main_win.igsSiteSys = ComboCheckBox(['GPS', 'GLO', 'GAL', 'BDS', 'SBAS', 'QZSS', 'IRNSS'], None)
    main_win.igsSiteSys.setMinimumSize(QSize(40, lable_h))
    main_win.igsSiteSys.qCheckBox[0].setChecked(True)
    siteMenu.addWidget(main_win.igsSiteSys, 2, 0, 1, 1)

    igsSiteSysLable = QLabel('GNSS System')
    igsSiteSysLable.setFont(font)
    igsSiteSysLable.setAlignment(Qt.AlignRight)
    siteMenu.addWidget(igsSiteSysLable, 2, 1, 1, 1)

    # 天线列表
    main_win.igsAntList = ['TRM57971.00', 'ASH701945G_M', 'TRM59800.99', 'TRM159800.00',
                           'SEPCHOKE_B3E6', 'TRM59800.80', 'LEIAR20', 'LEIAR25.R4', 'TRM59800.00',
                           'TRM115000.00', 'AOAD/M_T', 'LEIAR25.R3', 'ASH701945D_M', 'TPSCR.G5C',
                           'JAVRINGANT_DM', 'ASH700936D_M', 'STXSA1500', 'ASH701945C_M', 'TRM55971.00',
                           'TPSCR.G3', 'LEIAR10', 'TPSCR.G5', 'JAV_RINGANT_G3T', 'TRM59900.00', 'NOV702GG',
                           'TWIVC6150', 'LEIAT504', 'ASH701945B_M', 'ASH701945E_M', 'JAV_GRANT-G3T',
                           'ASH700941.B', 'TWIVC6050', 'JAVRINGANT_G5T', 'NOV750.R4', 'TRM159900.00',
                           'LEIAT504GG', 'LEIAX1202GG', 'SEPCHOKE_MC', 'JPSREGANT_SD_E1', 'JNSCR_C146-22-1',
                           'TPSCR3_GGD', 'AOAD/M_T_RFI_T', 'ASH700936A_M', 'CHCC220GR2', 'LEIAR25',
                           'JPSREGANT_DD_E1', 'ASH700936C_M', 'ASH701073.1', 'AOAD/M_B', '3S-02-TSADM',
                           'ASH701933B_M', 'TRM29659.00', 'TRM41249.00', 'HITAT45101CP', 'HXCCGX601A', 'TRM59800.00C']
    main_win.igsAntList.sort()
    main_win.igsAntListComboCheck = ComboCheckBox(main_win.igsAntList, None)
    for i in range(main_win.igsAntListComboCheck.row_num):
        main_win.igsAntListComboCheck.qCheckBox[i].setChecked(True)
    siteMenu.addWidget(main_win.igsAntListComboCheck, 3, 0, 1, 1)

    antLable = QLabel('AntennaName')
    antLable.setFont(font)
    antLable.setAlignment(Qt.AlignRight)
    siteMenu.addWidget(antLable, 3, 1, 1, 1)

    none_lable0 = QLabel('')
    none_lable0.setMinimumSize(QSize(60, normalBtnH))
    siteMenu.addWidget(none_lable0, 0, 2, 4, 1)

    stationSelLable = QLabel('Station Selection')
    stationSelLable.setFont(font)
    stationSelLable.setAlignment(Qt.AlignCenter)
    siteMenu.addWidget(stationSelLable, 0, 3, 1, 3)

    # Thinning
    main_win.thinningLine = QLineEdit(main_win)
    main_win.thinningLine.setFont(font)
    siteMenu.addWidget(main_win.thinningLine, 1, 3, 1, 2)

    thinningLable = QLabel('Thinning  [deg]')
    thinningLable.setFont(font)
    thinningLable.setAlignment(Qt.AlignRight)
    siteMenu.addWidget(thinningLable, 1, 5, 1, 1)

    # 经度范围
    main_win.LminLine = QLineEdit(main_win)
    main_win.LminLine.setFont(font)
    main_win.LminLine.setText('-180')
    siteMenu.addWidget(main_win.LminLine, 2, 3, 1, 1)

    main_win.LmaxLine = QLineEdit(main_win)
    main_win.LmaxLine.setFont(font)
    main_win.LmaxLine.setText('180')
    siteMenu.addWidget(main_win.LmaxLine, 2, 4, 1, 1)

    LRangeLable = QLabel('L  Range  [deg]')
    LRangeLable.setFont(font)
    siteMenu.addWidget(LRangeLable, 2, 5, 1, 1)

    # 纬度范围
    main_win.BminLine = QLineEdit(main_win)
    main_win.BminLine.setFont(font)
    main_win.BminLine.setText('-90')
    siteMenu.addWidget(main_win.BminLine, 3, 3, 1, 1)

    main_win.BmaxLine = QLineEdit(main_win)
    main_win.BmaxLine.setFont(font)
    main_win.BmaxLine.setText('90')
    siteMenu.addWidget(main_win.BmaxLine, 3, 4, 1, 1)

    BRangeLable = QLabel('B  Range  [deg]')
    BRangeLable.setFont(font)
    siteMenu.addWidget(BRangeLable, 3, 5, 1, 1)

    none_lable = QLabel('')
    none_lable.setMinimumSize(QSize(60, normalBtnH))
    siteMenu.addWidget(none_lable, 0, 6, 4, 1)

    # 复选框
    main_win.siteNameCheckBox = QCheckBox('SITE NAME')
    main_win.siteNameCheckBox.setFont(font)
    main_win.siteNameCheckBox.setMinimumSize(QSize(200, normalBtnH))
    siteMenu.addWidget(main_win.siteNameCheckBox, 0, 7, 1, 1)

    main_win.globalCheckBox = QCheckBox('SET GLOBAL', main_win)
    main_win.globalCheckBox.setFont(font)
    siteMenu.addWidget(main_win.globalCheckBox, 1, 7, 1, 1)
    main_win.globalCheckBox.setChecked(True)

    # 按钮
    main_win.siteRefreshBtn = QPushButton('PLOT', main_win)
    main_win.siteRefreshBtn.setFont(font)
    main_win.siteRefreshBtn.setMinimumSize(QSize(125, normalBtnH))
    siteMenu.addWidget(main_win.siteRefreshBtn, 2, 7, 1, 1)
    main_win.siteRefreshBtn.clicked.connect(lambda: sitePlotProcess(main_win))

    main_win.siteSaveFileBtn = QPushButton('SAVE', main_win)
    main_win.siteSaveFileBtn.setFont(font)
    main_win.siteSaveFileBtn.setMinimumSize(QSize(125, normalBtnH))
    main_win.siteSaveFileBtn.clicked.connect(lambda: saveSite(main_win))
    siteMenu.addWidget(main_win.siteSaveFileBtn, 3, 7, 1, 1)

    none_lable2 = QLabel('')
    none_lable2.setMinimumSize(QSize(60, normalBtnH))
    siteMenu.addWidget(none_lable2, 0, 8, 4, 1)

    # 布局
    siteTop = QSplitter(Qt.Vertical)
    siteTop.addWidget(siteTop_in)

    siteDown = QSplitter(Qt.Vertical)
    siteDown.addWidget(siteDown_in)

    siteAllLayout = QSplitter(Qt.Vertical)
    siteAllLayout.addWidget(siteTop)
    siteAllLayout.addWidget(siteDown)
    siteAllLayout.setStretchFactor(3, 1)

    siteLayout = QHBoxLayout(main_win)
    siteLayout.addWidget(siteAllLayout)
    
    return siteLayout
