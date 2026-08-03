# -*- coding: utf-8 -*-
# FAST           : Site UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : AIR, Chinese Academy of Sciences
# Creation       : 2026.03.18
# Latest Version : 3.01.01 - 2026.08.03

from PyQt5.QtWidgets import QGridLayout, QComboBox, QFrame, QWidget, QSplitter, \
    QLabel, QPushButton, QLineEdit, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt, QSize
from fast.qt.qtFrame import ComboCheckBox
from fast.qt.qtSite import sitePlotProcess, siteChooseFileProcess, siteCombBoxChanged, saveSite

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt


def init_site_ui(main_win, font, chinese, label_h, normalBtnH):
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
    main_win.siteCombBox.setMinimumSize(QSize(70, label_h))
    main_win.siteCombBox.setToolTip('ALL IGS SITE: 全部IGS站点\nIGS LIST FILE: 4位站名列表文件\nSITE FILE: 自定义站点文件(L,B,siteName)')
    main_win.siteCombBox.currentIndexChanged.connect(lambda: siteCombBoxChanged(main_win))
    siteMenu.addWidget(main_win.siteCombBox, 0, 0, 1, 2)

    # 站点文件
    main_win.siteFileChoose = QLineEdit(main_win)
    main_win.siteFileChoose.setFont(font)
    siteMenu.addWidget(main_win.siteFileChoose, 1, 0, 1, 1)
    main_win.siteFileChoose.setEnabled(False)

    main_win.siteFileData = None
    main_win.siteChooseFileBtn = QPushButton('SELECT FILE', main_win)
    main_win.siteChooseFileBtn.setFont(font)
    siteMenu.addWidget(main_win.siteChooseFileBtn, 1, 1, 1, 1, alignment=Qt.AlignRight)
    main_win.siteChooseFileBtn.clicked.connect(lambda: siteChooseFileProcess(main_win))
    main_win.siteChooseFileBtn.setEnabled(False)

    # GNSS系统
    main_win.igsSiteSys = ComboCheckBox(['GPS', 'GLO', 'GAL', 'BDS', 'SBAS', 'QZSS', 'IRNSS'], None)
    main_win.igsSiteSys.setMinimumSize(QSize(40, label_h))
    main_win.igsSiteSys.qCheckBox[0].setChecked(True)
    siteMenu.addWidget(main_win.igsSiteSys, 2, 0, 1, 1)

    igsSiteSysLabel = QLabel('GNSS System')
    igsSiteSysLabel.setFont(font)
    igsSiteSysLabel.setAlignment(Qt.AlignRight)
    siteMenu.addWidget(igsSiteSysLabel, 2, 1, 1, 1)

    # 天线列表: 从站点信息文件(IGSNetworkWithFormer.json)中读取所有天线类型
    # 2026.08.03 : 由写死的列表改为从JSON站点信息初始化
    #              by ChangChuntao -> Version : 3.01.01
    import os
    igsAntList = []
    if os.path.isdir(os.path.join(main_win.exeDirName, 'win_bin', 'bin')):
        binDir = os.path.join(main_win.exeDirName, 'win_bin', 'bin')
    else:
        binDir = os.path.join(main_win.exeDirName, 'mac_bin', 'bin')
    igsSiteFile = os.path.join(binDir, 'IGSNetworkWithFormer.json')
    if not os.path.isfile(igsSiteFile):
        igsSiteFile = os.path.join(binDir, 'IGSNetwork.csv')   # 兼容旧版CSV
    if os.path.isfile(igsSiteFile):
        from fast.com.mgexSite import readMegxSiteInf
        megxSiteList = readMegxSiteInf(igsSiteFile)
        for siteShort in megxSiteList:
            antName = megxSiteList[siteShort]['Ant']
            if antName and antName not in igsAntList:
                igsAntList.append(antName)
    if not igsAntList:
        # 站点信息文件读取失败时回退到默认天线列表
        igsAntList = ['TRM57971.00', 'ASH701945G_M', 'TRM59800.99', 'TRM159800.00',
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
    main_win.igsAntList = igsAntList
    main_win.igsAntList.sort()
    main_win.igsAntListComboCheck = ComboCheckBox(main_win.igsAntList, None)
    for i in range(main_win.igsAntListComboCheck.row_num):
        main_win.igsAntListComboCheck.qCheckBox[i].setChecked(True)
    siteMenu.addWidget(main_win.igsAntListComboCheck, 3, 0, 1, 1)

    antLabel = QLabel('AntennaName')
    antLabel.setFont(font)
    antLabel.setAlignment(Qt.AlignRight)
    siteMenu.addWidget(antLabel, 3, 1, 1, 1)

    none_label0 = QLabel('')
    none_label0.setMinimumSize(QSize(60, normalBtnH))
    siteMenu.addWidget(none_label0, 0, 2, 4, 1)

    stationSelLabel = QLabel('Station Selection')
    stationSelLabel.setFont(font)
    stationSelLabel.setAlignment(Qt.AlignCenter)
    siteMenu.addWidget(stationSelLabel, 0, 3, 1, 3)

    # Thinning
    main_win.thinningLine = QLineEdit(main_win)
    main_win.thinningLine.setFont(font)
    main_win.thinningLine.setToolTip('站点抽稀间隔(度), 留空则不抽稀')
    siteMenu.addWidget(main_win.thinningLine, 1, 3, 1, 2)

    thinningLabel = QLabel('Thinning  [deg]')
    thinningLabel.setFont(font)
    thinningLabel.setAlignment(Qt.AlignRight)
    siteMenu.addWidget(thinningLabel, 1, 5, 1, 1)

    # 经度范围
    main_win.LminLine = QLineEdit(main_win)
    main_win.LminLine.setFont(font)
    main_win.LminLine.setText('-180')
    main_win.LminLine.setToolTip('经度下限(deg)')
    siteMenu.addWidget(main_win.LminLine, 2, 3, 1, 1)

    main_win.LmaxLine = QLineEdit(main_win)
    main_win.LmaxLine.setFont(font)
    main_win.LmaxLine.setText('180')
    main_win.LmaxLine.setToolTip('经度上限(deg)')
    siteMenu.addWidget(main_win.LmaxLine, 2, 4, 1, 1)

    LRangeLabel = QLabel('L  Range  [deg]')
    LRangeLabel.setFont(font)
    siteMenu.addWidget(LRangeLabel, 2, 5, 1, 1)

    # 纬度范围
    main_win.BminLine = QLineEdit(main_win)
    main_win.BminLine.setFont(font)
    main_win.BminLine.setText('-90')
    main_win.BminLine.setToolTip('纬度下限(deg)')
    siteMenu.addWidget(main_win.BminLine, 3, 3, 1, 1)

    main_win.BmaxLine = QLineEdit(main_win)
    main_win.BmaxLine.setFont(font)
    main_win.BmaxLine.setText('90')
    main_win.BmaxLine.setToolTip('纬度上限(deg)')
    siteMenu.addWidget(main_win.BmaxLine, 3, 4, 1, 1)

    BRangeLabel = QLabel('B  Range  [deg]')
    BRangeLabel.setFont(font)
    siteMenu.addWidget(BRangeLabel, 3, 5, 1, 1)

    none_label = QLabel('')
    none_label.setMinimumSize(QSize(60, normalBtnH))
    siteMenu.addWidget(none_label, 0, 6, 4, 1)

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
    main_win.siteRefreshBtn.setToolTip('绘制站点分布图')
    siteMenu.addWidget(main_win.siteRefreshBtn, 2, 7, 1, 1)
    main_win.siteRefreshBtn.clicked.connect(lambda: sitePlotProcess(main_win))

    main_win.siteSaveFileBtn = QPushButton('SAVE', main_win)
    main_win.siteSaveFileBtn.setFont(font)
    main_win.siteSaveFileBtn.setMinimumSize(QSize(125, normalBtnH))
    main_win.siteSaveFileBtn.setToolTip('保存站点图(PNG)与站点信息文件')
    main_win.siteSaveFileBtn.clicked.connect(lambda: saveSite(main_win))
    siteMenu.addWidget(main_win.siteSaveFileBtn, 3, 7, 1, 1)

    none_label2 = QLabel('')
    none_label2.setMinimumSize(QSize(60, normalBtnH))
    siteMenu.addWidget(none_label2, 0, 8, 4, 1)

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
