#!/usr/bin/python3
# -*- coding: utf-8 -*-
# CDD_Sub        : Get user input
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.06
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-01-14 - Version 2.06
from Format import *
from help import *
from Dowload import *
from GNSS_TYPE import *
from Get_Ftp import *


def top_cdd():
    """
    2022-03-27 :    一级菜单 by Chang Chuntao -> Version : 1.00
    2022-04-22 :    + 新增TRO一级类
                    by Chang Chuntao  -> Version : 1.11
    2022-04-30 :    * 新增GNSS日常使用工具：GNSS_Timestran
                    调整输入模式, 0 -> a -> HELP / b -> GNSS_Timestran，增加分栏
                    by Chang Chuntao  -> Version : 1.12
    2022-05-24 :    + 新增ION一级类
                    by Chang Chuntao  -> Version : 1.13
    2022-07-13 :    + 新增SpaceData一级类
                    + 新增SpaceData内资源SW_EOP
                    by Chang Chuntao  -> Version : 1.16
    2022-09-20 :    > 修正TRO -> TROP
                    by Chang Chuntao  -> Version : 1.22
    2022-09-28 :    + 新增COSMIC一级类
                    by Chang Chuntao  -> Version : 1.23
    2022-10-10 :    + 新增Tables一级类
                    by Chang Chuntao  -> Version : 1.24
    """
    print("")
    print("    +----------------------------------FAST--------------------------------------+")
    print("    |                                                                            |")
    print("    |    1 : BRDC                   2 : SP3                   3 : CLK            |")
    print("    |    4 : RINEX                  5 : ERP                   6 : BIA_DCB_OBX    |")
    print("    |    7 : ION_TRO                8 : SINEX                 9 : CNES_AR        |")
    print("    |   10 : Time_Series           11 : Velocity_Fields      12 : SLR            |")
    print("    |   13 : COSMIC                14 : PANDA                15 : GAMIT          |")
    print("    |                                                                            |")
    print("    +----------------------------------------------------------------------------+")
    print("    |                                                                            |")
    print("    |    a : HELP                   b : GNSS_Timestran                           |")
    print("    |                                                                            |")
    print("    +----------------------------------------------------------------------------+")

    PrintGDD("Note: 请输入数据编号 (eg. 2 or a)", "input")
    obj = input("     ")
    while True:
        if obj == "a" or obj == "b":
            return obj
        elif obj.isdigit():  # 判断输入是否为数字
            if int(obj) > len(gnss_type) or int(obj) < 0:  # 判断输入是否超出列表范围
                print("")
                PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2 or a)", "input")
                obj = input("     ")
            else:
                obj = int(obj)
                return obj
        else:
            PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2 or a)", "input")
            obj = input("     ")


def sub_cdd(obj):
    """
    2022-03-27 :    二级菜单 by Chang Chuntao -> Version : 1.00
    2022-04-12 :    新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    * 新增返回上级菜单操作，输入y回到上级菜单
                    by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-04-30 :    * 新增GNSS日常使用工具：GNSS_Timestran
                    gnssTimesTran调用
                    by Chang Chuntao  -> Version : 1.12
    2022-05-24 :    + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
                    CARG_ion、ESAG_ion、ESRG_ion
                    by Chang Chuntao  -> Version : 1.13
    2022-05-31 :    + 新增BIA内资源MGEX_WHU_OSB_bia
                    > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
                    by Chang Chuntao  -> Version : 1.14
    2022-07-03 :    + 新增CLK内资源MGEX_WUHU_clk
                    + 新增ERP内资源WUHU_erp
                    + 新增OBX内资源MGEX_WUHU_obx
                    by Chang Chuntao  -> Version : 1.15
    2022-07-13 :    + 新增SpaceData一级类
                    + 新增SpaceData内资源SW_EOP
                    by Chang Chuntao  -> Version : 1.16
    2022-07-22 :    + 新增SP3内资源MGEX_WUH_Hour_sp3
                    + 新增CLK内资源MGEX_WUH_Hour_clk
                    + 新增ERP内资源WUH_Hour_erp
                    by Chang Chuntao  -> Version : 1.17
    2022-07-27 :    > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
                    > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
                    > 修正MGEX_COD_clk资源
                    by Chang Chuntao  -> Version : 1.18
    2022-09-16 :    + 新增RINEX内MGEX_HK_cors
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    > 修正TRO -> TROP
                    + 新增TROP内资源Meteorological
                    by Chang Chuntao  -> Version : 1.22
    2022-09-28 :    + 新增COSMIC一级类
                    + 新增COSMIC内资源'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx','C1_L1b_atmPhs', 'C1_L1b_gpsBit',
                    'C1_L1b_ionPhs', 'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec', 'C1_L1b_scnLv1', 'C2_L1a_leoAtt',
                    'C2_L1a_opnGps', 'C2_L1a_podCrx', 'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2'
                    by Chang Chuntao  -> Version : 1.23
    2022-10-10 :    + 新增Tables一级类
                    + 新增Tables内资源'Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM','Panda_oceanload',
                    'Panda_oceantide', 'Panda_utcdif','Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                    'Panda_ut1tid', 'Panda_leap_sec',
                    'Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno','Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                    'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod','Gamit_svnav', 'Gamit_rcvant'
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    ****重新配置分组 !
                    ****新增QT界面！
                    > BIA DCB OBX -> BIA_DCB_OBX
                    > ION TRO -> ION_TRO
                    > ATX SW_EOP Tables<PANDA> -> PANDA
                    > Tables<GAMIT> -> GAMIT
                    + IGS_hfile -> GAMIT
    2022-11-10 :    + 新增MGEX_WUHR_sp3、MGEX_WUHR_clk
                    by Chang Chuntao  -> Version : 2.02
    2022-11-15 :    + 新增GRE_IGS_01S
                    by Chang Chuntao  -> Version : 2.03
    2022-12-04 :    > MGEX_WUH_sp3 -> MGEX_WHU_F_sp3 / MGEX_WUHR_sp3 -> MGEX_WHU_R_sp3 / MGEX_WUHU_sp3 -> MGEX_WHU_U_sp3
                    > MGEX_WUH_Hour_sp3 -> MGEX_WHU_Hour_sp3 / MGEX_SHA_sp3 -> MGEX_SHA_F_sp3 / MGEX_COD_sp3 -> MGEX_COD_F_sp3
                    > MGEX_GRG_sp3 -> MGEX_GRG_F_sp3 / MGEX_GFZ_R_sp3 -> MGEX_GFZR_sp3 / GRE_CODR_sp3 -> GRE_COD_R_sp3
                    > GLO_IGL_sp3 -> GLO_IGL_F_sp3
                    + MGEX_GFZ_F_sp3
                    > MGEX_WUH_clk -> MGEX_WHU_F_clk / MGEX_WUHR_clk -> MGEX_WHU_R_clk / MGEX_WUHU_clk -> MGEX_WHU_U_clk
                    > MGEX_WUH_Hour_clk -> MGEX_WHU_Hour_clk / MGEX_COD_clk -> MGEX_COD_F_clk / MGEX_GRG_clk -> MGEX_GRG_F_clk
                    > MGEX_GFZR_clk -> MGEX_GFZ_R_clk
                    + MGEX_SHA_F_clk / MGEX_GFZ_F_clk / GRE_COD_R_clk / GLO_IGL_F_clk
                    > WUH_erp -> WHU_F_erp / WUHU_erp -> WHU_U_erp / GFZ_erp -> GFZ_F_erp / COD_erp -> COD_R_erp
                    > WUH_Hour_erp -> WHU_Hour_erp
                    > MGEX_COD_bia -> MGEX_COD_R_bia / MGEX_GFZ_bia -> MGEX_GFZ_R_bia / MGEX_WHU_ABS_bia -> MGEX_WHU_R_ABS_bia
                    > MGEX_WHU_OSB_bia -> MGEX_WHU_R_OSB_bia
                    x MGEX_WHU_OSB(与MGEX_WHU_R_OSB_bia重复)
                    > MGEX_CAS_dcb -> MGEX_CAS_R_dcb
                    > MGEX_WUH_obx -> MGEX_WHU_F_obx / MGEX_COD_obx -> MGEX_COD_F_obx / MGEX_GFZ_obx -> MGEX_GFZ_F_obx
                    > MGEX_WUHU_obx -> MGEX_WHU_U_obx
                    > WUHG_ion -> WHUG_ion
                    + MGEX_COD_F_bia
                    by Chang Chuntao  -> Version : 2.05
    2023-01-13 :    > MGEX_IGS_atx -> MGEX_IGS14_atx
                    + MGEX_IGS20_atx
                    x 删除GPS_GFZ_sp3 / GPS_GFZ_clk
                    > MGEX_GFZ_F_sp3 -> GRE_GFZ_F_sp3 / MGEX_GFZ_F_clk -> GRE_GFZ_F_clk
                    by Chang Chuntao  -> Version : 2.06
    """
    print("")
    if obj == 1:
        print("    +------------------------------------BRDC------------------------------------+")
        print("    |                                                                            |")
        print("    +-------------------------------------GPS------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : GPS_brdc                                                            |")
        print("    |                                                                            |")
        print("    +------------------------------------GCRE------------------------------------+")
        print("    |                                                                            |")
        print("    |    2 : MGEX_brdc              3 : MGEX_CNAV_brdm         4 : MGEX_CNAV_brd4|")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 2:
        print("    +-------------------------------------SP3------------------------------------+")
        print("    |                                                                            |")
        print("    +-------------------------------------GPS------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_sp3            2 : GPS_IGR_sp3            3 : GPS_IGU_sp3   |")
        print("    |    4 : GPS_GRG_sp3                                                         |")
        print("    |                                                                            |")
        print("    +------------------------------------GCRE------------------------------------+")
        print("    |                                                                            |")
        print("    |    5 : MGEX_WHU_F_sp3         6 : MGEX_WHU_R_sp3         7 : MGEX_WHU_U_sp3|")
        print("    |    8 : MGEX_WHU_Hour_sp3      9 : MGEX_SHA_F_sp3        10 : MGEX_COD_F_sp3|")
        print("    |   11 : MGEX_GRG_F_sp3        12 : MGEX_GFZ_R_sp3        13 : GRE_GFZ_F_sp3 |")
        print("    |   14 : GRE_COD_R_sp3         15 : GLO_IGL_F_sp3                            |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 3:
        print("    +-------------------------------------CLK------------------------------------+")
        print("    |                                                                            |")
        print("    +-------------------------------------GPS------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_clk            2 : GPS_IGR_clk           3 : GPS_GRG_clk    |")
        print("    |    4 : GPS_IGS_clk_30s                                                     |")
        print("    |                                                                            |")
        print("    +------------------------------------GCRE------------------------------------+")
        print("    |                                                                            |")
        print("    |    6 : MGEX_WHU_F_clk         7 : MGEX_WHU_R_clk         8 : MGEX_WHU_U_clk|")
        print("    |    9 : MGEX_WHU_Hour_clk     10 : MGEX_SHA_F_clk        11 : MGEX_COD_F_clk|")
        print("    |   12 : MGEX_GRG_F_clk        14 : MGEX_GFZ_R_clk        13 : GRE_GFZ_F_clk |")
        print("    |   14 : GRE_COD_R_clk         15 : GLO_IGL_F_clk                            |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 4:
        print("    +------------------------------------RINEX-----------------------------------+")
        print("    |                                                                            |")
        print("    +-------------------------------------GPS------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_rnx            2 : GPS_USA_cors           3 : GPS_HK_cors   |")
        print("    |    4 : GPS_EU_cors            5 : GPS_AU_cors                              |")
        print("    |                                                                            |")
        print("    +------------------------------------GCRE------------------------------------+")
        print("    |                                                                            |")
        print("    |    6 : MGEX_IGS_rnx           7 : MGEX_HK_cors           8 : GRE_IGS_01S   |")
        print("    |    9 : GCRE_MGEX_01S                                                       |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 5:
        print("    +------------------------------------ERP-------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : IGS_erp                2 : IGR_erp                3 : WHU_F_erp     |")
        print("    |    4 : WHU_U_erp              5 : GFZ_F_erp              6 : COD_R_erp     |")
        print("    |    7 : WHU_Hour_erp                                                        |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 6:
        print("    +--------------------------------BIA_DCB_OBX---------------------------------+")
        print("    |                                     |                                      |")
        print("    +------------------------------------BIA-------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : GPS_COD_bia            2 : MGEX_COD_F_bia         3 : MGEX_COD_R_bia|")
        print("    |    4 : MGEX_WHU_R_ABS_bia     5 : MGEX_WHU_R_OSB_bia     6 : MGEX_GFZ_R_bia|")
        print("    |                                                                            |")
        print("    +------------------------------------DCB-------------------------------------+")
        print("    |                                                                            |")
        print("    |    7 : GPS_COD_dcb            8 : MGEX_CAS_R_dcb                           |")
        print("    |    9 : P1C1                  10 : P1P2                  11 : P2C2          |")
        print("    |                                                                            |")
        print("    +------------------------------------OBX-------------------------------------+")
        print("    |                                                                            |")
        print("    |   12 : GPS_COD_obx           13 : GPS_GRG_obx                              |")
        print("    |   14 : MGEX_WHU_F_obx        15 : MGEX_COD_F_obx        16 : MGEX_GFZ_F_obx|")
        print("    |   17 : MGEX_WHU_U_obx                                                      |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 7:
        print("    +----------------------------------ION_TRO-----------------------------------+")
        print("    |                                     |                                      |")
        print("    +------------------------------------ION-------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : IGSG_ion               2 : IGRG_ion               3 : WHUG_ion      |")
        print("    |    4 : WURG_ion               5 : CODG_ion               6 : CORG_ion      |")
        print("    |    7 : UQRG_ion               8 : UPRG_ion               9 : JPLG_ion      |")
        print("    |   10 : JPRG_ion              11 : CASG_ion              12 : CARG_ion      |")
        print("    |   13 : ESAG_ion              14 : ESRG_ion                                 |")
        print("    |                                                                            |")
        print("    +------------------------------------TRO-------------------------------------+")
        print("    |                                                                            |")
        print("    |   15 : IGS_zpd               16 : COD_tro               17 : JPL_tro       |")
        print("    |   18 : GRID_1x1_VMF3         19 : GRID_2.5x2_VMF1       20 : GRID_5x5_VMF3 |")
        print("    |   21 : Meteorological                                                      |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 8:
        print("    +-----------------------------------SINEX------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : IGS_day_snx            2 : IGS_week_snx           3 : IVS_week_snx  |")
        print("    |    4 : ILS_week_snx           5 : IDS_week_snx                             |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 9:
        print("    +----------------------------------CNES_AR-----------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : CNES_post              2 : CNES_realtime                            |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 10:
        print("    +--------------------------------Time_Series---------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : IGS14_TS_ENU           2 : IGS14_TS_XYZ           3 : Series_TS_Plot|")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 11:
        print("    +------------------------------Velocity_Fields-------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : IGS14_Venu             2 : IGS08_Venu             3 : PLATE_Venu    |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 12:
        print("    +------------------------------------SLR-------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : HY_SLR                 2 : GRACE_SLR              3 : BEIDOU_SLR    |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 13:
        print("    +-----------------------------------COSMIC-----------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : C1_L1a_leoAtt          2 : C1_L1a_opnGps          3 : C1_L1a_podCrx |")
        print("    |    4 : C1_L1b_atmPhs          5 : C1_L1b_gpsBit          6 : C1_L1b_ionPhs |")
        print("    |    7 : C1_L1b_leoClk          8 : C1_L1b_leoOrb          9 : C1_L1b_podTec |")
        print("    |   10 : C1_L1b_scnLv1                                                       |")
        print("    |   11 : C2_L1a_leoAtt         12 : C2_L1a_opnGps         13 : C2_L1a_podCrx |")
        print("    |   14 : C2_L1b_conPhs         15 : C2_L1b_leoOrb         16 : C2_L1b_podTc2 |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 14:
        print("    +-----------------------------------PANDA------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : Panda_jpleph_de405     2 : Panda_poleut1          3 : Panda_EGM     |")
        print("    |    4 : Panda_oceanload        5 : Panda_oceantide        6 : Panda_utcdif  |")
        print("    |    7 : Panda_antnam           8 : Panda_svnav            9 : Panda_nutabl  |")
        print("    |   10 : Panda_ut1tid          11 : Panda_leap_sec        12 : MGEX_IGS14_atx|")
        print("    |   13 : MGEX_IGS20_atx        14 : SW_EOP                15 : Panda_gpsrapid|")
        print("    +----------------------------------------------------------------------------+")
    elif obj == 15:
        print("    +-----------------------------------GAMIT------------------------------------+")
        print("    |                                                                            |")
        print("    |    1 : Gamit_pmu_bull         2 : Gamit_ut1usno          3 : Gamit_poleusno|")
        print("    |    4 : Gamit_dcb_dat          5 : Gamit_soltab           6 : Gamit_luntab  |")
        print("    |    7 : Gamit_leap_sec         8 : Gamit_nutabl           9 : Gamit_antmod  |")
        print("    |   10 : Gamit_svnav           11 : Gamit_rcvant          12 : Gamit_nbody   |")
        print("    |                                                                            |")
        print("    +----------------------------------SOLUTION----------------------------------+")
        print("    |                                                                            |")
        print("    |   13 : IGS_hfile                                                           |")
        print("    |                                                                            |")
        print("    +----------------------------------------------------------------------------+")
    elif obj == "a":
        cddhelp()
        return 0
    elif obj == "b":
        gnssTimesTran()
        return 0

    PrintGDD("Note: 请输入数据编号 (eg. 2)", "input")  # 二级索引
    PrintGDD("Note: 如需返回上级目录，请输入y", "input")  # 二级索引
    subnum = input("     ")
    while True:
        if subnum == "y" or subnum == "Y":
            return "y"
        else:
            if subnum.isdigit():  # 判断是否为数字
                if int(subnum) > objnum[obj - 1] or int(subnum) < 1:  # 判断输入是否超出列表范围
                    print("")
                    PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2)", "input")
                    PrintGDD("Note: 如需返回上级目录，请输入y", "input")  # 二级索引
                    subnum = input("     ")  # 二级索引
                else:
                    subnum = int(subnum)
                    return subnum
            else:
                PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2)", "input")
                PrintGDD("Note: 如需返回上级目录，请输入y", "input")  # 二级索引
                subnum = input("     ")


def yd_cdd():
    '''
    2022-03-27 :    输入年日时间
                    by Chang Chuntao -> Version : 1.00
    2022-04-12 :    *新增返回上级菜单操作，输入y回到上级菜单
                    by Chang Chuntao  -> Version : 1.10
    '''
    print()
    PrintGDD("若需下载多天数据，请输入 <年 起始年积日 截止年积日> <year start_doy end_doy>", "input")
    PrintGDD("若需下载单天数据，请输入 <年 年积日> <year doy>", "input")
    PrintGDD("Note: 如需返回上级目录，请输入y", "input")
    yd = input("     ")
    while True:
        if yd == "y" or yd == "Y":
            return "y"

        else:
            YD = yd.split()
            if len(YD) == 2:
                year = int(YD[0])
                day1 = int(YD[1])
                day2 = int(YD[1])
                return year, day1, day2
            elif len(YD) == 3:
                year = int(YD[0])
                day1 = int(YD[1])
                day2 = int(YD[2])
                return year, day1, day2
            else:
                PrintGDD("Warning: 请输入正确的时间!", "warning")
                PrintGDD("若需下载多天数据，请输入 <年 起始年积日 截止年积日> <year start_doy end_doy>", "input")
                PrintGDD("若需下载单天数据，请输入 <年 年积日> <year doy>", "input")
                PrintGDD("Note: 如需返回上级目录，请输入y", "input")
                yd = input("     ")


def ym_cdd():
    '''
    2022-03-27 :    输入年月时间
                    by Chang Chuntao -> Version : 1.00
    2022-04-12 :    *新增返回上级菜单操作，输入y回到上级菜单
                    by Chang Chuntao  -> Version : 1.10
    '''
    print()
    PrintGDD("Note: 请输入 <年 月> <year month>", "input")
    PrintGDD("Note: 如需返回上级目录，请输入y", "input")
    ym = input("     ")
    while True:
        if ym == "y" or ym == "Y":
            return "y"
        else:
            YM = ym.split()
            if len(YM) == 2:
                year = int(YM[0])
                month = int(YM[1])
                return year, month
            else:
                PrintGDD("Warning: 请输入正确的时间!", "warning")
                PrintGDD("请输入 <年 月> <year month>", "input")
                PrintGDD("Note: 如需返回上级目录，请输入y", "input")
                ym = input("     ")


def getFile(datatype):
    """
    2022-03-27 :    * 输入站点文件
                    by Chang Chuntao  -> Version : 1.00
    2023-01-14 :    + 支持直接输入站点名
                    by Chang Chuntao  -> Version : 2.06
    """
    print()
    PrintGDD(r"请输入站点名称或站点文件所在位置(绝对位置/相对位置)", "input")
    PrintGDD(r'例如直接输入站点名 - BJFS00CHN irkj urum', "input")
    PrintGDD(r'或输入站点文件(相对目录/绝对目录/当前目录文件) - site.txt 或 D:\site.txt', "input")
    PrintGDD(r"文件内写入站名, 长名短名都可, 按行按空格分割都可！例如文件内容 - BJFS00CHN irkj urum", "input")
    sitefile = input("     ")
    return getSite(sitefile, datatype)


def getvlbicompress(ftpsite):
    '''
    2022-04-12 : 文件检索解压 by Chang Chuntao  -> Version : 1.10
    '''
    print()
    PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！ / Press enter to unzip!", "input")
    isuncpmress = input("     ")
    if isuncpmress == "":
        unzip_vlbi(os.getcwd(), ftpsite)


def uncompress(urllist):
    '''
    2022-04-12 : 通过下载列表解压文件(年日) by Chang Chuntao  -> Version : 1.10
    '''
    ftpsite = []
    for i in range(len(urllist)):
        for j in range(len(urllist[i])):
            ftpsite.append(urllist[i][j])
    print()
    isuncpmress = "y"
    for f in ftpsite:
        if str(f).split(".")[-1] == "gz" or str(f).split(".")[-1] == "Z" or str(f).split(".")[-1] == "tgz":
            PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！ / Press enter to unzip!", "input")
            isuncpmress = input("     ")
            break
    if isuncpmress == "":
        unzipfile(os.getcwd(), ftpsite)


def uncompress_highrate_rinex(urllist, type):
    '''
    2022-11-15 : 通过下载列表解压GRE_IGS_01S文件 by Chang Chuntao  -> Version : 2.03
    '''
    ftpsite = []
    for i in range(len(urllist)):
        for j in range(len(urllist[i])):
            ftpsite.append(urllist[i][j])
    print()
    if type == 'GRE_IGS_01S':
        unzipfile_highrate_rinex2(os.getcwd(), ftpsite)
    elif type == 'GCRE_MGEX_01S':
        unzipfile_highrate_rinex3(os.getcwd(), ftpsite)


#
def uncompress_ym(url):
    '''
    2022-04-12 : 通过下载列表解压文件(年月) by Chang Chuntao  -> Version : 1.10
    '''
    isuncpmress = "y"
    ftpsite = []
    for u in url:
        ftpsite.append(u)
    for f in ftpsite:
        if str(f).split(".")[-1] == "gz" or str(f).split(".")[-1] == "Z":
            PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！ / Press enter to unzip!", "input")
            isuncpmress = input("     ")
            break
    if isuncpmress == "":
        unzipfile(os.getcwd(), ftpsite)


def geturl_download_uncompress(cddarg, obj):
    """
    2022-04-12 :    通过输入引导的参数获取下载列表，下载文件、解压文件 by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-08-04 :    修正时序文件下载需求
                    by Chang Chuntao  -> Version : 1.19
    2022-09-16 :    新增站点字符串替换子程序
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological，为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-11-02 :    > 添加DORIS判断
                    by Chang Chuntao  -> Version : 1.25
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    2022-11-15 :    > 添加GRE_IGS_01S判断,调用uncompress_highrate_rinex
                    by Chang Chuntao  -> Version : 2.03
    """
    urllist = []  # 下载列表

    # 数据类型为IVS_week_snx, lftp下载
    if cddarg['datatype'] == "IVS_week_snx":
        ftpsite = FTP_S[cddarg['datatype']][0]
        ym = ym_cdd()  # 获取下载时间
        if ym == "y":
            return "y"
        else:
            [year, month] = ym  # 获取下载时间
            ftpsite = ftpsite.replace('<YY>', str(year)[2:4])
            ftpsite = ReplaceMMM(ftpsite, month)
            PrintGDD("正在开始下载!", "important")
            start_time = timeit.default_timer()
            lftps(ftpsite)
            end_time = timeit.default_timer() - start_time
            PrintGDD("全部下载结束!", "important")
            PrintGDD("程序运行时间 : %.02f seconds" % end_time, "important")
            getvlbicompress(ftpsite)
            return "n"

    # 数据类型为输入年月
    elif cddarg['datatype'] in ym_type and cddarg['datatype'] != "IVS_week_snx":
        ftpsite = FTP_S[cddarg['datatype']]
        ym = ym_cdd()  # 获取下载时间
        if ym == "y":
            return "y"
        else:
            [year, month] = ym  # 获取下载时间
            ftpsite_new = []
            ym_datetime = datetime.datetime(year, month, 1)
            for ftp in ftpsite:
                ftp = ReplaceTimeWildcard(ftp, ym_datetime)
                wgets(ftp)
                ftpsite_new.append(ftp)
            uncompress_ym(ftpsite_new)
            return "n"

    else:
        # 数据类型为输入年日
        # 输入为年， 起始年积日， 终止年积日 的数据类型
        if cddarg['datatype'] in yd_type:
            yd = yd_cdd()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                cddarg['year'] = year
                cddarg['day1'] = day1
                cddarg['day2'] = day2
                PrintGDD(
                    "下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']),
                    "normal")
                print("")
                for day in range(cddarg['day1'], cddarg['day2'] + 1):
                    gpsweek, dayofweek = doy2gpswd(year, day)
                    if cddarg['datatype'] == 'IDS_week_snx':
                        if dayofweek == 0:
                            ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                            urllist.append(ftpsitelist)  # 按天下载
                    else:
                        ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                        urllist.append(ftpsitelist)  # 按天下载
                if len(urllist) == 0:
                    PrintGDD('此天无数据，请换天下载！', 'fail')
                    return "n"
                if cddarg['datatype'] == 'IGS_week_snx' or cddarg['datatype'] == 'IVS_week_snx' or cddarg[
                    'datatype'] == 'IDS_week_snx' or cddarg['datatype'] == 'ILS_week_snx':
                    cddpooldownload(urllist, 1)  # 多线程下载
                else:
                    cddpooldownload(urllist, 3)  # 多线程下载
                uncompress(urllist)
                return "n"

        # 数据类型为输入年日站点文件
        # 输入为年， 起始年积日， 终止年积日, 站点文件 的数据类型
        elif cddarg['datatype'] in yds_type:
            yd = yd_cdd()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                cddarg['year'] = year
                cddarg['day1'] = day1
                cddarg['day2'] = day2
                PrintGDD(
                    "下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']),
                    "normal")
                cddarg['site'] = getFile(cddarg['datatype'])
                for day in range(cddarg['day1'], cddarg['day2'] + 1):
                    ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                    for siteInList in cddarg['site']:
                        siteftp = []
                        for ftpInList in ftpsitelist:
                            ftpInList = replaceSiteStr(ftpInList, siteInList)
                            siteftp.append(ftpInList)
                        urllist.append(siteftp)  # 按天下载
                cddpooldownload(urllist, 3)  # 多线程下载

                if cddarg['datatype'] == "GRE_IGS_01S" or cddarg['datatype'] == "GCRE_MGEX_01S":
                    uncompress_highrate_rinex(urllist, cddarg['datatype'])
                else:
                    uncompress(urllist)
                return "n"

        elif cddarg['datatype'] in s_type:  # 输入为站点文件 的数据类型
            cddarg['site'] = getFile(cddarg['datatype'])
            ftpsite = FTP_S[cddarg['datatype']]
            for siteInList in cddarg['site']:
                siteftp = []
                for ftpInList in ftpsite:
                    ftpInList = replaceSiteStr(ftpInList, siteInList)
                    siteftp.append(ftpInList)
                urllist.append(siteftp)  # 按天下载
            cddpooldownload(urllist, 3)  # 多线程下载
            uncompress(urllist)
            return "n"

        # 无需输入时间的数据类型
        elif cddarg['datatype'] in no_type:
            ftpsite = FTP_S[cddarg['datatype']]
            for ftp in ftpsite:
                wgets(ftp)
            cddpooldownload(urllist, 3)  # 多线程下载
            uncompress(urllist)
            return "n"
